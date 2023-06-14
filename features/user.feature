Feature: User

  Scenario: Logged user access their profile
    Given A user exists with the following data:
      """
      first_name: John
      last_name: Doe
      email: john_doe@email.com
      """
    And I am logged with the email john_doe@email.com
    When I do a GET request to "/user/me"
    Then I get a 200 response
    And The response JSON is:
      """
      first_name: John
      last_name: Doe
      email: john_doe@email.com
      image:
      squads: []
      """

  Scenario: Unauthorized user without headers
    When I do a GET request to "/user/me"
    Then I get a 401 response
    And The response JSON is:
      """
      detail:
        - msg: Missing Authorization Header
      """

  Scenario: Unauthorized user with invalid headers
    Given I set the Authorization header to Bearer invalid-token
    When I do a GET request to "/user/me"
    Then I get a 422 response
    And The response JSON is:
      """
      detail:
        - msg: Not enough segments
      """

  Scenario: Logged with deleted user
    Given A user exists with the following data:
      """
      first_name: John
      last_name: Doe
      email: john_doe@email.com
      deleted_at: 2021-01-01T00:00:00Z
      """
    And I am logged with the email john_doe@email.com
    When I do a GET request to "/user/me"
    Then I get a 404 response
    And The response JSON is:
      """
      detail:
          - msg: User not found
      """
