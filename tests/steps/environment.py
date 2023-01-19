import time


def before_step(context, step):
    time.sleep(2)


def after_scenario(context, scenario):
    context.browser.close()
