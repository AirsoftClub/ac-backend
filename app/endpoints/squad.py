from app.services import SquadService
from app.schemas import AddMemberRequest, CreateSquad, SquadMembersResponse
from app.repositories import SquadRepository, UserRepository
from app.models import User
from app.dependencies import get_current_user, get_repository, get_settings
from app.core.settings import Settings
from app.core.exceptions import Unauthorized
from fastapi import APIRouter, Depends, File, UploadFile


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
):
    return squad_repository.create(squad_data, leader=current_user)


@router.put("/{squad_id}/images/")
def upload_image(
    squad_id: int,
    files: list[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    squad_repository: SquadRepository = Depends(get_repository(SquadRepository)),
    settings: Settings = Depends(get_settings),
):
    squad = squad_repository.get(squad_id)

    if squad.leader != current_user:
        raise Unauthorized

    squad_service = SquadService(squad_repository)
    squad_service.save_images(squad, files, settings.STATIC_FOLDER)

    return {"message": "Images uploaded"}
