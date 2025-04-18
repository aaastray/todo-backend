import uuid

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_session
from src.schemas.todo import ToDoCreate, ToDoFromDB, ToDoUpdate
from src.models.todo import ToDo

todo_router = APIRouter(prefix="/todo", tags=["Todo"])


@todo_router.get("/all", response_model=list[ToDoFromDB])
async def get_todos(
        limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of items to return"),
        offset: int = Query(default=0, ge=0, description="Number of items to skip"),
        session: AsyncSession = Depends(get_session)
):
    try:
        query = select(ToDo).offset(offset).limit(limit)
        result = await session.execute(query)
        todos = result.scalars().all()
        return list(todos)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@todo_router.get("/{todo_id}", response_model=ToDoFromDB)
async def get_todo_from_id(
        todo_id: uuid.UUID,
        session: AsyncSession = Depends(get_session)
):
    try:
        query = select(ToDo).where(ToDo.id == todo_id)
        result = await session.execute(query)
        todo = result.scalar_one_or_none()

        if not todo:
            raise HTTPException(status_code=404, detail=f"ToDo with id {todo_id} not found :(")

        return todo

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@todo_router.post("/create", response_model=ToDoFromDB)
async def create_todo(
        todo: ToDoCreate,
        session: AsyncSession = Depends(get_session)
):
    try:
        new_todo = ToDo(**todo.model_dump())
        session.add(new_todo)

        await session.flush()
        await session.commit()
        await session.refresh(new_todo)

        return new_todo

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@todo_router.put("/update/{todo_id}", response_model=ToDoFromDB)
async def update_todo(
        todo_id: uuid.UUID,
        todo_update: ToDoUpdate,
        session: AsyncSession = Depends(get_session)
):
    query = select(ToDo).where(ToDo.id == todo_id)
    result = await session.execute(query)
    todo = result.scalar_one_or_none()

    if not todo:
        raise HTTPException(status_code=404, detail=f"ToDo with id {todo_id} not found :(")

    try:
        todo.title = todo_update.title
        todo.completed = todo_update.completed

        await session.commit()
        await session.refresh(todo)

        return todo

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@todo_router.delete("/delete/{todo_id}")
async def delete_todo(
        todo_id: uuid.UUID,
        session: AsyncSession = Depends(get_session),
):
    query = select(ToDo).where(ToDo.id == todo_id)
    result = await session.execute(query)
    todo = result.scalar_one_or_none()

    if not todo:
        raise HTTPException(status_code=404, detail=f"ToDo with {todo_id} id not found")

    await  session.delete(todo)
    await session.commit()

    return {"message": "Запись успешно удалена"}
