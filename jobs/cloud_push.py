import subprocess
import logging
from config import DB_PATH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TURSO_DB_NAME = "kwiaciarnia-db"


def push_to_cloud():
    """
    Exports local SQLite database to a SQL dump and pushes it to Turso Cloud.
    This replaces the data in the cloud with the current local state.
    """
    logger.info("Starting Cloud Push synchronization")

    # Check if local DB exists
    if not DB_PATH.exists():
        logger.error(f"Local database not found at {DB_PATH}")
        return

    try:
        dump_command = f"sqlite3 {DB_PATH} .dump"
        logger.info(f"Generating SQL dump from {DB_PATH}")

        cleanup_sql = (
            "DROP TABLE IF EXISTS customers;\nDROP TABLE IF EXISTS receipt_headers;\n"
        )

        process = subprocess.Popen(
            dump_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        dump_content, errors = process.communicate()

        if process.returncode != 0:
            logger.error(f"Error generating dump: {errors}")
            return

        full_sql = cleanup_sql + dump_content

        logger.info(f"Pushing dump to Turso database: {TURSO_DB_NAME}")

        push_process = subprocess.Popen(
            ["turso", "db", "shell", TURSO_DB_NAME],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = push_process.communicate(input=full_sql)

        if push_process.returncode == 0:
            logger.info("Cloud Push successful!")
        else:
            logger.error(f"Cloud Push failed: {stderr}")
            if "not found" in stderr.lower():
                logger.error(
                    "Make sure Turso CLI is in your PATH and you are logged in."
                )

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    push_to_cloud()
