import logging
import os

# SYSTEM
LOG_LEVEL = int(os.getenv("LOG_LEVEL", logging.ERROR))

# APP
NUMBER_OF_RUNS = int(os.getenv("NUMBER_OF_RUNS", 300))
DEFAULT_BALANCE = float(os.getenv("DEFAULT_BALANCE", 300.0))
QUANTITY_ESTATES = int(os.getenv("QUANTITY_ESTATES", 20))
