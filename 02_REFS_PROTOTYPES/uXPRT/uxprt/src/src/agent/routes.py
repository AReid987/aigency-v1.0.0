from fastapi import APIRouter

router = APIRouter()

@router.post("/chat")
async def chat():
    # TODO: Implement chat logic
    pass

# Optional endpoints
# @router.get("/state")
# async def get_state():
#     # TODO: Implement get state logic
#     pass

# @router.post("/command")
# async def handle_command():
#     # TODO: Implement handle command logic
#     pass