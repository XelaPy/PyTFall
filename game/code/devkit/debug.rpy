init -999 python:
    DEBUG = False # General debugging.
    DEBUG_QE = False # Debug Quests and Events

    # Special debug functions configured of global variables.
    DEBUG_SIMPY = False
    DEBUG_SIMPY_ND_BUILDING_REPORT = DSNBR = False
    def simpy_debug(msg):
        if DEBUG_SIMPY:
            devlog.info("|SIMPY DEBUG| {}".format(msg))

    # Item systems:
    AUTO_ITEM_DEBUG = False
    def aeq_debug(msg):
        if AUTO_ITEM_DEBUG:
            devlog.info("|AEQ DEBUG| {}".format(msg))

    DEBUG_BE = False
    def be_debug(msg):
        if DEBUG_BE:
            devlog.info("|BE DEBUG| {}".format(msg))
