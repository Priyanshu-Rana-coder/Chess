from pydantic import BaseModel

class MoveResponse(BaseModel):
    success: bool
    board: list[list[str]]
    white_move: bool
    check: bool
    checkmate: bool
    stalemate: bool
    state: int