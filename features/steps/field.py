import yaml
from behave import step

from tests.factories import FieldFactory, TagFactory


@step("These field exists with the following data")
def create_field(context):
    data = yaml.safe_load(context.text)
    for field_data in data:
        tags_data = field_data.pop("tags", [])
        tags = []
        for tag in tags_data:
            tags.append(TagFactory(**tag))
        FieldFactory(**field_data, tags=tags)
