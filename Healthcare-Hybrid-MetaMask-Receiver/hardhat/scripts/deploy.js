const hre = require("hardhat");

async function main() {

  const HealthcareAuth = await hre.ethers.getContractFactory("HealthcareAuth");

  const contract = await HealthcareAuth.deploy();

  await contract.waitForDeployment();

  console.log("HealthcareAuth deployed to:", await contract.getAddress());

}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});