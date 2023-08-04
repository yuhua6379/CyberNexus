from typing import List, Tuple

import chromadb

from datasource.vectordb.base import VectorDbBase, VectorDBConf
from datasource.vectordb.entities import Response, Document


class ChromaDB(VectorDbBase):

    def __init__(self, conf: VectorDBConf, collection_name: str, create_if_not_exists=True):
        super().__init__(conf)
        self.connection = chromadb.PersistentClient(self.conf.uri)
        try:
            self.collection = self.connection.get_collection(collection_name)
        except:
            if create_if_not_exists:
                self.collection = self.connection.create_collection(collection_name)
            else:
                raise

    def batch_get(self, ids: List[str]) -> List[Document]:
        ret = self.collection.get(ids=ids)
        response_list = []
        for i in range(len(ret["ids"])):
            ids = ret["ids"]
            metadatas = ret['metadatas']
            documents = ret['documents']

            doc = Document(id=ids[i], meta_data=dict(metadatas[i]), content=documents[i])

            response_list.append(doc)
        return response_list

    def batch_save(self, doc_list: List[Document]):
        documents = []
        metadatas = []
        ids = []
        for doc in doc_list:
            documents.append(doc.content)
            metadatas.append(doc.meta_data)
            ids.append(doc.id)

        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
        )

    def batch_query(self, query_texts: List[str]) -> List[Tuple[str, List[Response]]]:
        ret = self.collection.query(query_texts=query_texts)
        response_list = []
        for i in range(len(ret["ids"])):
            single_response = []
            for j in range(len(ret['ids'][0])):
                ids = ret["ids"][i]
                distances = ret['distances'][i]
                metadatas = ret['metadatas'][i]
                documents = ret['documents'][i]

                doc = Document(id=ids[j], meta_data=dict(metadatas[j]), content=documents[j])

                single_response.append(Response(distance=distances[j], document=doc))
            response_list.append((query_texts[i], single_response))
        return response_list
