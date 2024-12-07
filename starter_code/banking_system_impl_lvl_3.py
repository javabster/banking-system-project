from banking_system import BankingSystem
import math

class BankingSystemImpl(BankingSystem):
    """
    Banking system implementation

    Attributes
    ----------
    accounts : dict
        Stores accounts and a record of their balance at given timestamps
    total_spend: dict
        Stores information about the total spend to date for each account
    payment_history: dict
        Stores a record of every payment for each account 
    """

    def __init__(self):
        super(BankingSystem, self).__init__
        self.accounts = {} # account_id : {timestamp : transaction_amount}
        self.total_spend = {} # account_id : total_spent
        self.payment_history = {} # payment_id : (timestamp, account_id)

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
        
        #process pending cashback if this timestamp matches
        if timestamp in self.accounts[account_id]:
            amount += self.accounts[account_id][timestamp]

        self.accounts[account_id].update({timestamp: amount})
        return self._get_latest_balance(account_id, timestamp)
    
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
    
    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
        '''
        withdraws the specified amount of money from the specified account, providing a 2% cashback of the withdrawn amount to the account after 24 hours. 

        Parameters:
        ----------
        timestamp (int): time pay is occuring
        account_id (str): unique account identifier
        amount (int): the amount to be taken out of the account

        Returns:
        ---------
        (str): payment(n) where n is the number of payments the account has made 

        '''
    
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
        '''
        returns the status of the payment transaction 

        Parameters:
        ----------
        timestamp (int): time pay is occuring
        account_id (str): unique account identifier
        payment (str): the payment number you want to check status of (example: payment3)

        Returns:
        ---------
        (str): "IN_PROGRESS" if the cashback has not been received
        (str): "CASHBACK_RECEIVED" if the cashback has been received 

        '''
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
        '''
        returns the total amount of moeny in the account account_id at given timestamp time_at

        Parameters:
        ----------
        timestamp (int): the timestamp of where you want to check balance
        account_id (str): unique account identifier

        Returns:
        ---------
        (int): total money in the account_id at timestamp
        '''
        account = self.accounts[account_id]
        sorted_timestamps = sorted(account.keys())
        while sorted_timestamps:
            if sorted_timestamps[-1] <= timestamp:
                break
            sorted_timestamps.pop(-1)

        last_balance = sum(self.accounts[account_id][t] for t in sorted_timestamps)
        return last_balance