from sqlalchemy.ext.asyncio import AsyncEngine
from src.db.database import Base
from src.models.todo import ToDo

async def init_db(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)