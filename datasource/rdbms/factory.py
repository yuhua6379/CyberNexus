from datasource.rdbms.base import Rdbms, RDBMSBase, RdbmsType
from datasource.rdbms.sqlite_impl.engine import Base


def get_rdbms(conf: Rdbms) -> RDBMSBase:
    if conf.type == RdbmsType.Sqlite:
        from datasource.rdbms.base_entities import set_base
        set_base(Base)
        from datasource.rdbms.sqlite_impl.impl import Sqlite
        return Sqlite(conf)
    else:
        raise RuntimeError(f"unsupported rdbms type: {conf.type}")
