import algokit_utils as au
import algosdk as sdk
from utils import (
    account_creation,
    display_info,
)
import algokit_utils.transactions.transaction_composer as att

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
    charlie = account_creation(algorand, "CHARLIE", au.AlgoAmount(algo=100))

    # asset_id = generate_test_asset(algorand=algorand, sender=alice, total=15)
    asset_id = 1005

import os

os.system("algokit compile py --out-dir ./app app.py")
os.system("algokit generate client app/DigitalMarketplace.arc32.json --output client.py")

import client as cl

factory = algorand.client.get_typed_app_factory(
    cl.DigitalMarketplaceFactory, default_sender=alice.address
)

# result, _ = factory.send.create.create_application(
#         cl.CreateApplicationArgs(
#             asset_id=asset_id, unitary_price=au.AlgoAmount(algo=1).micro_algo
#         )
#     )
# app_id = result.app_id
app_id = 1014

ac = factory.get_app_client_by_id(app_id, default_sender=alice.address)

sp=algorand.get_suggested_params()

mbr_pay_txn=algorand.create_transaction.payment(
    au.PaymentParams(
        sender=alice.address,
        receiver=ac.app_address,
        amount=au.AlgoAmount(algo=0.2),
        extra_fee=au.AlgoAmount(micro_algo=sp.min_fee)
    )
)

# ac.send.opt_in_to_asset(
#     cl.OptInToAssetArgs(
#         mbr_pay=att.TransactionWithSigner(mbr_pay_txn, alice.signer)
#     ),
    
# result=ac.send.opt_in_to_asset(
#     cl.OptInToAssetArgs(
#         mbr_pay=att.TransactionWithSigner(mbr_pay_txn, alice.signer)
#     ),
#     au.CommonAppCallParams(
#         asset_references=[asset_id]
#     )
# )

print("Alice send to the APP")
algorand.send.asset_transfer(
    au.AssetTransferParams(
        sender=alice.address,
        receiver=ac.app_address,
        amount=10,
        asset_id=asset_id,
    )
)

amt_to_buy = 2
buyer_payment_txn = algorand.create_transaction.payment(
    au.PaymentParams(
        sender=charlie.address,
        receiver=ac.app_address,
        amount=au.AlgoAmount(
            micro_algo=amt_to_buy*ac.state.global_state.unitary_price
        ),
        extra_fee=au.AlgoAmount(micro_algo=sp.min_fee)
    )
)


composer = algorand.new_group()
composer.add_asset_opt_in(
    au.AssetOptInParams(
        sender=charlie.address,
        receiver=charlie.address,
        asset_id=asset_id
    )
)

print(f"Hold ASA-ID= {algod_client.account_info(ac.app_address)['assets']}")

composer.add_app_call_method_call(
    ac.params.buy(
        cl.BuyArgs(
            buyer_txn=att.TransactionWithSigner(
                txn=buyer_payment_txn,
                signer=charlie.signer
            ),
            quantity=2
        ),
    ),
    ac.CommonAppCallParams(
        sender=charlie.address,
        signer=charlie.signer,
    ),
)