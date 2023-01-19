
  Feature: Verify different fields of create coupon

    @TCID-43
    Scenario: Verify the given coupon metadata are recorded correctly


      Given I create a coupon with given parameters
             """
             {"discount_type": "fixed_cart",
             "amount": "50",
             "individual_use": "false",
             "usage_count": 10,
             "usage_limit": 5,
             "exclude_sale_items": "True"
             }
            """

      Then I verify the given metadata in database
            """
            {"discount_type": "fixed_cart",
            "coupon_amount": "50",
            "individual_use": "no",
            "usage_limit": "5",
            "usage_count": "0",
            "usage_limit_per_user": "0",
            "date_expires": "None",
            "exclude_sale_items": "yes"
            }
            """