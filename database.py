from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Yerel bir SQLite veritabanı dosyası tanımlıyoruz
SQLALCHEMY_DATABASE_URL = "sqlite:///./bank.db"

# SQLite için thread güvenliğini kapatıyoruz (FastAPI asenkron çalıştığı için gerekli)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Her API isteğinde veritabanı oturumunu açıp işi bitince kapatacak yardımcı fonksiyon
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()