from banking_system import BankingSystem

class BankingSystemImpl(BankingSystem):

    def __init__(self):
        super(BankingSystem, self).__init__
        self.accounts = {}
        self.total_spend = {}

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
        else:
            last_key = list(self.accounts[account_id].keys())[-1]
            last_balance = self.accounts[account_id][last_key]
            new_balance = last_balance + amount
            self.accounts[account_id].update({timestamp: new_balance})
            return new_balance
    
    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None:
        if source_account_id == target_account_id:
            return None
        
        if source_account_id not in self.accounts.keys():
            return None
        
        if target_account_id not in self.accounts.keys():
            return None
        
        last_source_key = list(self.accounts[source_account_id].keys())[-1]
        last_source_balance = self.accounts[source_account_id][last_source_key]
        if last_source_balance < amount:
            return None
        
        last_target_key = list(self.accounts[target_account_id].keys())[-1]
        last_target_balance = self.accounts[target_account_id][last_target_key]

        # update source account balance
        source_balance = last_source_balance - amount
        self.accounts[source_account_id].update({timestamp: source_balance})
        
        # update target account balance
        target_balance = last_target_balance + amount
        self.accounts[target_account_id].update({timestamp: target_balance})

        # update spending record of source account
        self.total_spend[source_account_id] += amount

        return source_balance
    
    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        # Sort in order of total transaction amount, or alphabetical of account_id for tie breaker
        sorted_spending = sorted(
            self.total_spend.items(),
            key=lambda item: (-item[1], item[0])
        )

        if len(self.total_spend) < n:
            return [f"{key}({val})" for key, val in sorted_spending]

        return [f"{key}({val})" for key, val in sorted_spending[:n]]