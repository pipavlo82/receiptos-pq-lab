// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract ReceiptAnchor {
    mapping(bytes32 => bool) private anchored;

    event ReceiptAnchored(bytes32 indexed receiptHash, address indexed sender);

    function anchorReceipt(bytes32 receiptHash) external {
        require(receiptHash != bytes32(0), "ZERO_HASH");
        require(!anchored[receiptHash], "ALREADY_ANCHORED");

        anchored[receiptHash] = true;
        emit ReceiptAnchored(receiptHash, msg.sender);
    }

    function isAnchored(bytes32 receiptHash) external view returns (bool) {
        return anchored[receiptHash];
    }
}
