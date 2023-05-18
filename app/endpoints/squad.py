from fastapi import APIRouter, Depends

from app.dependencies import get_current_user, get_repository
from app.models import User
from app.repositories import SquadRepository, UserRepository
from app.schemas import AddMemberRequest, SquadMembersResponse

router = APIRouter()


@router.get("/", response_model=list[SquadMembersResponse])
async def get_squads(
    squad_repository: SquadRepository = Depends(get_repository(SquadRepository)),
):
    return await squad_repository.get_all()


@router.get("/{squad_id}", response_model=SquadMembersResponse)
async def get_squad(
    squad_id: int,
    squad_repository: SquadRepository = Depends(get_repository(SquadRepository)),
):
    return await squad_repository.get(squad_id)


@router.post("/{squad_id}/members/")
async def add_member(
    add_member_request: AddMemberRequest,
    squad_id: int,
    current_user: User = Depends(get_current_user),
    squad_repository: SquadRepository = Depends(get_repository(SquadRepository)),
    user_repository: UserRepository = Depends(get_repository(UserRepository)),
):
    user_id = add_member_request.user_id
    user = await user_repository.get(user_id)
    await squad_repository.add_member(squad_id, current_user, user)
    return {"message": "Member added"}
