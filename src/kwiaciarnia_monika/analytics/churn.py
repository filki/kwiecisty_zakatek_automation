import pandas as pd

from src.kwiaciarnia_monika.db.engine import (
    get_customer_receipts_history,
    get_all_customers,
    get_customer_total_spent,
)
from pathlib import Path
from src.kwiaciarnia_monika.logger import setup_logger
from typing import List

logger = setup_logger()

CHURN_THRESHOLD = 35
FACTOR = 1.5


def find_possible_churn(db_path: Path) -> List[dict]:
    """
    Finds customers who may be at risk of churning.

    Args:
        db_path (Path): Path to the database file.

    Returns:
        None

    Raise:
        sqlite3.Error: If the database operation fails.
    """
    customers = get_all_customers(db_path)

    logger.info("Finding possible churn")
    churn_customers = []
    for customer in customers.iterrows():
        customer_id = customer[1]["customer_id"]
        customer_name = customer[1]["name"]
        print(f"DEBUG: Sprawdzam ID: {customer_id}")
        try:
            history = get_customer_receipts_history(db_path, str(customer_id))
            total_spent = get_customer_total_spent(db_path, str(customer_id))
            history["receipt_date"] = pd.to_datetime(history["receipt_date"])
            history_sorted = history.sort_values(by="receipt_date")
            days_since_last_purchase = (
                pd.Timestamp.now(tz="UTC") - history_sorted["receipt_date"].iloc[-1]
            ).days
            logger.info(
                f"Days since last purchase for {customer_name}: {days_since_last_purchase}"
            )
        except IndexError:
            days_since_last_purchase = 0
            total_spent = 0
            logger.info(f"Customer {customer_name} has no purchase history")
        if days_since_last_purchase > CHURN_THRESHOLD:
            churn_customers.append(
                {
                    "customer_id": customer_id,
                    "customer_name": customer_name,
                    "days_since_last_purchase": days_since_last_purchase,
                    "total_spent": total_spent,
                }
            )
    return churn_customers
