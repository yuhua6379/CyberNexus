from datasource.rdbms.base import RdbmsType
from datasource.rdbms.factory import Rdbms, get_rdbms
from datasource.vectordb.base import VectorDBConf, VectorDBType
from datasource.vectordb.factory import VectorDBFactory

SQLITE_URI = 'sqlite:///local.db'

CHROMADB_URI = "./chromadb_local.db"

RDBMS_CONF = Rdbms(uri=SQLITE_URI, type=RdbmsType.Sqlite)
rdbms_instance = get_rdbms(RDBMS_CONF)

VECTOR_DB_CONF = VectorDBConf(uri=CHROMADB_URI, type=VectorDBType.Chromadb)
vector_db_factory = VectorDBFactory(VECTOR_DB_CONF)
