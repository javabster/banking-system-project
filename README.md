# Simplified Banking System

This project is a simplified implementation of a banking system, designed and developed as part of the **CHEM 274B** final project. The system progressively incorporates features to simulate real-world banking operations.

Key features include:
- Account creation and basic transactions.
- Ranking accounts based on activity.
- Scheduling payments with cashback.
- Merging accounts while preserving transaction histories.

### Authors

This project was collaboratively developed by the following contributors (ordered alphabetically by last name):
- **Yishak Bililign: ysb@berkeley.edu**
- **Suki Cai: yufeicai@berkeley.edu**
- **Julian Dolan: Juliandolan@berkeley.edu**
- **Abby Mitchell: abby.mitchell@berkeley.edu**

---

## Implementation Overview

#### Level 1: **Basic Banking Operations**
**Goal:** Implement foundational banking operations like account creation, deposits, and transfers.

- **Design:** We used a dictionary to store account details with account IDs as keys, ensuring O(1) time complexity for operations.
- **Challenges:** Handling edge cases like duplicate accounts, invalid transfers, and insufficient funds.
- **Key Methods:**
  - `create_account(timestamp, account_id)`
  - `deposit(timestamp, account_id, amount)`
  - `transfer(timestamp, source_account_id, target_account_id, amount)`

<br>

#### Level 2: **Ranking Accounts by Outgoing Transactions**
**Goal:** Identify the top spenders by tracking outgoing transaction totals.

- **Design:** Added a data structure to store transaction histories and maintain a leaderboard of accounts based on outgoing transactions.
- **Challenges:** Efficiently updating rankings in real-time, ensuring correct handling of ties.
- **Key Methods:**
  - `top_spenders(timestamp, n)`: Sort accounts by outgoing amounts and tie-break alphabetically.

<br>

#### Level 3: **Payments with Cashback**
**Goal:** Allow payments with a cashback mechanism and track payment statuses.

- **Design:** Extended account data to include pending transactions and timestamps for cashback. Used a queue to process cashback transactions efficiently.
- **Challenges:** Synchronizing cashback processing with existing operations and ensuring correct status tracking.
- **Key Methods:**
  - `pay(timestamp, account_id, amount)`
  - `get_payment_status(timestamp, account_id, payment)`

<br>

#### Level 4: **Account Merging**
**Goal:** Merge accounts while preserving balances and transaction histories.

- **Design:** Introduced functionality to merge transaction logs and update all references to the merged accounts. Implemented inheritance of balances and histories to the primary account.
- **Challenges:** Ensuring data integrity during merges, handling pending cashback, and removing redundant accounts.
- **Key Methods:**
  - `merge_accounts(timestamp, account_id_1, account_id_2)`
  - `get_balance(timestamp, account_id, time_at)`
<br>
