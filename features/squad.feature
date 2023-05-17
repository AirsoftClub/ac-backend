Feature: Squad API

  Background: I am logged in
    Given A user exists with the following data:
      """
      first_name: John
      last_name: Doe
      email: john_doe@email.com
      """
    And I am logged with the email john_doe@email.com

  Scenario: Listing all fields
    Given These squads exists with the following data
      """
      - name: Squad1
        emblem: emblem1
        members:
        - first_name: Name1
          last_name: Lastname1
          email: name1@email.com
      - name: Squad2
        emblem: emblem2
      - name: Squad3
        emblem: emblem3
        members:
        - first_name: Name2
          last_name: Lastname2
          email: name2@email.com
      """
    When I do a GET request to "/squads/"
    Then I get a 200 response
    And The response JSON is:
      """
      - name: Squad1
        emblem: emblem1
        members:
        - full_name: Name1 Lastname1
          id: 2
      - name: Squad2
        emblem: emblem2
        members: []
      - name: Squad3
        emblem: emblem3
        members:
        - full_name: Name2 Lastname2
          id: 5
      """
