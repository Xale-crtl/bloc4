# 🚀 Algorand Smart Contract TP

## 📌 Objective

This TP will guide you through interacting with **Algorand Smart Contract Boxes**.
You will implement missing functionalities to:

- **Register a user**
- **Fund a user account**
- **Add or update assets**
- **Buy assets**

You will fill in the missing parts (`TODO` comments) to complete the transactions.

---

## 🛠 Setup Instructions

### 1️⃣ Prerequisites

Get all file from [https://github.com/SudoWeezy/bloc4/game](https://github.com/SudoWeezy/bloc4/game)

#### open the game repository in you vs code browser

```bash
code game
```

---

## 📝 Tasks

Complete the missing parts marked with **`TODO`**.

### ✅ Task 1: Implement `register()`

```mermaid
graph TD
sequenceDiagram
    participant User
    participant Client
    participant AlgorandNode
    participant AppContract

    rect rgba(200, 200, 255, 0.2)
    Note over User, AlgorandNode: User Registration Process

    User->>Client: Call register(user, value)
    Client->>AlgorandNode: Fetch box value (check if user exists)
    AlgorandNode-->>Client: Return box value or error

    alt User already registered
        Client-->>User: Return existing registration
    else User not found
        Client->>AlgorandNode: Prepare new box entry (store user data)
        AlgorandNode-->>Client: Confirm box storage
    end

    rect rgba(200, 255, 200, 0.2)
    Note over Client, AlgorandNode: Funding and Registration

    Client->>AlgorandNode: Check application balance
    AlgorandNode-->>Client: Return balance info

    alt Insufficient balance
        Client->>AlgorandNode: Create funding transaction
        AlgorandNode-->>Client: Confirm funding
    end

    Client->>AlgorandNode: Send registration app call
    AlgorandNode->>AppContract: Execute registration logic
    AppContract-->>AlgorandNode: Confirm transaction

    AlgorandNode-->>Client: Return registration result
    Client-->>User: Registration complete
    end
   end
```

- **Find `box_key`**.
- **Calculate `min_balance`** using `get_min_balance_required()`.
- **Add a payment transaction to cover minimum balance**.
- **Send an app call transaction to register the user**.

#### Example Hint:

```python
args = cl.RegisterArgs(name=value)
param = au.CommonAppCallParams(
    box_references=[box_key],
    sender=user.address,
    signer=user.signer
)
composer.add_payment(...)  # Implement this
composer.add_app_call_method_call(ac.params.register(...))  # Implement this
```

---

### ✅ Task 2: Implement `fund_account()`

```mermaid
sequenceDiagram
    participant User
    participant Client
    participant AlgorandNode
    participant AppContract

    rect rgba(200, 200, 255, 0.2)
    Note over User, AlgorandNode: Funding an Account

    User->>Client: Call fund_account(user, amount)
    Client->>AlgorandNode: Check if user is already registered
    AlgorandNode-->>Client: Return balance_before

    alt Account already funded
        Client-->>User: Return existing balance
    else
        rect rgba(200, 255, 200, 0.2)
        Note over Client, AlgorandNode: Creating payment transaction
        Client->>AlgorandNode: Create Algo payment transaction
        AlgorandNode-->>Client: Transaction object created
        end

        rect rgba(255, 200, 200, 0.2)
        Note over Client, AppContract: Funding the account via smart contract
        Client->>AppContract: Call fund_account(args, params)
        AppContract->>AlgorandNode: Execute funding logic
        AlgorandNode-->>AppContract: Confirm transaction execution
        AppContract-->>Client: Return updated balance
        end

        Client-->>User: Return new balance
    end
  end
```

- **Find correct arguments (`args`) and parameters (`param`)**.
- **Send a funding transaction to increase the user’s balance**.

#### Example Hint:

```python
args = cl.FundAccountArgs(...)  # Implement this
param = au.CommonAppCallParams(...)  # Implement this
balance_returned = ac.send.fund_account(args, param).abi_return
```

---

### ✅ Task 3: Implement `add_or_update_asset()`

```mermaid
sequenceDiagram
    participant Admin
    participant Client
    participant AlgorandNode
    participant AppContract

    rect rgba(200, 200, 255, 0.2)
    Note over Admin, AlgorandNode: Asset Registration / Update

    Admin->>Client: Call add_or_update_asset(ac, asset)
    Client->>AlgorandNode: Check if asset exists (fetch box)
    AlgorandNode-->>Client: Return asset data or error

    alt Asset already registered
        Client-->>Admin: Return existing asset details
    else
        rect rgba(200, 255, 200, 0.2)
        Note over Client, AppContract: Adding or updating asset
        Client->>AppContract: Call admin_upsert_asset(asset)
        AppContract->>AlgorandNode: Execute update logic
        AlgorandNode-->>AppContract: Confirm transaction execution
        AppContract-->>Client: Confirm asset update
        end

        Client-->>Admin: Return updated asset details
    end
end
```

- **Store asset data on the blockchain**.
- **Call `ac.send.admin_upsert_asset()` to update the asset**.

#### Example Hint:

```python
ac.send.admin_upsert_asset(
    cl.AdminUpsertAssetArgs(
    ),
    au.CommonAppCallParams(
    )
)
```

---

### ✅ Task 4: Implement `buy_asset()`

```mermaid
sequenceDiagram
    participant User
    participant Client
    participant AlgorandNode
    participant AppContract

    rect rgba(200, 200, 255, 0.2)
    Note over User, AlgorandNode: Buying an Asset

    User->>Client: Call buy_asset(ac, asset_name, quantity, user)
    Client->>AlgorandNode: Fetch asset details (asset box)
    AlgorandNode-->>Client: Return asset price

    Client->>AlgorandNode: Fetch user balance
    AlgorandNode-->>Client: Return user balance

    alt Insufficient balance
        Client-->>User: Error: Insufficient funds
    else
        Client->>AlgorandNode: Compute user asset box name
        AlgorandNode-->>Client: Check if user already owns asset

        alt User owns asset
            AlgorandNode-->>Client: Return existing quantity
        else
            AlgorandNode-->>Client: Quantity set to 0
        end

        rect rgba(200, 255, 200, 0.2)
        Note over Client, AppContract: Processing asset purchase
        Client->>AppContract: Call buy_asset(asset_id, quantity)
        AppContract->>AlgorandNode: Execute purchase transaction
        AlgorandNode-->>AppContract: Confirm execution
        AppContract-->>Client: Confirm asset purchase
        end

        Client-->>User: Asset purchase successful
    end
end
```

- **Ensure the user has enough balance before purchase**.
- **Call `ac.send.buy_asset()` to complete the transaction**.

#### Example Hint:

```python
ac.send.buy_asset(
    cl.BuyAssetArgs(
    ),
    au.CommonAppCallParams(
    )
)
```

---

## ⚠️ Debugging Tips

- Restart **Algorand Sandbox**:

  ```bash
  algokit localnet reset 
  ```

- Open **Lora the Explorer**:`

  ```bash
  algokit explore
  ```

- Print variable values to debug missing data.

---

## 📩 Submission

Once you complete all tasks:
Make sure your script runs without errors.
```bash
  python game.py
```

🎯 **Happy coding!** 🚀