"""
Database operations
"""
import sqlite3
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def create_or_check_db(db_path, table_name, schema):
    """
    Creates or checks a database table.
    
    Args:
        db_path (str): Path to the database file.
        table_name (str): Name of the table to create or check.
        schema (str): Schema of the table to create.

    Returns:
        None

    Raise:
        sqlite3.Error: If the database operation fails.
    """
    logger = logging.getLogger(__name__)
    logger.info("Creating or checking database")
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        logger.info("Successfully connected to database")
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}({schema})""")
        logger.info("Successfully created table")
        con.commit()
        logger.info("Successfully committed changes")


def add_records_to_db(data,db_path,table_name):
    """
    Adds records to the database.
    
    Args:
        data (pd.DataFrame): DataFrame containing data to add.
        db_path (str): Path to the database file.
        table_name (str): Name of the table to add data to.

    Returns:
        None

    Raise:
        sqlite3.Error: If the database operation fails.
    """
    logger = logging.getLogger(__name__)
    logger.info("Adding records to database")
    with sqlite3.connect(db_path) as con:
        data.to_sql(table_name, con, if_exists='append',index = False)
        logger.info("Successfully added records to database")

def get_rows_number(db_path,table_name,unique_id):
    """
    Gets the number of rows in a table.
    
    Args:
        db_path (str): Path to the database file.
        table_name (str): Name of the table to get the number of rows from.
        unique_id (str): Unique identifier of the table.

    Returns:
        int: Number of rows in the table.

    Raise:
        sqlite3.Error: If the database operation fails.
    """
    logger = logging.getLogger(__name__)
    logger.info("Getting rows number")
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        logger.info("Successfully connected to database")
        cur.execute(f"""SELECT COUNT({unique_id}) FROM {table_name}""")
        logger.info("Successfully executed query")
        result = cur.fetchone()
    return result[0]


def get_table_keys(db_path, table_name, unique_id):
    """
    Gets the unique keys from a table.
    
    Args:
        db_path (str): Path to the database file.
        table_name (str): Name of the table to get the unique keys from.
        unique_id (str): Unique identifier of the table.

    Returns:
        list: List of unique keys from the table.

    Raise:
        sqlite3.Error: If the database operation fails.
    """
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        try:
            cur.execute(f"""SELECT DISTINCT {unique_id} FROM {table_name} """)
            result = cur.fetchall()
            result_list = [item[0] for item in result]
        except sqlite3.OperationalError:
            result_list = []
    return result_list
def get_biggest_receipt_customer(db_path,table_name,unique_id):
    """
    Gets the biggest receipt customer from the database.
    
    Args:
        db_path (str): Path to the database file.
        table_name (str): Name of the table to get the biggest receipt customer from.
        unique_id (str): Unique identifier of the table.

    Returns:
        pd.DataFrame: DataFrame containing the biggest receipt customer.

    Raise:
        sqlite3.Error: If the database operation fails.
    """
    logger = logging.getLogger(__name__)
    logger.info("Getting biggest receipt customer")
    with sqlite3.connect(db_path) as con:
        twoja_zmienna = pd.read_sql_query("""SELECT c.name, r.total_money FROM receipt_headers r JOIN customers c ON r.customer_id = c.id ORDER BY r.total_money DESC LIMIT 1""", con)
        logger.info("Successfully executed query")
        logger.info(f"Biggest receipt customer: {twoja_zmienna}")
        return twoja_zmienna
        
    