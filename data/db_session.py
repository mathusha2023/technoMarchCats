from sqlalchemy.orm import Session
import sqlalchemy as sa
import sqlalchemy.orm as orm


SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init(db_url):
    global __factory

    if __factory:
        return

    if not db_url or not db_url.strip():
        raise Exception("Необходимо указать файл базы данных.")

    print(f"Подключение к базе данных по адресу {db_url}")

    engine = sa.create_engine(db_url, echo=False, max_overflow=1100, pool_size=1000)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    with engine.connect() as conn:
        result = conn.execute(sa.text("SELECT 1 FROM information_schema.tables WHERE table_schema='public'"))
        if result.fetchone() is None:
            SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()