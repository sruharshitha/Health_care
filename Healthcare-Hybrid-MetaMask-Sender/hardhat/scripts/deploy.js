const { ethers } = require("hardhat");

async function main() {

  const HealthcareAuth = await ethers.getContractFactory("HealthcareAuth");

  const contract = await HealthcareAuth.deploy();

  await contract.waitForDeployment();

  console.log("Contract deployed at:", await contract.getAddress());

}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});