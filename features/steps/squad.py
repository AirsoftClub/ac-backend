import yaml
from behave import step

from tests.factories import SquadFactory, UserFactory


@step("These squads exists with the following data")
def create_squads(context):
    data = yaml.safe_load(context.text)
    for squad_data in data:
        members_data = squad_data.pop("members", [])
        members = []
        for member in members_data:
            members.append(UserFactory(**member))

        SquadFactory(**squad_data, members=members)
