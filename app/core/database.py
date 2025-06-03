from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


DATABASE_URL_SYNC = "sqlite:///./db.sqlite3" 
DATABASE_URL_ASYNC = "sqlite+aiosqlite:///./db.sqlite3" 

# Create sync engine & session factory
sync_engine = create_engine(DATABASE_URL_SYNC, connect_args={"check_same_thread": False})
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Create async engine & session factory
async_engine = create_async_engine(DATABASE_URL_ASYNC, connect_args={"check_same_thread": False})
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)




class Base(DeclarativeBase):
    pass


def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()  


async def get_async_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()  
