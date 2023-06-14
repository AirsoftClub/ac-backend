from pydantic import BaseModel


class File(BaseModel):
    class Config:
        orm_mode = True

    path: str


class HasFiles(BaseModel):
    """
    This works as a mixin, adding a `files` attribute to a model.
    """

    files: list[File] = []
