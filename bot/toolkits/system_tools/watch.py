from langchain.tools import BaseTool
import requests
import logging
from datetime import datetime


class Watch(BaseTool):
    name = "watch"
    description = "useful for when you want to know what day or time it is"

    @staticmethod
    def get_dt() -> datetime:
        dt = datetime.now()
        logging.info(f"the current dt is {dt}")
        return dt

    def _run(self) -> datetime:
        return self.get_dt()

    async def _arun(self) -> datetime:
        return self.get_dt()
