const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("ReceiptAnchor", function () {
  this.timeout(120000);

  async function deployFixture() {
    const F = await ethers.getContractFactory("ReceiptAnchor");
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

  it("anchors a receipt hash successfully", async function () {
    const c = await deployFixture();
    const hash = ethers.keccak256(ethers.toUtf8Bytes("receipt:loot:valid"));

    await c.anchorReceipt(hash);
    await mine();
    expect(await c.isAnchored(hash)).to.equal(true);
  });

  it("rejects duplicate/replay anchor", async function () {
    const c = await deployFixture();
    const hash = ethers.keccak256(ethers.toUtf8Bytes("receipt:loot:dup"));

    await c.anchorReceipt(hash);
    await mine();
    await expectRevertContains(c.anchorReceipt(hash), "ALREADY_ANCHORED");
  });
});
