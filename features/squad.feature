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

  Scenario: Listing empty squads
    When I do a GET request to "/squads/"
    Then I get a 200 response
    And The response JSON is:
      """
      []
      """

  Scenario: Listing on particular squad
    Given These squads exists with the following data
      """
      - name: Squad1
        emblem: emblem1
        members:
        - first_name: Name1
          last_name: Lastname1
          email: name1@email.com
      """
    When I do a GET request to "/squads/1/"
    Then I get a 200 response
    And The response JSON is:
      """
      name: Squad1
      emblem: emblem1
      members:
      - full_name: Name1 Lastname1
        id: 2
      """

  Scenario: Listing missing squad
    When I do a GET request to "/squads/99/"
    Then I get a 404 response
    And The response JSON is:
      """
      detail: Squad not found
      """

  Scenario: Adding a member to a squad
    Given These squads exists with the following data
      """
      - name: Squad1
        emblem: emblem1
        members: []
        leader: john_doe@email.com
      """
    And A user exists with the following data:
      """
      first_name: New
      last_name: Member
      email: new_member@email.com
      """
    When I do a POST request to "/squads/1/members/" with the following data:
      """
      user_id: 2
      """
    Then I get a 200 response
    And The response JSON is:
      """
      message: Member added
      """

  Scenario: Adding a non existent member to a squad
    Given These squads exists with the following data
      """
      - name: Squad1
        emblem: emblem1
        members: []
        leader: john_doe@email.com
      """
    When I do a POST request to "/squads/1/members/" with the following data:
      """
      user_id: 99
      """
    Then I get a 404 response
    And The response JSON is:
      """
      detail: User not found
      """

  Scenario: Adding a member to a squad where I'm not a leader from
    Given A user exists with the following data:
      """
      email: squad1_leader@email.com
      """
    And These squads exists with the following data
      """
      - name: Squad1
        emblem: emblem1
        members: []
        leader: squad1_leader@email.com
      """
    And A user exists with the following data:
      """
      first_name: New
      last_name: Member
      email: new_member@email.com
      """
    When I do a POST request to "/squads/1/members/" with the following data:
      """
      user_id: 3
      """
    Then I get a 401 response
    And The response JSON is:
      """
      detail: Not authorized
      """