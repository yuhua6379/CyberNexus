import time
from uuid import uuid4

from datasource.config import vector_db_factory
from datasource.vectordb.entities import Document
from repo.character import Character
from repo.memory import Memory


class LongTermMemory:

    def __init__(self, character: Character):
        self.character = character

    def _get_memory_collection_name(self):
        return f'memory_of_{self.character.name}'

    def save(self, memory: str):
        vector_db_instance = vector_db_factory.get_vector_db(self._get_memory_collection_name())
        doc_id = str(uuid4())
        document = Document(id=doc_id, content=memory, meta_data={"timestamp": time.time()})
        vector_db_instance.save(document)
        Memory.add(self.character.id, doc_id, content=document.content)

    def search(self, key_word):
        # 取相关性最高前10条
        vector_db_instance = vector_db_factory.get_vector_db(self._get_memory_collection_name())
        res_list = vector_db_instance.query(key_word)
        return [res.document.content for res in res_list[:10]]

    def latest_memory(self):
        return "\n".join([memory.content for memory in Memory.get_latest_memory_by_character_id(self.character.id)])
