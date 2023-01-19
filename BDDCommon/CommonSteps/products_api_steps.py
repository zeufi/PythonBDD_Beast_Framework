from behave import step
from BDDCommon.CommonDAO.productsDAO import ProductsDAO
from BDDCommon.CommonAPI import products_api


@step("I get number of available products from db")
def i_get_number_of_available_products_from_db(context):
    """

    """
    # get all available products with SQL
    all_rows = ProductsDAO().get_app_products_from_db()
    print("")
    print("Number of products in db: {}".format(len(all_rows)))
    # then set the number available product as context varialbe
    context.qty_products_db = len(all_rows)


@step("I get number of available products from api")
def i_get_number_of_available_products_from_api(context):
    """

    """
    # call api
    list_of_products = products_api.list_all_products()
    number_of_products_in_api = len(list_of_products)
    print("")
    print("Number of products in API: {}".format(number_of_products_in_api))

    # set context variable with numver of products
    context.qty_products_api = number_of_products_in_api


@step("the total number of products in api should be same as in db")
def the_total_number_of_products_in_api_should_be_same_as_in_db(context):

    assert context.qty_products_api == context.qty_products_db, \
        "The number of products in db and in api response do not match." \
        "DB qty: {}, API qty: {}".format(context.qty_products_db, context.qty_products_api)


@step("I get {qty} random product from database")
def i_get_random_product_from_database(context, qty):

    context.random_products = ProductsDAO().get_random_products_from_db(qty)


@step("I verify product api returns correct product by id")
def i_verify_product_api_returns_correct_product_by_id(context):

    product_id = context.random_products[0]['ID']

    rs_get_product = products_api.get_product_by_id(product_id)

    assert rs_get_product['id'] == product_id, "Wrong product id when calling 'get product by id'."
    assert rs_get_product['name'] == context.random_products[0]['post_title'], \
        "Wrong product name when calling 'get product by id'. Api: {}," \
        " DB: {}".format(rs_get_product['name'], context.random_products[0]['post_title'])
