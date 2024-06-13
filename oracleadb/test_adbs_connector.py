import os
import sys
import pytest
from dotenv import load_dotenv
from provider.client import ADBSClient

load_dotenv()

#Test End to End Functionality
def test_end_to_end_employee_table():

    #Create a DB Connection
    dsn = os.getenv("ORACLEADB_DSN")
    user = os.getenv("ORACLEADB_USER")
    password = os.getenv("ORACLEADB_PASSWORD")
    wallet_dir = os.getenv("ORACLEADB_WALLET_DIR")
    wallet_password = os.getenv("ORACLEADB_WALLET_PASSWORD")
    fts_columns = "employee_reviews,technical_feedback"
    table_name = "employee"
    connection_type = os.getenv("ORACLEADB_CONNECTION_TYPE")
    auto_index_fts_columns = os.getenv("ORACLEADB_AUTO_INDEX_FTS_COLUMNS")

    create_table_sql = """
            CREATE TABLE EMPLOYEE (
                EMPLOYEE_ID NUMBER PRIMARY KEY,
                FIRST_NAME VARCHAR2(50),
                LAST_NAME VARCHAR2(50),
                EMPLOYEE_REVIEWS VARCHAR2(500),
                TECHNICAL_FEEDBACK VARCHAR2 (500)
            )
    """

    # SQL script to insert data into the EMPLOYEE table
    insert_data_sql = """
        INSERT INTO EMPLOYEE (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, EMPLOYEE_REVIEWS, TECHNICAL_FEEDBACK)
        VALUES (:employee_id, :first_name, :last_name, :employee_reviews, :technical_feedback)
    """

    client = ADBSClient(
                        user=user, 
                        password=password, 
                        dsn=dsn,
                        wallet_dir=wallet_dir, 
                        wallet_password=wallet_password,
                        fts_columns = fts_columns,
                        connection_type = connection_type,
                        table_name = table_name,
                        auto_index_fts_columns = False #as manually indexing later, as table needs needs to be made first (this is for testing only)
            )
    
    connection = client.get_connection()

    cursor = connection.cursor()

    # Execute the create table SQL
    cursor.execute(create_table_sql)
    
    #Insert data into the EMPLOYEE table
    data_to_insert = [
        (1, 'John', 'Doe', 'Great employee, highly skilled and dedicated.', 'An elegant python Coder'),
        (2, 'Jane', 'Smith', 'Needs improvement in communication skills.', 'Can code in Java with her eyes closed'),
        (3, 'Michael', 'Johnson', 'Consistently meets deadlines and delivers quality work.', 'Eats ElasticSearch for Breakfast'),
        (4, 'Emily', 'Williams', 'Very creative and brings innovative ideas to the team.', 'He makes Python look like english'),
        (5, 'David', 'Brown', 'Excellent team player, always willing to help others.', 'Makes AI look less intelligent when he codes')
    ]

    cursor.executemany(insert_data_sql, data_to_insert)

    connection.commit()

    client._create_index_configuration()

    for column in client.fts_columns:
        client._prepare_fts_index(column)

    query = "I want to talk to people who are very skilled and help others and can also understand ElasticSearch"

    response = client.search(query)

    expected_response = [
        {'EMPLOYEE_ID': 1, 'FIRST_NAME': 'John', 'LAST_NAME': 'Doe', 'EMPLOYEE_REVIEWS': 'Great employee, highly skilled and dedicated.', 'TECHNICAL_FEEDBACK': 'An elegant python Coder'}, 
        {'EMPLOYEE_ID': 2, 'FIRST_NAME': 'Jane', 'LAST_NAME': 'Smith', 'EMPLOYEE_REVIEWS': 'Needs improvement in communication skills.', 'TECHNICAL_FEEDBACK': 'Can code in Java with her eyes closed'}, 
        {'EMPLOYEE_ID': 3, 'FIRST_NAME': 'Michael', 'LAST_NAME': 'Johnson', 'EMPLOYEE_REVIEWS': 'Consistently meets deadlines and delivers quality work.', 'TECHNICAL_FEEDBACK': 'Eats ElasticSearch for Breakfast'}, 
        {'EMPLOYEE_ID': 5, 'FIRST_NAME': 'David', 'LAST_NAME': 'Brown', 'EMPLOYEE_REVIEWS': 'Excellent team player, always willing to help others.', 'TECHNICAL_FEEDBACK': 'Makes AI look less intelligent when he codes'}
    ]

    assert response == expected_response

#Test End to End Functionality
def test_end_to_end_tickets_table():

    #Create a DB Connection
    dsn = os.getenv("ORACLEADB_DSN")
    user = os.getenv("ORACLEADB_USER")
    password = os.getenv("ORACLEADB_PASSWORD")
    wallet_dir = os.getenv("ORACLEADB_WALLET_DIR")
    wallet_password = os.getenv("ORACLEADB_WALLET_PASSWORD")
    fts_columns = "ISSUE_DESCRIPTION,TICKET_RESOLUTION"
    table_name = "TICKETS"
    connection_type = os.getenv("ORACLEADB_CONNECTION_TYPE")
    auto_index_fts_columns = os.getenv("ORACLEADB_AUTO_INDEX_FTS_COLUMNS")

    create_table_sql = """
            CREATE TABLE TICKETS (
                TICKET_ID NUMBER PRIMARY KEY,
                ISSUE_DESCRIPTION VARCHAR2(500),
                TICKET_RESOLUTION VARCHAR2(500)
            )
    """

    # SQL script to insert data into the EMPLOYEE table
    insert_data_sql = """
        INSERT INTO TICKETS (TICKET_ID, ISSUE_DESCRIPTION, TICKET_RESOLUTION)
        VALUES (:ticket_id, :issue_description, :ticket_resolution)
    """

    client = ADBSClient(
                        user=user, 
                        password=password, 
                        dsn=dsn,
                        wallet_dir=wallet_dir, 
                        wallet_password=wallet_password,
                        fts_columns = fts_columns,
                        connection_type = connection_type,
                        table_name = table_name,
                        auto_index_fts_columns = False #as manually indexing later, as table needs needs to be made first (this is for testing only)
            )
    
    connection = client.get_connection()

    cursor = connection.cursor()

    # Execute the create table SQL
    cursor.execute(create_table_sql)
    
    #Insert data into the Tickets table
    data_to_insert = [
        (1, 'Cannot log in to account', 'Reset password and cleared cache'),
        (2, 'Product delivery delayed', 'Expedited shipping and issued refund'),
        (3, 'Website error message', 'Patched backend system for bug fix'),
        (4, 'Billing discrepancy', 'Investigated and corrected billing error'),
        (5, 'Product not as described', 'Contacted return team and refund process'),
        (6, 'Blocked login', 'Open in Incognito'),
        (7, 'Login taking too long', 'Switched to older app version as new version is device incompatible'),
        (8, 'Billed for twice the usage', 'Confirmed discrepancy and raised ticket to backend'),
        (9, 'Unable to login, password error', 'Had Caps Lock on, told to check Caps'),
        (10, 'Shipped faulty product', 'Raised ticket with return team and initiated refund')
    ]


    cursor.executemany(insert_data_sql, data_to_insert)

    connection.commit()

    client._create_index_configuration()

    for column in client.fts_columns:
        client._prepare_fts_index(column)

    query = "Customer is facing issues with Login what actions can I take or suggest the user to do"

    response = client.search(query)
    
    expected_response = [
        {'TICKET_ID': 1, 'ISSUE_DESCRIPTION': 'Cannot log in to account', 'TICKET_RESOLUTION': 'Reset password and cleared cache'},
        {'TICKET_ID': 2, 'ISSUE_DESCRIPTION': 'Product delivery delayed', 'TICKET_RESOLUTION': 'Expedited shipping and issued refund'},
        {'TICKET_ID': 6, 'ISSUE_DESCRIPTION': 'Blocked login', 'TICKET_RESOLUTION': 'Open in Incognito'},
        {'TICKET_ID': 7, 'ISSUE_DESCRIPTION': 'Login taking too long', 'TICKET_RESOLUTION': 'Switched to older app version as new version is device incompatible'},
        {'TICKET_ID': 8, 'ISSUE_DESCRIPTION': 'Billed for twice the usage', 'TICKET_RESOLUTION': 'Confirmed discrepancy and raised ticket to backend'},
        {'TICKET_ID': 9, 'ISSUE_DESCRIPTION': 'Unable to login, password error', 'TICKET_RESOLUTION': 'Had Caps Lock on, told to check Caps'},
        {'TICKET_ID': 10, 'ISSUE_DESCRIPTION': 'Shipped faulty product', 'TICKET_RESOLUTION': 'Raised ticket with return team and initiated refund'}
    ]

    assert response == expected_response
