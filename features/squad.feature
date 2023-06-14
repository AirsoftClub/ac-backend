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
        id: 1
        emblem: emblem1
        files: []
        members:
        - full_name: Name1 Lastname1
          id: 2
      - name: Squad2
        id: 2
        emblem: emblem2
        files: []
        members: []
      - name: Squad3
        id: 3
        emblem: emblem3
        files: []
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
        - first_name: Name2
          last_name: Lastname2
          email: name2@email.com
      """
    When I do a GET request to "/squads/1"
    Then I get a 200 response
    And The response JSON is:
      """
      name: Squad1
      id: 1
      emblem: emblem1
      files: []
      members:
      - full_name: Name1 Lastname1
        id: 2
      - full_name: Name2 Lastname2
        id: 3
      """

  Scenario: Listing missing squad
    When I do a GET request to "/squads/99/"
    Then I get a 404 response
    And The response JSON is:
      """
      detail:
        - msg: Squad not found
      """

  Scenario: Adding a member to a squad
    Given These squads exists with the following data
      """
      - name: Squad1
        emblem: emblem1
        files: []
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
    And I do a GET request to "/squads/1/"
    And I get a 200 response
    And The response JSON is:
      """
      name: Squad1
      id: 1
      emblem: emblem1
      files: []
      members:
      - full_name: New Member
        id: 2
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
      detail:
       - msg: User not found
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
      detail:
        - msg: Not authorized
      """

  Scenario: Create squad
    When I do a POST request to "/squads/" with the following data:
      """
      name: New Squad
      emblem: new emblem
      """
    Then I get a 200 response
    And The response JSON is:
      """
      id: 1
      name: New Squad
      emblem: new emblem
      files: []
      members: []
      """

  Scenario: Create squad and assign members
    Given A user exists with the following data:
      """
      first_name: Some
      last_name: User
      email: some_user@email.com
      """
    When I do a POST request to "/squads/" with the following data:
      """
      name: New Squad
      emblem: new emblem
      """
    And I do a GET request to "/squads/1"
    And The response JSON is:
      """
      id: 1
      name: New Squad
      emblem: new emblem
      files: []
      members: []
      """
    And I do a POST request to "/squads/1/members/" with the following data:
      """
      user_id: 2
      """
    Then I do a GET request to "/squads/1/"
    And I get a 200 response
    And The response JSON is:
      """
      id: 1
      name: New Squad
      emblem: new emblem
      files: []
      members:
        - full_name: Some User
          id: 2
      """

  Scenario: Adding images to the squad
    Given These squads exists with the following data
      """
      - name: Squad1
        emblem: emblem1
        leader: john_doe@email.com
        members: []
      """
    Then I do a PUT request to "/squads/1/images/" with 3 images in the form data
    And I get a 200 response
    Then I do a GET request to "/squads/1/"
    And The response JSON is:
      """
      id: 1
      name: Squad1
      emblem: emblem1
      files:
        - path: /squads/1/fake_uuid4.jpg
        - path: /squads/1/fake_uuid4.jpg
        - path: /squads/1/fake_uuid4.jpg
      members: []
      """
