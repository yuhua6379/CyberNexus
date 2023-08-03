from datasource.vectordb.base import VectorDB, VectorDBType
from datasource.vectordb.chromadb_impl.impl import ChromaDB


class VectorDBFactory:
    def __init__(self):
        self.vector_db_instances = {}

    def get_vector_db(self, conf: VectorDB, collection_name: str):

        if collection_name not in self.vector_db_instances:
            if conf.type == VectorDBType.Chromadb:
                self.vector_db_instances[collection_name] = ChromaDB(conf, collection_name)
            else:
                raise RuntimeError(f"unsupported vector db: {conf.type}")

        return self.vector_db_instances[collection_name]
