from fastapi import APIRouter, Depends

from app.dependencies import get_current_user, get_repository
from app.models import User
from app.repositories import SquadRepository, UserRepository
from app.schemas import SquadMembersResponse

router = APIRouter()


@router.get("/", response_model=list[SquadMembersResponse])
def get_squads(
    squad_repository: SquadRepository = Depends(get_repository(SquadRepository)),
):
    return squad_repository.get_all()


@router.get("/{squad_id}", response_model=SquadMembersResponse)
def get_squad(
    squad_id: int,
    squad_repository: SquadRepository = Depends(get_repository(SquadRepository)),
):
    return squad_repository.get(squad_id)


@router.post("/{squad_id}/members/{user_id}")
def add_member(
    squad_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    squad_repository: SquadRepository = Depends(get_repository(SquadRepository)),
    user_repository: UserRepository = Depends(get_repository(UserRepository)),
):
    user = user_repository.get(user_id)
    squad_repository.add_member(squad_id, current_user, user)
    return {"message": "Member added"}
