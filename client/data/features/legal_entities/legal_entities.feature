Feature: Creating and querying legal entities
  Scenario: Creating legal entities
    Given User 'aqua' is in the system identified by 'aquapwd'
    And User 'blue' is in the system identified by 'bluepwd'
    When 'aqua' creates the legal entity 'Aqua corp.'
    And 'blue' creates the legal entity 'Blue & Associates'
    And 'blue' creates the legal entity 'Rainbow, llc'
    Then 'aqua' should see legal entity 'Aqua corp.'
    And 'aqua' should not see legal entity 'Blue & Associates'
    And 'aqua' should not see legal entity 'Rainbow, llc'
    And 'blue' should not see legal entity 'Aqua corp.'
    And 'blue' should see legal entity 'Blue & Associates'
    And 'blue' should see legal entity 'Rainbow, llc'

