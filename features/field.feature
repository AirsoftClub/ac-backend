Feature: API Fields

  Background: I am logged in
    Given A user exists with the following data:
      """
      first_name: John
      last_name: Doe
      email: john_doe@email.com
      """
    And I am logged with the email john_doe@email.com

  Scenario: Listing all fields
    Given These field exists with the following data
      """
      - name: Field1
        description: Description Field1
        tags: []
        deleted_at: 2020-01-01
        latitude: 1.23456789
        longitude: 9.87654321
      - name: Field2
        description: Description Field2
        tags: []
        latitude: 1.23456789
        longitude: 9.87654321
      - name: Field3
        description: Description Field3
        tags: []
        latitude: 1.23456789
        longitude: 9.87654321
      """
    When I do a GET request to "/fields"
    Then I get a 200 response
    And The response JSON is:
      """
      - id: 3
        name: Field3
        description: Description Field3
        tags: []
        latitude: 1.23456789
        longitude: 9.87654321
      - id: 2
        name: Field2
        description: Description Field2
        tags: []
        latitude: 1.23456789
        longitude: 9.87654321
      """

  Scenario: Listing empty Fields
    When I do a GET request to "/fields"
    Then I get a 200 response
    And The response JSON is:
      """
      []
      """

  Scenario: Listing one particular Field
    Given These field exists with the following data
      """
      - id: 1
        name: Field1
        description: Description Field1
        tags: []
        latitude: 1.23456789
        longitude: 9.87654321
      """
    When I do a GET request to "/fields/1"
    Then I get a 200 response
    And The response JSON is:
      """
      id: 1
      name: Field1
      description: Description Field1
      latitude: 1.23456789
      longitude: 9.87654321
      tags: []
      """

  Scenario: Missing Field
    When I do a GET request to "/fields/99"
    Then I get a 404 response
    And The response JSON is:
      """
      detail: Field not found
      """

  Scenario: Listing empty Fields by tag
    Given These field exists with the following data
      """
      - id: 1
        name: Field1
        description: Description Field1
        latitude: 1.23456789
        longitude: 9.87654321
        tags:
          - description: Tag1
      """
    When I do a GET request to "/fields/tag/1"
    Then I get a 200 response
    And The response JSON is:
      """
      - id: 1
        name: Field1
        description: Description Field1
        tags:
          - id: 1
            description: Tag1
        latitude: 1.23456789
        longitude: 9.87654321
      """

  Scenario: Listing Field by location
    Given These field exists with the following data
      """
      - id: 1
        name: Field1
        description: Description Field1
        latitude: 0.0
        longitude: 0.0
        tags: []
      - id: 2
        name: Field2
        description: Description Field2
        latitude: 1.1
        longitude: 2.2
        tags: []
      """
    When I do a GET request to "/fields/location?latitude=1.23456789&longitude=9.87654321"
    Then I get a 200 response
    And The response JSON is:
      """
      - id: 2
        name: Field2
        description: Description Field2
        latitude: 1.1
        longitude: 2.2
        distance: 853.54623
        tags: []
      - id: 1
        name: Field1
        description: Description Field1
        tags: []
        latitude: 0.0
        longitude: 0.0
        distance: 1106.6836
      """
