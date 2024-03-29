""" Term Project - PyBank
CSD 4523 - Python II
CSAM   Group 02   2022S
"""
from datetime import datetime
from random import randint

from db import agent, account, customer, movement
from model.movement import Movement

""" AGENT FUNCTIONS """


def search_customer(search_string, result):
    """ Search bank customers who match de provided search string.
        Return a list of customers who satisfy the search criteria. """
    customers_result = []
    result.set_code("99")
    agent.search_customer(search_string, customers_result, result)
    if result.code == "00":
        return customers_result
    else:
        return None


def search_account(search_string, result):
    """ Search bank accounts who match de provided search string.
        Return a list of accounts who satisfy the search criteria. """
    account_result = []
    result.set_code("99")
    agent.search_account(search_string, account_result, result)
    if result.code == "00":
        return account_result
    else:
        return None


def create_customer(new_customer, result):
    """ Create a new bank customer """
    new_customer.creation_date = datetime.now()
    agent.create_customer(new_customer, result)


def open_account(new_account, result):
    """ Create a new bank account """
    result.set_code("99")
    acc_number = generate_acc_num(new_account.acc_type_id, result)
    new_account.acc_number = acc_number
    # print(new_account)
    agent.open_account(new_account, result)


""" ACCOUNT FUNCTIONS"""


def get_new_acc_num(acc_type_id: int):
    acc_number = randint(10000000, 99999999)
    if acc_type_id == 1:
        acc_number = acc_number + 300000000
    elif acc_type_id == 2:
        acc_number = acc_number + 600000000
    elif acc_type_id == 3:
        acc_number = acc_number + 900000000
    else:
        acc_number = acc_number + 100000000

    return str(acc_number)


def generate_acc_num(acc_type_id: int, result):
    """ Create a random bank account number different to the existing ones """
    account_numbers = []
    result.set_code("99")
    account.view_acc_numbers(account_numbers, result)

    acc_number = get_new_acc_num(acc_type_id)
    while acc_number in account_numbers:
        acc_number = get_new_acc_num(acc_type_id)

    return acc_number


def view_account(acc_number, result):
    """ Search bank account based on an account number """
    account_movements = []
    result.set_code("99")
    account.view_account(acc_number, account_movements, result)
    if result.code == "00":
        return account_movements


def update_account(bank_account, result):
    """ Update bank account based on an account number """
    result.set_code("99")
    account.update_account(bank_account, result)
    if result.code == "00":
        print(bank_account)


def change_account_type(bank_account, result):
    """ Update bank account based on an account number """
    result.set_code("99")
    account.change_account_type(bank_account, result)
    if result.code == "00":
        print(bank_account)


def delete_account(active_agent, bank_account, result):
    """ Delete bank account """
    result.set_code("99")

    if bank_account.balance > 0:
        closing_movement = Movement(
            movement_id=0,
            source_account=bank_account.acc_number,
            destination_account="",
            amount=bank_account.balance,
            previous_balance=bank_account.balance,
            new_balance=0,
            movement_date=datetime.now(),
            transaction_id=6,
            agent_id=active_agent.username
        )

        bank_account.transfer_amount += closing_movement.amount
        bank_account.transfer_quantity = bank_account.transfer_quantity + 1
        bank_account.balance = closing_movement.new_balance
        movement.create_transaction(closing_movement, result)
        if result.code == "00":
            account.update_account(bank_account, result)
            delete_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            account.delete_account(bank_account, active_agent.username, delete_date, result)
            result.set_code("05")
    else:
        delete_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        account.delete_account(bank_account, active_agent.username, delete_date, result)


""" CUSTOMER FUNCTIONS """


def view_customer(customer_id, result):
    customer_accounts = []
    result.set_code("99")
    customer.view_customer(customer_id, customer_accounts, result)

    if result.code == "00":
        return customer_accounts


def update_customer(active_customer, result):
    """ Update Customer """
    result.set_code("99")
    customer.update_customer(active_customer, result)


def delete_customer(active_agent, active_customer, result):
    """ Delete customer """
    result.set_code("99")
    if view_customer(active_customer.customer_id, result):
        result.set_code("04")
        print(result.message)
    else:
        delete_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        customer.delete_customer(active_customer, active_agent.username, delete_date, result)


""" MOVEMENTS FUNCTIONS """


def deposit(active_movement, active_account, result):
    """ Deposit money into a bank account """
    result.set_code("99")
    fee = active_movement.get_transaction_fee()
    active_movement.previous_balance = active_account.balance
    active_movement.new_balance = active_account.balance + active_movement.amount
    active_account.balance = active_movement.new_balance
    active_movement.movement_date = datetime.now()
    movement.create_transaction(active_movement, result)
    if result.code == "00":
        fee_movement = active_movement.copy()
        fee_movement.amount = fee
        fee_movement.transaction_id = 10
        fee_movement.destination_account = "000000000"
        fee_movement.source_account = active_account.acc_number
        fee_movement.previous_balance = active_account.balance
        fee_movement.new_balance = active_account.balance - fee
        active_account.balance = fee_movement.new_balance
        movement.create_transaction(fee_movement, result)
        if result.code == "00":
            account.update_account(active_account, result)
            # print("Deposit Successful")


def withdrawal(active_movement, active_account, result):
    """ Withdraw money from a bank account """
    result.set_code("99")
    fee = active_movement.get_transaction_fee()
    active_movement.previous_balance = active_account.balance
    active_movement.new_balance = active_account.balance - active_movement.amount
    active_movement.movement_date = datetime.now()
    if active_movement.new_balance - fee < active_account.acc_type.minimum_balance:
        result.set_code("06")
        # print(result.message)
    else:
        active_account.transfer_amount += active_movement.amount
        active_account.transfer_quantity = active_account.transfer_quantity + 1
        active_account.balance = active_movement.new_balance
        movement.create_transaction(active_movement, result)
        if result.code == "00":
            fee_movement = active_movement.copy()
            fee_movement.amount = fee
            fee_movement.transaction_id = 10
            fee_movement.destination_account = "000000000"
            fee_movement.source_account = active_account.acc_number
            fee_movement.previous_balance = active_account.balance
            fee_movement.new_balance = active_account.balance - fee
            active_account.balance = fee_movement.new_balance
            movement.create_transaction(fee_movement, result)
            if result.code == "00":
                account.update_account(active_account, result)
                # print("Withdrawal Successful")


def transfer(active_movement, active_account, result):
    """ Transfer money from a bank account to another account """
    account_result = []
    result.set_code("99")
    active_product = active_account.acc_type
    agent.search_account(active_movement.destination_account, account_result, result)

    if account_result:
        destination_account = account_result[0]
        active_movement.destination_account = destination_account.acc_number
        fee = active_movement.get_transaction_fee()
        active_movement.previous_balance = active_account.balance
        active_movement.new_balance = active_account.balance - active_movement.amount
        active_movement.movement_date = datetime.now()
        if active_movement.new_balance - fee < active_product.minimum_balance:
            result.set_code("06")
        elif active_account.transfer_quantity + 1 > active_product.quantity_limit:
            result.set_code("07")
        elif active_account.transfer_amount + active_movement.amount > active_product.amount_limit:
            result.set_code("08")
        else:
            active_account.transfer_amount += active_movement.amount
            active_account.transfer_quantity = active_account.transfer_quantity + 1
            active_account.balance = active_movement.new_balance
            movement.create_transaction(active_movement, result)
            if result.code == "00":
                fee_movement = active_movement.copy()
                fee_movement.amount = fee
                fee_movement.transaction_id = 10
                fee_movement.destination_account = "000000000"
                fee_movement.source_account = active_account.acc_number
                fee_movement.previous_balance = active_account.balance
                fee_movement.new_balance = active_account.balance - fee
                active_account.balance = fee_movement.new_balance
                movement.create_transaction(fee_movement, result)
                if result.code == "00":
                    account.update_account(active_account, result)
                    if result.code == "00":
                        destination_account.balance += active_movement.amount
                        account.update_account(destination_account, result)
                        # print("Transfer Successful")
    else:
        result.set_code("09")
        # print(result.message)
