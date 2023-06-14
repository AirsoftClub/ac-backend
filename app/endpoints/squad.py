from fastapi import APIRouter, Depends

from app.core.exceptions import SquadNameAlreadyInUse
from app.dependencies import get_current_user, get_repository
from app.dependencies.db import get_db
from app.models import User
from app.models.base import SessionLocal
from app.models.squad import Squad
from app.repositories import SquadRepository, UserRepository
from app.schemas import AddMemberRequest, CreateSquad, SquadMembersResponse

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


@router.post("/{squad_id}/members/")
def add_member(
    add_member_request: AddMemberRequest,
    squad_id: int,
    current_user: User = Depends(get_current_user),
    squad_repository: SquadRepository = Depends(get_repository(SquadRepository)),
    user_repository: UserRepository = Depends(get_repository(UserRepository)),
):
    user_id = add_member_request.user_id
    user = user_repository.get(user_id)
    squad_repository.add_member(squad_id, current_user, user)
    return {"message": "Member added"}


@router.post("/", response_model=SquadMembersResponse)
def create_squad(
    squad_data: CreateSquad,
    current_user: User = Depends(get_current_user),
    squad_repository: SquadRepository = Depends(get_repository(SquadRepository)),
    db_session: SessionLocal = Depends(get_db),
):
    name_count = db_session.query(Squad).filter(Squad.name == squad_data.name).count()
    if name_count:
        raise SquadNameAlreadyInUse
    return squad_repository.create(squad_data, leader=current_user)
