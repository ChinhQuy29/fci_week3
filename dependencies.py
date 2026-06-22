from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import Settings

engine = create_engine(Settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()