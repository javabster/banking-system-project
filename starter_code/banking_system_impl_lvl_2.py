from banking_system import BankingSystem

class BankingSystemImpl(BankingSystem):
    """
    Banking system implementation

    Attributes
    ----------
    accounts : dict
        Stores accounts and a record of their balance at given timestamps
    total_spend: dict
        Stores information about the total spend to date for each account
    """

    def __init__(self):
        super(BankingSystem, self).__init__
        self.accounts = {} # account_id : {timestamp : transaction_amount}
        self.total_spend = {} # account_id : total_spent

    def create_account(self, timestamp: int, account_id: str) -> bool:
        '''
        create_account function creates a new account if the account id dooes not already exist

        Parameters: 
        ----------
        timestamp (int): time creation is occurring
        account_id (str): unique account identifier
        
        Returns:
        --------
        True (boolean): account is created
        False(boolean): account is not created because it already exists
        '''
        if account_id in self.accounts: #account already exists
            return False
        else:
            self.accounts[account_id] = {timestamp: 0}
            self.total_spend[account_id] = 0
            return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        '''
        deposit function adds given amount of money into specified account and returns the new balance

        Parameters:
        ----------
        timestamp (int): time of transaction
        account_id (str): unique account identifier
        amount (int): amount of money to add to account

        Returns:
        -------
        (int): updated balance after deposit
        
        '''
        if account_id not in self.accounts.keys(): #account already exists
            return None
        else:
            last_key = list(self.accounts[account_id].keys())[-1]
            last_balance = self.accounts[account_id][last_key]
            new_balance = last_balance + amount
            self.accounts[account_id].update({timestamp: new_balance})
            return new_balance
    
    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None:
        '''
        transfer function moves amount from source_account_id and deposits it into target_account_id

        Parameters:
        ----------
        timestamp (int): time of transaction
        source_account_id (): unique identifier for account that funds are removed from
        target_account_id (): unique identifier for the account that receives funds
        amount (int): amount of money to be transferred

        Returns:
        -------
        (int) new balance of the source_account_id 
        '''
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
        '''
        top_spenders function returns the identifiers of the top n accounts with the highest
        outgoing transactions (total amount of money either transferred out of or paid/withdrawn)
        
        Parameters:
        ----------
        timestamp (int): time top_spenders is accessed
        n (int): the number of accounts you want returned

        Returns:
        --------
        (list): [account_id_1(total_outgoing),account_id_n(total_outgoing)]
        '''
        # Sort in order of total transaction amount, or alphabetical of account_id for tie breaker
        sorted_spending = sorted(
            self.total_spend.items(),
            key=lambda item: (-item[1], item[0])
        )

        if len(self.total_spend) < n:
            return [f"{key}({val})" for key, val in sorted_spending]

        return [f"{key}({val})" for key, val in sorted_spending[:n]]