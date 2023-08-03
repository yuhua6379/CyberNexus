from datasource.rdbms.base import RdbmsType
from datasource.rdbms.factory import Rdbms, get_rdbms

SQLITE_URI = 'sqlite:///local.db'

CHROMADB_URI = "./chromadb_local.db"

RDBMS_CONF = Rdbms(uri=SQLITE_URI, type=RdbmsType.Sqlite)
rdbms_instance = get_rdbms(RDBMS_CONF)
