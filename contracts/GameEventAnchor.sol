// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract GameEventAnchor {
    struct AnchoredEvent {
        bytes32 eventHash;
        uint256 seq;
        bytes32 prevHash;
        uint256 anchoredAt;
    }

    mapping(bytes32 => bool) public isEventAnchored;
    mapping(uint256 => AnchoredEvent) private eventsBySeq;
    uint256 public lastSeq;
    bytes32 public lastEventHash;

    event GameEventAnchored(bytes32 indexed eventHash, uint256 indexed seq, bytes32 prevHash, address sender);

    function anchorGameEvent(bytes32 eventHash, uint256 seq, bytes32 prevHash) external {
        require(eventHash != bytes32(0), "ZERO_EVENT_HASH");
        require(!isEventAnchored[eventHash], "DUPLICATE_EVENT_HASH");

        if (lastSeq == 0) {
            require(seq == 1, "FIRST_SEQ_MUST_BE_1");
            require(prevHash == bytes32(0), "FIRST_PREV_MUST_BE_ZERO");
        } else {
            require(seq == lastSeq + 1, "SEQ_GAP");
            require(prevHash == lastEventHash, "CONTINUITY_MISMATCH");
        }

        isEventAnchored[eventHash] = true;
        eventsBySeq[seq] = AnchoredEvent({
            eventHash: eventHash,
            seq: seq,
            prevHash: prevHash,
            anchoredAt: block.timestamp
        });

        lastSeq = seq;
        lastEventHash = eventHash;

        emit GameEventAnchored(eventHash, seq, prevHash, msg.sender);
    }

    function getEventBySeq(uint256 seq) external view returns (AnchoredEvent memory) {
        return eventsBySeq[seq];
    }
}
