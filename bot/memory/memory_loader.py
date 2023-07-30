from sqlalchemy import func

from bot.memory.shorterm_memory import ShortTermMemory
from datasource.rdbms.sqlite import get_session, HistoryModel


class MemoryLoader:
    def load_short_term_memory(self):
        session = get_session()
        results = session.query(HistoryModel, func.order_by(HistoryModel.create_time).desc()).all()
        return [ShortTermMemory.from_orm(ShortTermMemory, result) for result in results]
