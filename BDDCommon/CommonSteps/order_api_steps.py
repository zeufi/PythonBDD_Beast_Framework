from behave import then
from BDDCommon.CommonDAO.ordersDAO import OrdersDAO


@then("I verify order is created in database")
def verify_order_is_created_in_database(context):

    db_order = OrdersDAO().get_order_by_id(context.order_id)

    assert db_order, f"Order id {context.order_id} not found in database"
    assert db_order[0]['post_type'] == 'shop_order', f"For order id '{context.order_id}', the 'post_type' field " \
           f"value is not as expected. Expected 'shop_order' actual '{db_order[0]['post_type']}'"
