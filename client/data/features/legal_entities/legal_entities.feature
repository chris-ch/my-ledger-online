Feature: Creating and querying legal entities
  Scenario: Creating legal entities
    Given User 'aqua' is in the system
    And User 'blue' is in the system
    When 'aqua' creates the legal entity 'Aqua corp.'
    And 'blue' creates the legal entity 'Blue & Associates'
    And 'blue' creates the legal entity 'Rainbow, llc'
    Then I should get a '200' response
    And 'aqua' should see legal entity 'Aqua corp.'
    And 'aqua' should not see legal entity 'Blue & Associates'
    And 'aqua' should not see legal entity 'Rainbow, llc'
    And 'blue' should not see legal entity 'Aqua corp.'
    And 'blue' should see legal entity 'Blue & Associates'
    And 'blue' should see legal entity 'Rainbow, llc'

