import log
from config import LOG_LEVEL

logger = log.init_logger(__name__, LOG_LEVEL)

from .__behavior_enum import BehaviorEnum  # noqa: F401, E402
from .__player_abstract import PlayerAbstract  # noqa: F401, E402
from .__player_factory import PlayerFactory  # noqa: F401, E402
