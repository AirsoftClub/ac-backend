class ResourceNotFound(Exception):
    def __init__(self, resource: str):
        self.resource = resource.capitalize()


class Unauthorized(Exception):
    pass
