import logging
from datetime import datetime

from langchain.tools import StructuredTool


def watch() -> datetime:
    """useful for when you want to know what day or time it is."""

    dt = datetime.now()
    logging.info(f"the current dt is {dt}")
    return dt


watch = StructuredTool.from_function(watch)
