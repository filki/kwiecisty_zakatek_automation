from pathlib import Path
import sqlite3
import logging
import pandas as pd
from typing import List, Optional
from datetime import date
import libsql
import os
from contextlib import contextmanager

logger = logging.getLogger(__name__)


def create_or_check_db(db_path: Path, table_name: str, schema: str):
    """
    Creates or checks a database table.
    """
    logger.info("Creating or checking database")
    with get_connection(db_path) as con:
        cur = con.cursor()
        logger.info("Successfully connected to database")
        cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}({schema})""")
        logger.info("Successfully created table")
        con.commit()
        logger.info("Successfully committed changes")


def add_records_to_db(data: pd.DataFrame, db_path: Path, table_name: str):
    """
    Adds records to the database.
    """
    if data.empty:
        logger.info("No records to add")
        return

    logger.info(f"Adding {len(data)} records to database table: {table_name}")
    with get_connection(db_path) as con:
        data.to_sql(table_name, con, if_exists="append", index=False)
        logger.info("Successfully added records to database")


def get_rows_number(
    db_path: Path, table_name: str, unique_id: str, query_date: Optional[date] = None
) -> int:
    """
    Gets the number of rows in a table.
    """
    logger.info("Getting rows number")
    with get_connection(db_path) as con:
        logger.info("Successfully connected to database")
        cur = con.cursor()
        if query_date is None:
            cur.execute(f"""SELECT COUNT({unique_id}) FROM {table_name}""")
        else:
            cur.execute(
                f"""SELECT COUNT({unique_id}) FROM {table_name} WHERE DATE(receipt_date) = ?""",
                [str(query_date)],
            )
        logger.info("Successfully executed query")
        result = cur.fetchone()[0]
        return int(result)


def get_table_keys(db_path: Path, table_name: str, unique_id: str) -> List[str]:
    """
    Gets the unique keys from a table.
    """
    with get_connection(db_path) as con:
        try:
            cur = con.cursor()
            cur.execute(f"""SELECT DISTINCT {unique_id} FROM {table_name} """)
            result_list = cur.fetchall()
        except sqlite3.OperationalError:
            result_list = []
    return result_list


def get_biggest_receipt_customer(
    db_path: Path, query_date: Optional[date] = None
) -> dict:
    """
    Gets the biggest receipt customer from the database.
    """
    logger.info("Getting biggest receipt customer")
    with get_connection(db_path) as con:
        if query_date is None:
            query_date = date.today()
        cur = con.cursor()
        cur.execute(
            """SELECT COALESCE(c.name, 'Gość'), r.total_money FROM receipt_headers r LEFT JOIN customers c ON r.customer_id = c.id WHERE r.receipt_date = DATE(?) ORDER BY r.total_money DESC LIMIT 1""",
            [str(query_date)],
        )
        logger.info("Successfully executed query")
        top_customer = cur.fetchone()
        logger.info(f"Biggest receipt customer: {top_customer}")
        if top_customer is None:
            return {"name": "Brak danych", "total_money": 0}
        return {
            "name": top_customer[0],
            "total_money": top_customer[1],
        }


def get_customer_receipts_history(db_path: Path, customer_id: str) -> pd.DataFrame:
    """
    Gets the customer receipts history from the database.
    """
    logger.info("Getting customer receipts history")
    with get_connection(db_path) as con:
        cur = con.cursor()
        cur.execute(
            """SELECT * FROM receipt_headers WHERE customer_id = ?""",
            [customer_id],
        )
        logger.info("Successfully executed query")
        result_df = cur.fetchall()
        logger.info(f"Customer receipts history: {result_df}")
        return result_df


def get_all_customers(db_path: Path) -> pd.DataFrame:
    """
    Gets all customers from the database.
    """
    logger.info("Getting all customers")
    with get_connection(db_path) as con:
        cur = con.cursor()
        cur.execute(
            """SELECT DISTINCT r.customer_id, c.name FROM receipt_headers r JOIN customers c ON r.customer_id = c.id"""
        )
        logger.info("Successfully executed query")
        result = cur.fetchall()
        result_df = result_to_df(result, ["customer_id", "name"])
        logger.info(f"All customers: {result_df}")
        return result_df


def get_customer_total_spent(db_path: Path, customer_id: str) -> float:
    """
    Gets the total amount spent by a customer.
    """
    logger.info("Getting customer total spent")
    with get_connection(db_path) as con:
        cur = con.cursor()
        cur.execute(
            """SELECT COALESCE(SUM(total_money), 0) FROM receipt_headers WHERE customer_id = ?""",
            [customer_id],
        )
        logger.info("Successfully executed query")
        result = cur.fetchone()
        logger.info(f"Customer total spent: {result}")
        return float(result[0])


@contextmanager
def get_connection(db_path: Path):
    """
    Returns a connection to the database.
    """
    logger.info("Getting connection to database")
    if os.getenv("TURSO_DATABASE_URL") and os.getenv("TURSO_AUTH_TOKEN"):
        con = libsql.connect(
            os.getenv("TURSO_DATABASE_URL"), auth_token=os.getenv("TURSO_AUTH_TOKEN")
        )
    else:
        con = sqlite3.connect(db_path)
    logger.info("Successfully connected to database")
    yield con
    con.close()
    logger.info("Successfully closed connection to database")


def result_to_df(result: list, columns: list) -> pd.DataFrame:
    """
    Converts a list of tuples to a pandas DataFrame.
    """
    logger.info("Converting result to DataFrame")
    df = pd.DataFrame(result, columns=columns)
    logger.info("Successfully converted result to DataFrame")
    return df
