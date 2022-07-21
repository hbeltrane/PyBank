""" Term Project - PyBank
CSD 4523 - Python II
CSAM   Group 02   2022S
"""
from db.database_conn import ConnectionPool


def main():
    """ Application main method """
    # Database Configuration
    config = {
        'user': 'test_user',
        'password': 'secret',
        'host': 'localhost',
        'port': '3307',
        'database': 'pybank',
        'pool_name': 'pybank_conn_pool',
        'pool_size': 1
    }

    print("* Welcome to PyBank *")

    ConnectionPool.create_pool(**config)


# Start the program
if __name__ == '__main__':
    main()
