from banking_system import BankingSystem

class BankingSystemImpl(BankingSystem):
    """
    Banking system implementation

    Attributes
    ----------
    accounts : dict
        Stores accounts and a record of their balance at given timestamps 
    """

    def __init__(self):
        super(BankingSystem, self).__init__
        self.accounts = {} # account_id: {timestamp : balance}

    def create_account(self, timestamp: int, account_id: str) -> bool:
        if account_id in self.accounts: # Account already exists
            return False
        else:
            self.accounts[account_id] = {timestamp: 0}
            return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        if account_id not in self.accounts.keys(): # Account already exists
            return None
        else:
            # Get balance from most recent timestamp
            last_key = list(self.accounts[account_id].keys())[-1]
            last_balance = self.accounts[account_id][last_key]

            # Update balance with deposit amount at current timestamp
            new_balance = last_balance + amount
            self.accounts[account_id].update({timestamp: new_balance})
            return new_balance
    
    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None:
        if source_account_id == target_account_id: # Account ids are the same
            return None
        
        if source_account_id not in self.accounts.keys(): # Source account doesn't exist
            return None
        
        if target_account_id not in self.accounts.keys(): # Target account doesn't exist
            return None
        
        # Get most recent balance for source and target accounts 
        last_source_key = list(self.accounts[source_account_id].keys())[-1]
        last_source_balance = self.accounts[source_account_id][last_source_key]
        if last_source_balance < amount: # Balance less than requested transfer amount
            return None
        
        last_target_key = list(self.accounts[target_account_id].keys())[-1]
        last_target_balance = self.accounts[target_account_id][last_target_key]

        # Update source account balance
        source_balance = last_source_balance - amount
        self.accounts[source_account_id].update({timestamp: source_balance})
        
        # Update target account balance
        target_balance = last_target_balance + amount
        self.accounts[target_account_id].update({timestamp: target_balance})

        return source_balance
