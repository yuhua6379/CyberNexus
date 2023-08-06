from pydantic import BaseModel

from datasource.config import rdbms_instance
from datasource.rdbms.entities import MemoryModel


class Memory(BaseModel, orm_mode=True):
    character_id: int
    vector_db_id: str
    content: str

    @classmethod
    def add(cls, character_id: int, vector_db_id: str, content: str):
        memory = MemoryModel()
        memory.character_id = character_id
        memory.vector_db_id = vector_db_id
        memory.content = content

        with rdbms_instance.get_session() as session:
            session.add(memory)
            session.commit()

    @classmethod
    def get_latest_memory_by_character_id(cls, character_id: int):
        with rdbms_instance.get_session() as session:
            results = session.query(MemoryModel).filter(MemoryModel.character_id == character_id).order_by(
                MemoryModel.create_time.desc()).limit(10).all()
            return [cls.from_orm(memory) for memory in results]
