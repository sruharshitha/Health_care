// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HealthcareAuth {

    struct Message {
        string cid;
        address sender;
        string token;
    }

    Message[] public messages;

    // -------------------------
    // STORE MESSAGE
    // -------------------------
    function storeMessage(
        string memory _cid,
        address _sender,
        string memory _token
    ) public {
        messages.push(Message(_cid, _sender, _token));
    }

    // -------------------------
    // GET MESSAGE BY INDEX
    // -------------------------
    function getMessage(uint index)
        public
        view
        returns (string memory, address, string memory)
    {
        Message memory m = messages[index];
        return (m.cid, m.sender, m.token);
    }

    // -------------------------
    // GET TOTAL COUNT
    // -------------------------
    function messagesLength() public view returns (uint) {
        return messages.length;
    }
}