from enum import Enum


class BehaviorEnum(Enum):
    """
    Cada um dos jogadores tem uma implementação de comportamento diferente,
    que dita as ações que eles vão tomar ao longo do jogo
    """

    IMPULSIVE = "Impulsive"
    PICKY = "Picky"
    WARY = "Wary"
    RANDOM = "Random"
