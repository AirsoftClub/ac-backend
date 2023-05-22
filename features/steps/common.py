import respx
import yaml
from behave import step
from deepdiff import DeepDiff
from httpx import Response


@step('I do a {verb} request to "{url}"')
def do_request(context, verb, url):
    context.response = getattr(context.client, verb.lower())(
        url, headers=context.headers
    )


@step('I do a {verb} request to "{url}" with the following data')
def do_request_with_json(context, verb, url):
    json = yaml.safe_load(context.text)
    context.response = getattr(context.client, verb.lower())(
        url, json=json, headers=context.headers
    )


@step("I get a {status_code:d} response")
def check__status_code(context, status_code):
    assert context.response.status_code == status_code, context.response.json()


@step("The response JSON is")
def check_response_json(context):
    actual = context.response.json()
    expected = yaml.safe_load(context.text)
    diff = DeepDiff(actual, expected)
    assert not diff, diff.pretty()


@step("The following HTTP mock")
def mock_request(context):
    data = yaml.safe_load(context.text)
    verb = data["verb"]
    url = data["url"]
    status_code = data["status_code"]
    json = data.get("json")
    context.request_mock = getattr(respx, verb.lower())(url).mock(
        return_value=Response(status_code, json=json)
    )


@step("The validation error response is")
def check_validation_error(context):
    data = yaml.safe_load(context.text)
    response = context.response.json()
    assert "detail" in response
    detail = response["detail"][0]
    msg = data["msg"]
    loc = data["loc"]

    assert detail["loc"] == loc, detail["loc"]
    assert detail["msg"] == msg, detail["msg"]
