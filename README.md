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

To use the license contract you first need to run a MuesliSwap On-Chain DAO. This can then be extended with the license consumer smart contract as explained in our report. For this, you need to have an Ogmios endpoint available and set the environment variables OGMIOS_API_HOST, OGMIOS_API_PROTOCOL and OGMIOS_API_PORT to the respective values (default localhost, ws and 1337).

Create and fund two wallets for the DAO administration and for voting.
You can use the [testnet faucet](https://docs.cardano.org/cardano-testnet/tools/faucet/) to fund them, make sure to select `preprod` network!.

```bash
python3 -m batcher_dao_governance.create_key_pair creator
python3 -m batcher_dao_governance.create_key_pair voter
python3 -m batcher_dao_governance.create_key_pair vault_admin
```

Then, build the smart contracts. Note that this requires the [`aiken`](https://aiken-lang.org) executable present in the `PATH` environment variable. 

```bash
python3 -m batcher_dao_governance.build
``` 
You can then use the license creation script in connection with the MuesliSwap On-Chain DAO scripts. For this, you need to create a new proposal that can create licenses. The license are then released with limited validity to the specified address if the tally is successful. Tallys are expected to have infinite validity and do not need to be finished for releasing licenses. However the quorum must be reached.

The license name is structured as follows:
- The first 3 bytes are the id of the winning tally in big-endian, left-padded with 0s
- The remaining bytes are the expiry date of the license in POSIX time, milliseconds, big-endian.
  They may be left-padded with 0s but do not have to be.

Outputs of this contract may go to:
- The winning address of the referenced address in the winning tally

Reference inputs:
- tally/tally (1, referencing a winning proposal that indicates a governance upgrade)

NFTs that the outputs may hold:
- licenses/licenses (previously minted plus the own minted one)

It is not allowed to mint several license NFTs with distinct names in a single transaction but well allowed to mint
several licenses of the same name (i.e. expiry date). You can use this requirements to then construct a valid transaction that allows for the minting of this NFT. 

### References 
[1]: [Decentralised Batcher Framework with DAO governance](https://projectcatalyst.io/funds/12/cardano-open-developers/decentralised-batcher-framework-with-dao-governance)
