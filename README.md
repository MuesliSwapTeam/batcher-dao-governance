MuesliSwap Batcher DAO Governance
---------------------------------

This repository contains the documentation and code for the implementation
of the MuesliSwap Batcher DAO Governance funded in Fund 12 by Project Catalyst [1].

### Structure

The directory `batcher_dao_governance` contains the code for the blockchain part of the Batcher DAO Governance system.
The following subdirectories are present:

- `onchain`: Contains the code for the on-chain part of the system i.e. Smart Contracts written in OpShin
- `offchain`: Contains the code for the off-chain part of the system i.e. building and submitting transactions for interaction with the Smart Contracts
- `tests`: Contains the tests for the on-chain part of the system

### Setup

First, install python poetry. For this, follow the official documentation [here](https://python-poetry.org/docs/#installation).

```bash
poetry install
```

Building the smart contracts requires the [`aiken`](https://aiken-lang.org) executable present in the `PATH` environment variable. The original contract was built with version `aiken v1.0.26-alpha+075668b`. Then the contract can be built using the following command:

```bash
python3 -m batcher_dao_governance.build
``` 


[1]: [Decentralised Batcher Framework with DAO governance](https://projectcatalyst.io/funds/12/cardano-open-developers/decentralised-batcher-framework-with-dao-governance)