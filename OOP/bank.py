class BankAccount:
    def __init__(self, owner, initial_balance):
        self.__owner = owner
        self.__balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"{self.__owner} deposited ${amount}. New balance: ${self.__balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.__balance:
            self.__balance -= amount
            print(f"{self.__owner} withdrew ${amount}. New balance: ${self.__balance}")
        else:
            print("Withdrawal failed. Insufficient funds or invalid amount.")

    def check_balance(self):
        print(f"{self.__owner}'s balance: ${self.__balance}")

    # 供子類別存取
    def _get_balance(self):
        return self.__balance

    def _set_balance(self, amount):
        self.__balance = amount


# 子類別一：儲蓄帳戶，月底按利率加息
class SavingsAccount(BankAccount):
    def __init__(self, owner, initial_balance, interest_rate):
        super().__init__(owner, initial_balance)
        self.interest_rate = interest_rate  # e.g. 0.02 = 2%

    def apply_interest(self):
        balance = self._get_balance()
        interest = balance * self.interest_rate
        self.deposit(interest)
        print(f"Applied interest ${interest:.2f} at rate {self.interest_rate*100:.1f}%.")


# 子類別二：支票帳戶，提款時若不足額允許手續費透支
class CheckingAccount(BankAccount):
    def __init__(self, owner, initial_balance, overdraft_fee):
        super().__init__(owner, initial_balance)
        self.overdraft_fee = overdraft_fee  # e.g. $35

    # 覆寫 withdraw：允許透支但收手續費
    def withdraw(self, amount):
        balance = self._get_balance()
        if amount <= balance:
            super().withdraw(amount)
        else:
            # 允許透支
            new_balance = balance - amount - self.overdraft_fee
            self._set_balance(new_balance)
            print(f"{self._get_owner()} overdrew ${amount} (fee ${self.overdraft_fee}). New balance: ${new_balance}")

    # 幫助子類別存取 owner
    def _get_owner(self):
        # 反射存取 private 欄位
        return self._BankAccount__owner


if __name__ == "__main__":
    # 建立各種帳戶
    acct_base     = BankAccount("Alice",   500.0)
    acct_savings  = SavingsAccount("Bob",   1000.0, 0.03)
    acct_checking= CheckingAccount("Carol",  200.0,  35.0)

    # 把它們放在一個 list，示範多型
    accounts = [acct_base, acct_savings, acct_checking]

    for acc in accounts:
        acc.deposit(100)       # 相同介面，不同類別都可呼叫
        acc.withdraw(50)
        acc.check_balance()
        print("---")

    # 特殊操作：只對儲蓄帳戶加息
    print("Applying interest to savings accounts:")
    for acc in accounts:
        if isinstance(acc, SavingsAccount):
            acc.apply_interest()
            acc.check_balance()
