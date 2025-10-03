import asyncio
import time
from aptos_sdk.account import Account
from aptos_sdk.async_client import RestClient, FaucetClient
from aptos_sdk.bcs import Serializer
from aptos_sdk.transactions import (
    TransactionPayload,
    EntryFunction,
    TransactionArgument,
)

async def example_single_orderless():
    """Submit a single orderless transaction"""
    print("=== Single Orderless Transaction ===\n")
    
    client = RestClient("https://fullnode.devnet.aptoslabs.com/v1")
    faucet_client = FaucetClient("https://faucet.devnet.aptoslabs.com", client)
    
    sender = Account.generate()
    recipient = Account.generate()
    
    print(f"Sender: {sender.address()}")
    print(f"Recipient: {recipient.address()}")
    
    print("\nFunding sender...")
    await faucet_client.fund_account(sender.address(), 100_000_000)
    
    # Create transfer payload
    payload = TransactionPayload(EntryFunction.natural(
        "0x1::aptos_account",
        "transfer",
        [],
        [
            TransactionArgument(recipient.address(), Serializer.struct),
            TransactionArgument(1_000_000, Serializer.u64),
        ]
    ))

    nonce_orderless = 12345

    print("Submitting orderless transaction...")
    tx_hash = await client.submit_orderless_transaction(
        sender,
        payload,
        nonce=nonce_orderless,
        wait=True
    )
    
    print(f"✓ Transaction completed: {tx_hash}")
    
    balance = await client.account_balance(recipient.address())
    print(f"✓ Recipient balance: {balance} octas")
    
    await client.close()

if __name__ == "__main__":    
    try:
        asyncio.run(example_single_orderless())
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()