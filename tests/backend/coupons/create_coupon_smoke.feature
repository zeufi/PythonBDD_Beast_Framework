
  @coupon  @coupon_be  @be
  Feature: Create Coupon Smoke

    @TCID-36  @TCID-37  @TCID-38  @TCID-39  @TCID-40
    Scenario Outline: Create coupon with minimum parameters should create coupon

      Given I create a "<discount_type>" coupon
      Then the coupon should exist in database

      Examples:
      | discount_type |
      | None          |
      | percent       |
      | fixed_cart    |
      | fixed_product |