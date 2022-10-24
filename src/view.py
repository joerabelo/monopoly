import operator
import statistics
from logging import WARNING
from pprint import pprint

from config import LOG_LEVEL, NUMBER_OF_RUNS
from domain.player import BehaviorEnum
from utils import print_head, print_line


def display_stdout(statistic) -> None:
    if LOG_LEVEL <= WARNING:
        print("***** Statistics *****")
        pprint(statistic)

    print_head("")
    print_head(f"RESULTADO APÓS EXECUTAR {NUMBER_OF_RUNS} SIMULAÇÕES")
    print_head("\n")

    qtd_timeout = sum(x["timeout"] for x in statistic)
    print_head("Quantas partidas terminam por time out (1000 rodadas)?")
    print_line("Total", qtd_timeout, ln_break=True)

    avg_rounds = statistics.mean([x["rounds"] for x in statistic])
    print_head("Quantos turnos em média demora uma partida?")
    print_line("Média", f"{avg_rounds:.2f}", ln_break=True)

    behaviors = {
        BehaviorEnum.IMPULSIVE.value: sum(
            x["behavior"][BehaviorEnum.IMPULSIVE.value] for x in statistic
        )
        / len(statistic)
        * 100,
        BehaviorEnum.PICKY.value: sum(
            x["behavior"][BehaviorEnum.PICKY.value] for x in statistic
        )
        / len(statistic)
        * 100,
        BehaviorEnum.WARY.value: sum(
            x["behavior"][BehaviorEnum.WARY.value] for x in statistic
        )
        / len(statistic)
        * 100,
        BehaviorEnum.RANDOM.value: sum(
            x["behavior"][BehaviorEnum.RANDOM.value] for x in statistic
        )
        / len(statistic)
        * 100,
    }
    print_head("Qual a porcentagem de vitórias por comportamento dos jogadores?")
    for behavior, percent in behaviors.items():
        print_line(behavior, f"{percent:.2f}%")
    print()

    print_head("Qual o comportamento que mais vence?")
    print_line(
        "Comportamento", sorted(behaviors.items(), key=operator.itemgetter(1)).pop()[0]
    )
