# Desafio Python

Criar um jogo hipotético muito semelhante ao Banco Imobiliário para simular um número determinado de partidas e ao final exibir um relatório estatístico simples.

## Requisitos
- pdm

## Instalação

```console
make install
```

## Execução
```console
make run
```

## Testes
```console
make test
```

## Configurações opicionais

- LOG_LEVEL - Nível de exibição dos logs. Default 40 (ERROR)
- NUMBER_OF_RUNS = Número de simulações de partidas. Default 300
- DEFAULT_BALANCE = Saldo inicial dos jogadores. Default 300

Exemplos
```console
export LOG_LEVEL=40
export NUMBER_OF_RUNS=300
export DEFAULT_BALANCE=300
make run
```
