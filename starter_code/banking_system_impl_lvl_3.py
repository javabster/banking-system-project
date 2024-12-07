from banking_system import BankingSystem
import math

class BankingSystemImpl(BankingSystem):

    def __init__(self):
        super(BankingSystem, self).__init__
        self.accounts = {}
        self.total_spend = {}
        self.payment_history = {} # payment_id : (timestamp, account_id)

        # self.accounts = {
        # 1: {time1: $0, time2: $100},
        #2: {time1: $0, time2: $100}
        #}

        # self.total_spend = {
        # 1: $20,
        #2: $120
        #}

    def create_account(self, timestamp: int, account_id: str) -> bool:
        if account_id in self.accounts: #account already exists
            return False
        else:
            self.accounts[account_id] = {timestamp: 0}
            self.total_spend[account_id] = 0
            return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        if account_id not in self.accounts.keys(): #account already exists
            return None
        
        #process pending cashback if this timestamp matches
        if timestamp in self.accounts[account_id]:
            amount += self.accounts[account_id][timestamp]

        self.accounts[account_id].update({timestamp: amount})
        return self._get_latest_balance(account_id, timestamp)
    
    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None:
        if source_account_id == target_account_id:
            return None
        
        if source_account_id not in self.accounts.keys():
            return None
        
        if target_account_id not in self.accounts.keys():
            return None
        
        last_source_balance = self._get_latest_balance(source_account_id, timestamp)
        if last_source_balance < amount:
            return None
        
        last_target_balance = self._get_latest_balance(target_account_id, timestamp)

        # update source account balance
        self.accounts[source_account_id].update({timestamp: -amount})
        
        # update target account balance
        self.accounts[target_account_id].update({timestamp: amount})

        # update spending record of source account
        self.total_spend[source_account_id] += amount

        return self._get_latest_balance(source_account_id, timestamp)
    
    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        # Sort in order of total transaction amount, or alphabetical of account_id for tie breaker
        sorted_spending = sorted(
            self.total_spend.items(),
            key=lambda item: (-item[1], item[0])
        )

        if len(self.total_spend) < n:
            return [f"{key}({val})" for key, val in sorted_spending]

        return [f"{key}({val})" for key, val in sorted_spending[:n]]
    
    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
    
        if account_id not in self.accounts.keys():
            return None
        
        # Insufficient funds
        account_balance = self._get_latest_balance(account_id, timestamp)
        if account_balance < amount:
            return None
        
        # withdraw amount from account
        self.accounts[account_id][timestamp] = self.accounts[account_id].get(timestamp, 0) - amount

        # Update total spend for account
        self.total_spend[account_id] += amount

        # Process cash back
        cashback = math.floor(0.02*amount)
        cashback_timestamp = timestamp + 86400000
        if cashback > 0:
            self.accounts[account_id].setdefault(cashback_timestamp, 0)
            self.accounts[account_id][cashback_timestamp] += cashback
        # update payment history
        payment_id = f"payment{len(self.payment_history) + 1}"
        self.payment_history.update({payment_id : (timestamp, account_id)})

        return payment_id
    
    def get_payment_status(self, timestamp: int, account_id: str, payment: str) -> str | None:
        # Account ID doesnt exist
        if account_id not in self.accounts.keys():
            return None
        
        # check if payment exists for specified account
        if payment not in self.payment_history or self.payment_history[payment][1] != account_id:
            return None
        
        # check payment status
        if timestamp < (self.payment_history[payment][0] + 86400000):
            return "IN_PROGRESS"
        else:
            return "CASHBACK_RECEIVED"

    def _get_latest_balance(self, account_id: str, timestamp : int):
        account = self.accounts[account_id]
        sorted_timestamps = sorted(account.keys())
        while sorted_timestamps:
            if sorted_timestamps[-1] <= timestamp:
                break
            sorted_timestamps.pop(-1)

        last_balance = sum(self.accounts[account_id][t] for t in sorted_timestamps)
        return last_balance