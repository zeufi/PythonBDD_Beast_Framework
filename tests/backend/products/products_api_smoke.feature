
  @products_smoke  @smoke
  Feature: Product API Smoke

    @TCID-24
    Scenario: Verify 'get all products' returns the expected number of products

        Given I get number of available products from db
        When I get number of available products from api
        Then the total number of products in api should be same as in db

    @TCID-25
    Scenario: Verify 'products/id' returns a product with the given id

      Given I get 1 random product from database
      Then I verify product api returns correct product by id