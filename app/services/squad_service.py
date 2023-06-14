from pathlib import Path
from uuid import uuid4

from app.models import File, Squad
from app.repositories import SquadRepository


class SquadService:
    def __init__(self, squad_repository: SquadRepository):
        self.squad_repository = squad_repository

    def save_images(self, squad: Squad, files: list[File], directory: Path):
        # Create squad directory if it doesn't exist
        squad_directory = f"squads/{squad.id}"
        image_directory = directory / squad_directory
        image_directory.mkdir(exist_ok=True, parents=True)

        for f in files:
            # Define a unique image name for each file
            filename = f"{uuid4()}.jpg"  # TODO: hardcoded jpg, fix this
            with open(image_directory / filename, "wb") as image:
                image.write(f.file.read())
            squad.files.append(File(path=f"/{squad_directory}/{filename}"))

        self.squad_repository.save(squad)
