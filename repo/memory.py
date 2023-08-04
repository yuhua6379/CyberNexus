from pydantic import BaseModel

from datasource.config import rdbms_instance
from datasource.rdbms.entities import MemoryModel


class Memory(BaseModel):
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
