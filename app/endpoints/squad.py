from uuid import uuid4

from fastapi import APIRouter, Depends, File, UploadFile

from app.core.exceptions import Unauthorized
from app.dependencies import get_current_user, get_repository, get_settings
from app.models import User
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
):
    return squad_repository.create(squad_data, leader=current_user)


@router.put("/{squad_id}/images/")
def upload_image(
    squad_id: int,
    current_user: User = Depends(get_current_user),
    squad_repository: SquadRepository = Depends(get_repository(SquadRepository)),
    files: list[UploadFile] = File(...),
    settings=Depends(get_settings),
):
    squad = squad_repository.get(squad_id)

    if squad.leader != current_user:
        raise Unauthorized

    # Creat squad directory if it doesn't exist
    squad_directory = settings.STATIC_FOLDER / "squads" / str(squad_id)
    squad_directory.mkdir(exist_ok=True, parents=True)

    for f in files:
        # Define a unique image name for each file
        filename = f"{uuid4()}.jpg"  # TODO: hardcoded jpg, fix this
        with open(squad_directory / filename, "wb") as image:
            image.write(f.file.read())

    return {"message": "Image uploaded"}
