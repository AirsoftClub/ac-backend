class ResourceNotFound(Exception):
    def __init__(self, resource: str):
        self.resource = resource.capitalize()


class Unauthenticated(Exception):
    pass


class Unauthorized(Exception):
    pass
