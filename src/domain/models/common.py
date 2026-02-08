from litestar.contrib.sqlalchemy.base import orm_registry

BaseWithoutID = orm_registry.generate_base()
