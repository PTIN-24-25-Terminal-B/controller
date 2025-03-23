## Código para crear una conexión a la base de datos
# De esta manera, se puede usar la misma conexión en todos los servicios que necesiten acceder a la base de datos.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ejemplo para PostgreSQL (usa variables de entorno en producción)
DATABASE_URL = "postgresql://user:password@localhost:5432/mydatabase"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()