from fastapi import APIRouter

todo_router = APIRouter(prefix="/todo", tags=["Todo"])

@todo_router.get("/")
async def get_todos():
    pass

@todo_router.post("/")
async def create_todo():
    pass