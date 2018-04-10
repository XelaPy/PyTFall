init python:
    # Special debug functions configured of global variables.
    DEBUG_SIMPY = False
    DEBUG_SIMPY_ND_BUILDING_REPORT = DSNBR = False

    # Item systems:
    AUTO_ITEM_DEBUG = False

    def simpy_debug(msg):
        if DEBUG_SIMPY:
            devlog.info("|SIMPY DEBUG| {}".format(msg))

    def aeq_debug(msg):
        if AUTO_ITEM_DEBUG:
            devlog.info("|AEQ DEBUG| {}".format(msg))
