from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://postgres:prash741@localhost/FastAPi"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()