import yaml
from behave import step

from app.repositories import UserRepository
from tests.factories import SquadFactory, UserFactory


@step("These squads exists with the following data")
def create_squads(context):
    data = yaml.safe_load(context.text)
    for squad_data in data:
        members_data = squad_data.pop("members", [])
        members = []
        for member in members_data:
            members.append(UserFactory(**member))
        leader = squad_data.pop("leader", None)

        if leader:
            leader = UserRepository(context.session).get_by_email(leader)
            SquadFactory(**squad_data, members=members, leader=leader)
        else:
            SquadFactory(**squad_data, members=members)
