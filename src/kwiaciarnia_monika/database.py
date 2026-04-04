from pathlib import Path
import sqlite3
import logging
import pandas as pd
from typing import List, Optional
from datetime import date

logger = logging.getLogger(__name__)


def create_or_check_db(db_path: Path, table_name: str, schema: str):
    """
    Creates or checks a database table.
    """
    logger.info("Creating or checking database")
    with sqlite3.connect(db_path) as con:
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
    with sqlite3.connect(db_path) as con:
        data.to_sql(table_name, con, if_exists="append", index=False)
        logger.info("Successfully added records to database")


def get_rows_number(db_path: Path, table_name: str, unique_id: str) -> int:
    """
    Gets the number of rows in a table.
    """
    logger.info("Getting rows number")
    with sqlite3.connect(db_path) as con:
        logger.info("Successfully connected to database")
        result_df = pd.read_sql_query(
            f"""SELECT COUNT({unique_id}) FROM {table_name}""", con
        )
        logger.info("Successfully executed query")
        result = result_df.iloc[0, 0]
        return int(result)


def get_table_keys(db_path: Path, table_name: str, unique_id: str) -> List[str]:
    """
    Gets the unique keys from a table.
    """
    with sqlite3.connect(db_path) as con:
        try:
            result_df = pd.read_sql_query(
                f"""SELECT DISTINCT {unique_id} FROM {table_name} """, con
            )
            result_list = result_df[unique_id].tolist()
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
    with sqlite3.connect(db_path) as con:
        if query_date is None:
            query_date = date.today()
        top_customer = pd.read_sql_query(
            """SELECT c.name, r.total_money FROM receipt_headers r JOIN customers c ON r.customer_id = c.id WHERE r.receipt_date = ? ORDER BY r.total_money DESC LIMIT 1""",
            con,
            params=[query_date],
        )
        logger.info("Successfully executed query")
        logger.info(f"Biggest receipt customer: {top_customer}")
        if top_customer.empty:
            return {"name": "Brak danych", "total_money": 0}
        return {
            "name": top_customer["name"].iloc[0],
            "total_money": top_customer["total_money"].iloc[0],
        }


def get_customer_receipts_history(db_path: Path, customer_id: str) -> pd.DataFrame:
    """
    Gets the customer receipts history from the database.
    """
    logger.info("Getting customer receipts history")
    with sqlite3.connect(db_path) as con:
        result_df = pd.read_sql_query(
            """SELECT * FROM receipt_headers WHERE customer_id = ?""",
            con,
            params=[customer_id],
        )
        logger.info("Successfully executed query")
        logger.info(f"Customer receipts history: {result_df}")
        return result_df


def get_all_customers(db_path: Path) -> pd.DataFrame:
    """
    Gets all customers from the database.
    """
    logger.info("Getting all customers")
    with sqlite3.connect(db_path) as con:
        result_df = pd.read_sql_query(
            """SELECT DISTINCT r.customer_id, c.name FROM receipt_headers r JOIN customers c ON r.customer_id = c.id""",
            con,
        )
        logger.info("Successfully executed query")
        logger.info(f"All customers: {result_df}")
        return result_df


def get_customer_total_spent(db_path: Path, customer_id: str) -> float:
    """
    Gets the total amount spent by a customer.
    """
    logger.info("Getting customer total spent")
    with sqlite3.connect(db_path) as con:
        result_df = pd.read_sql_query(
            """SELECT COALESCE(SUM(total_money), 0) FROM receipt_headers WHERE customer_id = ?""",
            con,
            params=[customer_id],
        )
        logger.info("Successfully executed query")
        logger.info(f"Customer total spent: {result_df}")
        return float(result_df.iloc[0, 0])
