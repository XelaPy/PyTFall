init python:
    # Special debug functions configured of global variables.
    DEBUG_SIMPY = False
    DEBUG_SIMPY_ND_BUILDING_REPORT = DSNBR = False

    def simpy_debug(msg):
        if DEBUG_SIMPY:
            devlog.info("|SIMPY DEBUG| {}".format(msg))
