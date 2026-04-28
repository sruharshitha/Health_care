// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HealthcareAuth {

    string public cid;

    function storeCID(string memory _cid) public {
        cid = _cid;
    }

    function getCID() public view returns(string memory){
        return cid;
    }
}