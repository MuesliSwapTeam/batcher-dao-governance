import subprocess
import sys
from pathlib import Path
from typing import Union
import fire

from batcher_dao_governance.onchain.licenses import licenses


def build_compressed(
    type: str, script: Union[Path, str], cli_options=("--cf",), args=()
):
    script = Path(script)
    command = [
        sys.executable,
        "-m",
        "opshin",
        *cli_options,
        "build",
        type,
        script,
        *args,
        "--recursion-limit",
        "2000",
        "-O2",
    ]
    subprocess.run(command, check=True)

    built_contract = Path(f"build/{script.stem}/script.cbor")
    built_contract_compressed_cbor = Path(f"build/tmp.cbor")

    with built_contract_compressed_cbor.open("wb") as fp:
        subprocess.run(
            ["aiken", "uplc", "shrink", built_contract, "--cbor", "--hex"],
            stdout=fp,
            check=True,
        )

    subprocess.run(
        [
            sys.executable,
            "-m",
            "uplc",
            "build",
            "--from-cbor",
            built_contract_compressed_cbor,
            "-o",
            f"build/{script.stem}_compressed",
            "--recursion-limit",
            "2000",
        ]
    )


def main():
    build_compressed("minting", licenses.__file__)


if __name__ == "__main__":
    fire.Fire(main)
