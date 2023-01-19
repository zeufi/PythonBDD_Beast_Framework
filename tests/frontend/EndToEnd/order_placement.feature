

  Feature: Order Placement

    @TCID-33
    Scenario: New user place order with 1 item without creating an account

      Given I go to 'home' page
      When I add 1 random item to cart from the homepage
      And I click on cart in the top nav bar and verify cart page opens
      And I select 'Free shipping' option
      And I click on 'Proceed to checkout' button in the cart page
      And I verify 'Checkout' page is loaded
      And I fill in the billing details form
      And I click on 'Place order' button in the checkout page
      Then order received page should load with correct data
      Then I verify order is created in database