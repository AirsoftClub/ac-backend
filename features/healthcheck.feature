Feature:

  Scenario: Healtcheck works
    When I do a GET request to "/health"
    Then I get a 200 response
    And the response JSON is
      """
      database: online
      """
