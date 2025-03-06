import algokit_utils as au
import algosdk as sdk
from utils import (
    account_creation,
    display_info,
)

# Choisir le réseau localnet
algorand = au.AlgorandClient.from_environment()

# Verifier que le réseau est correctement initialisé
algod_client = algorand.client.algod
indexer_client = algorand.client.indexer

print(algod_client.block_info(0))
print(indexer_client.health())

# Création des comptes pour Alice et Bob
alice = account_creation(algorand, "ALICE", au.AlgoAmount(algo=10_000))
bob = account_creation(algorand, "BOB", au.AlgoAmount(algo=100))

# accès à la mémoire du compte
sdk.mnemonic.from_private_key(alice.private_key)

# Création d'un payment d'alice vers Bob de 1 Algo
pay_txn_alice = algorand.create_transaction.payment(
    au.PaymentParams(
        sender=alice.address,
        receiver=bob.address,
        amount=au.AlgoAmount(algo=1)
))

# Signature de la transaction pour Alice
pay_txn_alice_signed = pay_txn_alice.sign(
    alice.private_key
)

# Envoi de la transaction d'Alice vers Bob
tx_id_alice = algorand.client.algod.send_transaction(
    pay_txn_alice_signed
)

res_alice = sdk.transaction.wait_for_confirmation(
    algod_client,
    tx_id_alice
)

                        # --------------------------------------------------------------------- #

# Création d'un payment de Bob vers Alice de 1 Algo
pay_txn_bob = algorand.create_transaction.payment(
    au.PaymentParams(
        sender=bob.address,
        receiver=alice.address,
        amount=au.AlgoAmount(algo=1)
))

# Signature de la transaction pour Bob
pay_txn_bob_signed = pay_txn_bob.sign(
    bob.private_key
)

# Envoi de la transaction de Bob vers Alice
tx_id_bob = algorand.client.algod.send_transaction(
    pay_txn_bob_signed
)

res_bob = sdk.transaction.wait_for_confirmation(
    algod_client,
    tx_id_bob
)

# Afficher les résultats
print(res_alice)
print(res_bob)