def assert_response(response, error_loc, error_msg):
    assert "detail" in response, "Response does not contain 'detail' key"
    error_list = response["detail"]

    for error in error_list:
        if error["loc"] == error_loc and error["msg"] == error_msg:
            return

    raise AssertionError(
        f"Expected loc='{error_loc}' and msg='{error_msg}' not found in response"
    )
