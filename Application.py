from MySQL_Connector_v3 import close_connection, create_connection, read_query, write_query
import time
import sys
from loggers import logger




''' Section 1: Menus'''

'''Main Menu for Employee and Customers'''

def main_menu(self=None):
    print('Welcome to Bank of Python \n')
    print('\n Main Menu \n'
        '\n (1) New or Existing Customer'
        '\n (2) New or Existing Employee')
    try:
        person=int(input('Please enter number 1 or 2 \n'))
        if person==1:   
            selection=int(input('\n Please select the following number options:' 
                                '\n (1) New Customer Registration' 
                                '\n (2) Account Login\n'))     
            if selection==1:
                print('\n Great! Let\'s begin creating an Account...\n')
                customer_registration()
            elif selection==2:
                print('\n Great! let\'s begin logging into an Account...\n')
                customer_login()   
            else:
                print('Please try again.')
                main_menu()
                
        elif person==2:
            selection=int(input('\n Please select the following number options: ' 
                                '\n (1) New Employee ' 
                                '\n (2) Current Employee \n'))  
            if selection==1:
                print('Welcome to the team!')
                employee_registration()
            elif selection==2:
                print('Welcome back!')
                employee_login(self)
            else:
                print('Please try again.')
                main_menu()

    except ValueError as err:
        print(f"Error: '{err}'")
        logger.error(
            f'Input of type string entered in customer menu screen.\n')
        main_menu()

            
def exit_menu():
        print('\nThank you, have a wonderful day!')
        sys.exit()

'''Menus for Customers'''

def customer_menu(self):
    print('\n What would you like to do?\n'
            '(1) View Account Info\n'
            '(2) Deposit\n'
            '(3) Withdraw\n'
            '(4) Bank Services and Products\n'
            '(5) Check Balance\n'
            '(6) Return to Main Menu \n'
            '(7) Exit \n')
    try:
        choice=int(input('\nPlease Enter Number '))
        if choice==1:
            self.account_details()
        elif choice==2:
            self.deposit()
        elif choice==3:
            self.withdraw()
        elif choice==4:
            Services.view_services(self,self.balance,self.type,self.accid)
        elif choice==5:
            self.check_balance()
        elif choice==6:
            main_menu()
        elif choice==7:
            exit_menu()
        else:
            print('Please try again.\n')
            customer_menu(self)

    except ValueError as err:
        print(f"Error: '{err}'")
        logger.error(
            f'Input of type string entered in customer menu screen.\n')
        customer_menu(self)
        

def customer_registration():
    '''Function collects user input to create customer profile
        and instantiate Savings or Checking object.
        
        Customer profile and Object information are then stored in 
        two seperate MySQL tables: Customers, Accounts.
        
        Object is passed into Customer_Menu Function for further operations'''
        
    try:
        print('\n Select Account Type:\n'
            '(1) Checking Account \n'
            '(2) Savings Account \n')
        selection=int(input('Please enter number 1 or 2 \n'))
        fullname=input('Enter Full Name: ')
        ss=int(input('Enter Social Security #: '))
        password=input('Enter password: ')

        con=create_connection()
        cust_query=f"INSERT INTO Customers (Name,Password,Social_Security) VALUES('{fullname}','{password}',{ss})"
        write_query(con,cust_query)
        cust_id_query=f"SELECT Cust_ID FROM Customers WHERE (Name='{fullname}') AND (Social_Security={ss})"
        cust_id=read_query(con,cust_id_query,True)
        
        if selection==1:
            acc_type='Checking'
            balance=0.00
            cust_query=f"INSERT INTO Accounts (Cust_ID,Account_Type,Balance) VALUES({cust_id[0]},'{acc_type}',{balance})"
            write_query(con,cust_query)
            acc_id_query=f"SELECT Acc_ID FROM Accounts WHERE (Cust_ID={cust_id[0]});"
            acc_id=read_query(con,acc_id_query,True)
            close_connection(con)
            account=Checking(fullname,ss,password,
                            cust_id,balance,acc_id[0])
            customer_menu(account) 
        elif selection==2:
            acc_type='Savings'
            balance=0.00
            cust_query=f"INSERT INTO Accounts (Cust_ID,Account_Type,Balance) VALUES({cust_id[0]},'{acc_type}',{balance})"
            write_query(con,cust_query)
            acc_id_query=f"SELECT Acc_ID FROM Accounts WHERE (Cust_ID={cust_id[0]});"
            acc_id=read_query(con,acc_id_query,True)
            close_connection(con)
            account=Savings(fullname,ss,password,
                            cust_id,balance,acc_id[0])
            customer_menu(account)

    except ValueError as err:
        print(f"Error: '{err}'")
        logger.error(
            f'Input of type string entered in customer registration screen')
        print('Returning to Main Menu\n')
        main_menu()


def customer_login():
    '''Function retrieves information from MySQL based on
    collected user input. Then a Savings or Checking object is instantiated
    and passed into Customer_Menu Function for further operations'''
        
    try:
        cust_id=int(input('Please enter your Customer ID: '))
        password=input('Enter password: ')
        con=create_connection()
        login_query=f"SELECT Cust_ID, Password FROM Customers WHERE (Cust_ID={cust_id}) AND (Password='{password}');"
        login=read_query(con,login_query,True)

        if login is None:
            print('\nCustomer ID or Password Incorrect')
            print('Returning to Main Menu\n')
            main_menu()

        elif login[0]==cust_id and login[1]==password:
            print('\n You have Successfully Logged In!')
            acc_id=int(input('Please enter your Account ID: '))
            account_query=f"SELECT * FROM Accounts JOIN Customers ON Customers.Cust_ID=Accounts.Cust_ID WHERE (Customers.Cust_ID={cust_id}) AND (Accounts.Acc_ID={acc_id});"
            account=read_query(con,account_query,True)
            close_connection(con)

            if account[2]=='Savings':
                account=Savings(account[9],account[11],account[10],
                                account[1],account[3],account[0],logged=True)
                customer_menu(account)
            elif account[2]=='Checking':
                account=Checking(account[9],account[11],account[10],
                                account[1],account[3],account[0],logged=True)
                customer_menu(account)
        else:
            print('Customer ID or Password Incorrect\n')
            print('Returning to Main Menu')
            time.sleep(1.5)
            main_menu()


    except ValueError as err:
        print(f"Error: '{err}'")
        logger.error(
            f'Input of type string entered in customer login screen\n')
        customer_login()


'''Menu for Employees'''

def employee_menu(self):
    print('\n What would you like to do?\n'
            '(1) View Profile \n'
            '(2) Update Profile\n'
            '(3) Return to Main Menu\n'
            '(4) Exit \n')

    try:
        choice=int(input('Please Select Number:'))
        if choice==1:
            self.view_profile()
        elif choice==2:
            self.update_profile()
        elif choice==3:
            main_menu(self)
        elif choice==4:
            exit_menu()  

    except ValueError as err:
        print(f"Error: '{err}'")
        logger.error(
            f'Input of type string entered in employee_menu screen\n')
        employee_menu(self)

def employee_registration():
    fullname=input('Enter Full Name: ')
    email=input('Enter Email: ')
    password=input('Enter password: ')
    employee=Employee(fullname,email,password)
    employee_menu(employee)

def employee_login(self):
    eid=input('Enter Employee ID: ')
    password=input('Enter password: ')
    employee=Employee(self.fullname,self.email,password,eid)
    employee_menu(employee)






'''Section 2: Classes'''


class Bank:
    bankname='Bank of Python'
    branch='Los Angeles'


class Employee(Bank):
    accum=1
    def __init__(self,fullname,email,password,eid=None):
        self.branch=Bank.branch
        self.bankname=Bank.bankname
        self.fullname=fullname
        self.email=email
        self.password=password
        if eid==None:
            self.eid='EID'+str(Employee.accum)
            Employee.accum+=1
        elif eid!=None:
            self.eid=eid

    def view_profile(self):
        print(f'Name: {self.fullname}')
        print(f'Employee ID: {self.eid}')
        print(f'Email: {self.email}')
        print(f'Branch Location: {self.branch}')
        employee_menu(self)

    def update_profile(self):
        self.fullname=input('Please Update Name:')
        self.email=input('Please Update Email: ')
        self.branch=input('Please Update Branch Location: ')
        employee_menu(self)



class Services:

    @classmethod
    def cd(cls,object,balance,accid,amount):
        con=create_connection()
        query=f"UPDATE Accounts SET CD={amount},Balance={balance} WHERE Acc_ID={accid}"
        write_query(con,query)
        close_connection(con)
        time.sleep(1.5)
        customer_menu(object)
    
    @classmethod
    def investment(cls,object,balance,accid,amount):
        con=create_connection()
        query=f"UPDATE Accounts SET Investment={amount},Balance={balance} WHERE Acc_ID={accid}"
        write_query(con,query)
        close_connection(con)
        time.sleep(1.5)
        customer_menu(object)

    @classmethod              
    def loan(cls,object,balance,accid):
        con=create_connection()
        query=f"UPDATE Accounts SET Approved_Loan={balance*0.15} WHERE Acc_ID={accid}"
        write_query(con,query)
        close_connection(con)
        time.sleep(1.5)
        customer_menu(object)

    @classmethod
    def credit_card(cls,object,balance,accid):
        con=create_connection()
        query=f"UPDATE Accounts SET Approved_Credit={balance*0.1} WHERE Acc_ID={accid}"
        write_query(con,query)
        close_connection(con)
        time.sleep(1.5)
        customer_menu(object)

    @classmethod
    def view_services(cls,object,balance,type,accid):
        print(f'\nFor {type} Account Type with')
        print(f'Balance of ${balance} \n')
        if type=='Checking':
            if balance<1000:
                print(f'Insufficient funds for Services, please raise Account Balance above $1000')
            elif balance>=1000 and balance<=9999:
                print('Services: \n' 
                    '(1) Credit Card  \n')
                choice=int(input('Please enter number: '))
                if choice==1:
                    print(f'Credit Card Approved. Monthly Credit Limit is ${balance*0.1}')
                    Services.credit_card(object,balance,accid)
                else:
                    print('''An issue occured. \n
                            Please call our customer support for further inquiry.''')

            elif balance>=10000:
                print('Services: \n' 
                    '(1) Credit Card  \n'
                    '(2) Loan \n'
                    '(3) Exit ')
                choice=int(input('Please enter number: '))
                if choice==1:
                    print(f'Credit Card Approved. Monthly Credit Limit is ${balance*0.1}')
                    Services.credit_card(object,balance,accid)
                elif choice==2:
                    amount=balance*0.15
                    print(f'Loan Details: Max Loan Amount is ${amount}. Six monthly payments of Principal')
                    print(f'and 4% Interest equals 6 installments of ${amount/6}')
                    print('Do you accept these conditions?\n(1) Yes \n(2) No')
                    choice=int(input('Please enter number: '))       
                    if choice==1:
                        print(f'Loan approved. Approved Loan is ${amount}')
                        Services.loan(object,balance,accid)
                    elif choice==2:
                        print(f'Please call our customer support for further inquiry.')
                
                    
        elif type=='Savings':
            if balance<1000:
                print(f'Insufficient funds for Services, please raise Account Balance above $1000')
            elif balance>=1000 and balance<=9999:
                print('Services: \n' 
                    '(1) Certificate of Deposits: Deposits will collect 3 percent interest, and will be unaccessible 6 months. \n(2) Exit \n')
                choice=int(input('Please Enter Number: '))
                if choice==1:
                    amount=int(input(f'Please enter amount to Deposit: '))
                    if balance>=amount:
                        object.balance-=amount
                        print(f'CD deposited. Account balance is now ${object.balance}')
                    else:
                        print(f'Insufficient funds, please fund Account Balance')
            elif balance>=10000:
                print('Services: \n' 
                    '(1) Certificate of Deposits:\n --CD will collect 3 percent interest, and will be unaccessible 6 months. \n'
                    '(2) Managed Investments: \n --Mininum investment is $10,000. Terms & conditions need to be signed first before proceeding \n'
                    '(3) Exit')
                choice=int(input('Please Enter Number: '))
                if choice==1:
                    amount=int(input(f'Please enter amount to Deposit: '))
                    if balance>=amount:
                        print(f'${amount} deposited into CD.Account balance is ${object.balance}')
                        object.balance-=amount
                        Services.cd(object,object.balance,accid,amount)
                    else:
                        print(f'Insufficient funds, please fund Account Balance')
                elif choice==2:
                    amount=int(input(f'Please enter amount to Invest: '))
                    if balance>=amount:
                        object.balance-=amount
                        print(f'${amount} Invested. Account balance is ${object.balance}')
                        Services.investment(object,object.balance,accid,amount)
                    else:
                        print(f'Insufficient funds, please fund Account Balance')
                else:
                    print(f'Please call our customer support for further inquiry.')
        time.sleep(1.5)
        customer_menu(object)
    



class Customer:
    def __init__(self,fullname,ss,password):
        self.fullname=fullname
        self.ss=ss
        self.password=password
    


class Account(Customer):

    def account_details(self):
        print(f'****\nCustomer Name: {self.fullname}')
        print(f'Account ID: {self.accid}')
        print(f'Account Type: {self.type}')
        print(f'Account Balance: ${self.balance} \n****')
        time.sleep(1.5)
        customer_menu(self)

    def check_balance(self):
        print(f'****\nYour current balance is ${self.balance}\n****')
        time.sleep(1.5)
        customer_menu(self)
        

    def deposit(self):
        print('\nTo Begin Depositing...\n')
        amount=int(input("Please enter amount to deposit: "))
        self.balance+=amount
        print(f'****\n${amount} Deposited')
        print(f'Current balance is ${self.balance}')

        con=create_connection()
        query=f"UPDATE Accounts SET Balance={self.balance} WHERE Acc_ID={self.accid}"
        write_query(con,query)
        close_connection(con)      

        

    def withdraw(self):
        print('\n To Begin Withdrawing...\n')
        amount=int(input("Please enter amount to Withdraw: \n"))
        if amount>self.balance:
            print('****\nInsufficient Funds')
            print(f'Current Account Balance is ${self.balance}\n****')
            amount=int(input("Please enter amount to Withdraw: \n"))
            if amount>self.balance:
                print('****\n Insufficient Funds')
                print(f'Returning to Main Menu\n****')
            else:
                self.balance-=amount
                print(f'****\n ${amount} Withdrawed')
                print(f'Current Account Balance is ${self.balance}\n****')
                con=create_connection()
                query=f"UPDATE Accounts SET Balance={self.balance} WHERE Acc_ID={self.accid}"
                write_query(con,query)
                close_connection(con)
        else:
            self.balance-=amount
            print(f'****\n ${amount} Withdrawed')
            print(f'Current Account Balance is ${self.balance}\n****')
            con=create_connection()
            query=f"UPDATE Accounts SET Balance={self.balance} WHERE Acc_ID={self.accid}"
            write_query(con,query)
            close_connection(con)
        time.sleep(1.5)
        customer_menu(self)


class Checking(Account):
    def __init__(self,fullname,ss,password,cust_id,balance,acc_id,type='Checking',logged=False):
        Customer.__init__(self,fullname,ss,password)
        self.balance=balance
        self.custid=cust_id
        self.accid=acc_id
        self.type=type
        self.logged=logged

        if not(self.logged):
            print(f'\n Thank you, you have successfully created an account. Your Account ID is {self.accid}\n')
        else:
            print(f'\n Thank you, you have successfully logged into account {self.accid}.\n')
        customer_menu(self)


class Savings(Account):
    def __init__(self,fullname,ss,password,cust_id,balance,acc_id,type='Savings',logged=False):
        super().__init__(fullname,ss,password)
        self.balance=balance
        self.cust_id=cust_id
        self.accid=acc_id
        self.type=type
        self.logged=logged

        if not(self.logged):
            print(f'\n Thank you, you have successfully created an account. Your Account ID is {self.accid}\n')
        else:
            print(f'\n Thank you, you have successfully logged into account {self.accid}.\n')
        customer_menu(self)





if __name__ == "__main__":
    main_menu()
