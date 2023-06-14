Feature: Auth process

  Scenario: Successful registration
    Given The following HTTP mock
      """
      verb: GET
      url: https://www.googleapis.com/oauth2/v3/userinfo
      status_code: 200
      json:
          given_name: John
          family_name: Doe
          email: johd@email.com
          picture: https://website.com/image.png
      """
    And The JWT generates the following data:
      """
      access_token: access-token
      refresh_token: refresh-token
      expires_at: 123
      """
    When I do a POST request to "/auth/register" with the following data
      """
      token: valid-token
      provider: google
      """
    Then I get a 200 response
    And The response JSON is:
      """
      access_token: access-token
      refresh_token: refresh-token
      expires_at: 123
      """

  Scenario: Failed registration by provider
    Given The following HTTP mock
      """
      verb: GET
      url: https://www.googleapis.com/oauth2/v3/userinfo
      status_code: 401
      """
    When I do a POST request to "/auth/register" with the following data
      """
      token: valid-token
      provider: google
      """
    Then I get a 403 response
    And The response JSON is:
      """
      detail:
      - msg: Not authenticated
      """

  Scenario Outline: Failed registration by missing params
    When I do a POST request to "/auth/register" with the following data
      """
      token: <token>
      provider: <provider>
      """
    Then I get a 422 response
    And The validation error response is:
      """
      msg: "<msg>"
      loc: <loc>
      """

    Examples:
      | token       | provider | msg                                                                      | loc                  |
      |             | google   | none is not an allowed value                                             | ['body', 'token']    |
      | valid-token |          | none is not an allowed value                                             | ['body', 'provider'] |
      | valid-token | foo      | value is not a valid enumeration member; permitted: 'google', 'facebook' | ['body', 'provider'] |

# TODO: add tests for refresh token
