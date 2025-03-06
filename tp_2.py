import algokit_utils as au
import algosdk as sdk
from utils import (
    account_creation,
    display_info,
)
from algokit_utils import AlgorandClient, AssetCreateParams
import random


# Générer l'asset
def generate_test_asset(algorand: au.AlgorandClient, sender: au.SigningAccount , total: int | None = None) -> int:
    """Create a test asset and return its ID"""
    if total is None:
        total = 15

    create_result = algorand.send.asset_create(
        AssetCreateParams(
            sender=sender.address,
            total=total,
            decimals=0,
            default_frozen=False,
            unit_name="TST",
            asset_name=f"Test Asset TP 2",
        )
    )

    print(create_result)

    return int(create_result.confirmation["asset-index"])

if __name__ == "__main__":
    # Choisir le réseau localnet
    algorand = au.AlgorandClient.from_environment()

    algod_client = algorand.client.algod
    indexer_client = algorand.client.indexer

    print(algod_client.block_info(0))
    print(indexer_client.health())

    # Création des comptes pour Alice et Bob
    alice = account_creation(algorand, "ALICE", au.AlgoAmount(algo=10_000))
    bob = account_creation(algorand, "BOB", au.AlgoAmount(algo=100))

    # asset_id = generate_test_asset(algorand=algorand, sender=alice, total=15)
    asset_id = 1005

    result = (
        algorand.new_group()
        .add_asset_opt_in(
            au.AssetOptInParams(
                sender=bob.address,
                asset_id=asset_id,
                signer=bob.signer,
            ))
            
        .add_payment(au.PaymentParams(
            sender=bob.address,
            receiver=alice.address,
            amount=au.AlgoAmount.from_algo(1),
        ))
        .add_asset_transfer(
            au.AssetTransferParams(
                sender=alice.address,
                receiver=bob.address,
                amount=1,
                asset_id=asset_id,
            ))
        .send()
    )
    display_info(algorand, ["Alice", "Bob"])