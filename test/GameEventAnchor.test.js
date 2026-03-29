const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("GameEventAnchor", function () {
  this.timeout(120000);

  async function deployFixture() {
    const F = await ethers.getContractFactory("GameEventAnchor");
    const c = await F.deploy();
    await c.waitForDeployment();
    return c;
  }

  async function mine() {
    await ethers.provider.send("evm_mine", []);
  }

  async function expectRevertContains(promise, msg) {
    let ok = false;
    try {
      await promise;
      await mine();
    } catch (e) {
      ok = String(e).includes(msg);
    }
    expect(ok).to.equal(true);
  }

  it("anchors successful chained game events", async function () {
    const c = await deployFixture();

    const e1 = ethers.keccak256(ethers.toUtf8Bytes("loot:player42:phoenix_bow"));
    const e2 = ethers.keccak256(ethers.toUtf8Bytes("match:tourn-sf-02:red-16-14"));

    await c.anchorGameEvent(e1, 1, ethers.ZeroHash);
    await mine();
    await c.anchorGameEvent(e2, 2, e1);
    await mine();

    const s1 = await c.getEventBySeq(1);
    const s2 = await c.getEventBySeq(2);

    expect(s1.eventHash).to.equal(e1);
    expect(s2.eventHash).to.equal(e2);
    expect(await c.lastSeq()).to.equal(2n);
  });

  it("rejects continuity mismatch", async function () {
    const c = await deployFixture();

    const e1 = ethers.keccak256(ethers.toUtf8Bytes("loot:valid:1"));
    const e2 = ethers.keccak256(ethers.toUtf8Bytes("match:valid:2"));
    const wrongPrev = ethers.keccak256(ethers.toUtf8Bytes("wrong-prev"));

    await c.anchorGameEvent(e1, 1, ethers.ZeroHash);
    await mine();
    await expectRevertContains(c.anchorGameEvent(e2, 2, wrongPrev), "CONTINUITY_MISMATCH");
  });

  it("rejects duplicate event hash (replay-style)", async function () {
    const c = await deployFixture();

    const e1 = ethers.keccak256(ethers.toUtf8Bytes("loot:player42:rare"));
    await c.anchorGameEvent(e1, 1, ethers.ZeroHash);
    await mine();
    await expectRevertContains(c.anchorGameEvent(e1, 2, e1), "DUPLICATE_EVENT_HASH");
  });

  it("gaming-oriented scenario: loot fairness then match integrity chain", async function () {
    const c = await deployFixture();

    const lootFairnessHash = ethers.keccak256(
      ethers.toUtf8Bytes("game:arena-alpha|event:loot_drop|player:42|item:phoenix_bow|proof:vrf")
    );

    const matchIntegrityHash = ethers.keccak256(
      ethers.toUtf8Bytes("game:arena-alpha|event:match_result|match:tourn-sf-02|winner:red|score:16-14|mode:hybrid")
    );

    await c.anchorGameEvent(lootFairnessHash, 1, ethers.ZeroHash);
    await mine();
    await c.anchorGameEvent(matchIntegrityHash, 2, lootFairnessHash);
    await mine();

    expect(await c.isEventAnchored(lootFairnessHash)).to.equal(true);
    expect(await c.isEventAnchored(matchIntegrityHash)).to.equal(true);
  });
});
