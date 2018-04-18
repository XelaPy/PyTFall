init -999 python:
    ## Should we enable the use of developer tools? This should be
    ## set to False before the game is released, so the user can't
    ## cheat using developer tools.
    config.developer = True
    # config.debug = False

    DEBUG = True # General debugging.
    DEBUG_QE = False # Debug Quests and Events
    DEBUG_PROFILING = False # Loading time of various game elements.
    DEBUG_INTERACTIONS = False

    # SimPy:
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

    # Battle Engine:
    DEBUG_BE = False
    def be_debug(msg):
        if DEBUG_BE:
            devlog.info("|BE DEBUG| {}".format(msg))

    # Simulated exploration:
    DEBUG_SE = False
