import algokit_utils as au
import algosdk as sdk
from algokit_utils import AlgorandClient, TransactionParameters
from utils import (
    account_creation,
)
import os
os.system("algokit compile py --out-dir ./app app.py")
os.system("algokit generate client app/Eval.arc32.json --output client.py")
import client as cl
import algokit_utils.transactions.transaction_composer as att

# --------------------------------------------------------------------- INITIALISATION DE L'ALGORAND CLIENT ---------------------------------------------------------------------
# Se connecter au testnet
algorand = au.AlgorandClient.testnet()

algod_client = algorand.client.algod
indexer_client = algorand.client.indexer

print(algod_client.block_info(0))
print(indexer_client.health())

# --------------------------------------------------------------------- RECUPERATION DU COMPTE DE L'UTILISATEUR ---------------------------------------------------------------------
# Récupérer le compte de l'utilisateur et son adresse :
mnemonic = "mixed october dose hurry process myself captain already knee sure alpha enable divert net over suggest coconut feed system eight fog nothing ice able crouch"
private_key = sdk.mnemonic.to_private_key(mnemonic)
account = sdk.account.address_from_private_key(private_key)
print("Compte de l'utilisateur :", account)
print("Adresse de l'utilisateur :", private_key)
axel = algorand.account.from_mnemonic(mnemonic=mnemonic)

# --------------------------------------------------------------------- APPEL DE LA FONCTION claim_algo ---------------------------------------------------------------------
    # @arc4.abimethod
    # def claim_algo(self) -> None:
    #     assert Txn.sender in self.q4_string
    #     assert Txn.sender not in self.q1
    #     self.q1[Txn.sender] = arc4.Bool(True)
    #     itxn.Payment(
    #         receiver=Txn.sender,
    #         amount=500_000,
    #         fee=2*op.Global.min_txn_fee
    #     ).submit()

evalFactory = cl.EvalFactory(
    algorand=algorand,
    default_sender=axel.address
)

evalId = 736038676
print("ID de l'application :", evalId)
eval = evalFactory.get_app_client_by_id(evalId)

# Appel de la fonction claim_algo
# result = eval.send.claim_algo(
#     params=au.CommonAppCallParams(
#         sender=axel.address,
#         signer=axel.signer,
#         box_references=[axel.public_key, b"q1" + axel.public_key]
#     ),
#     send_params=au.SendParams(populate_app_call_resources=True)
# )

# --------------------------------------------------------------------- CREATION DE L'ASSET ---------------------------------------------------------------------
    # @arc4.abimethod
    #     def opt_in_to_asset(self, mbr_pay: gtxn.PaymentTransaction, asset: Asset) -> None:
    #         assert Txn.sender in self.q4_string
    #         assert Txn.sender not in self.q2
    #         self.q2[Txn.sender] = arc4.Bool(True)
    #         assert not Global.current_application_address.is_opted_in(asset)
    #         assert mbr_pay.receiver == Global.current_application_address
    #         assert mbr_pay.amount == Global.min_balance + Global.asset_opt_in_min_balance
    #         itxn.AssetTransfer(
    #             xfer_asset=asset.id,
    #             asset_receiver=Global.current_application_address,
    #             asset_amount=0,
    #         ).submit()

# res_asset = algorand.send.asset_create(
#     au.AssetCreateParams(
#         sender=axel.address,
#         signer=axel.signer,
#         total=15,
#         decimals=0,
#         default_frozen=False,
#     )
# )

# assetId = res_asset.confirmation["asset-index"]
# sp = algorand.get_suggested_params()
# mbr_pay_txn = algorand.create_transaction.payment(
#     au.PaymentParams(
#         sender=axel.address,
#         receiver=eval.app_address,
#         amount=au.AlgoAmount(algo=0.2),
#         extra_fee=au.AlgoAmount(micro_algo=sp.min_fee)
#     )
# )

# result = eval.send.opt_in_to_asset(
#         cl.OptInToAssetArgs(
#             mbr_pay=att.TransactionWithSigner(mbr_pay_txn, axel.signer),
#             asset=assetId
#         ),
#         params=au.CommonAppCallParams(
#             sender=axel.address,
#             signer=axel.signer,
#             box_references=[axel.public_key, b"q2" + axel.public_key]
#         ),
#         send_params=au.SendParams(populate_app_call_resources=True)
#     )

# --------------------------------------------------------------------- APPEL DE LA FONCTION sum ---------------------------------------------------------------------
    # @arc4.abimethod
    # def sum(self, array: Bytes) -> UInt64:
    #     assert Txn.sender in self.q4_string
    #     assert Txn.sender not in self.q3
    #     self.q3[Txn.sender] = arc4.Bool(True)
    #     assert array.length == 2

    #     total = UInt64(0)
    #     for n in array:
    #         total += op.btoi(n)
    #     return total

# result = eval.send.sum(
#     cl.SumArgs(
#         array=bytes([1, 2]),
#     ),
#     params=au.CommonAppCallParams(
#         sender=axel.address,
#         signer=axel.signer,
#         box_references=[axel.public_key, b"q3_string" + axel.public_key]
#     ),
#     send_params=au.SendParams(populate_app_call_resources=True)
# )

# --------------------------------------------------------------------- APPEL DE LA FONCTION update_box ---------------------------------------------------------------------
    # @arc4.abimethod()
    # def update_box(self, value: arc4.String) -> arc4.String:
    #     assert Txn.sender in self.q4_string
    #     assert Txn.sender not in self.q4
    #     self.q4[Txn.sender] = arc4.Bool(True)
    #     self.q4_string[Txn.sender] = value
    #     return self.q4_string[Txn.sender]

# result=eval.send.update_box(
#     cl.UpdateBoxArgs(
#         value="TEST"
#     ),
#     params=au.CommonAppCallParams(
#         sender=axel.address,
#         signer=axel.signer,
#         box_references=[axel.public_key, b"q4_string" + axel.public_key]
#     ),
#     send_params=au.SendParams(populate_app_call_resources=True)
# )

# --------------------------------------------------------------------- Affichage des points obtenus ---------------------------------------------------------------------

def box(evalId, box_name):
    return algorand.app.get_box_value(evalId, box_name)

score = 1
scoreResult = {}

try :
    #boucle for pour les 4 premières fonctions
    for i in range(1, 5):
        box_name = f"q{i}".encode() + axel.public_key
        if box(evalId, box_name) == True:
            score += 1
    scoreResult["RESULTAT"] = score
    print(scoreResult)
except sdk.error.AlgodHTTPError as e:
    print(e)
    scoreResult["RESULTAT"] = 0