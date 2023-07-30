from langchain.tools import BaseTool, StructuredTool
import requests
import logging
from datetime import datetime


def watch() -> datetime:
    """useful for when you want to know what day or time it is."""

    dt = datetime.now()
    logging.info(f"the current dt is {dt}")
    return dt


watch = StructuredTool.from_function(watch)
