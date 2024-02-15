# Levantamento de requisitos

## Requisito 1 - Manipulação de Timeslices
A quantidade de elementos no vetor de timeslices é dada por : DailyTimeBracket * Daytype * Season

Por padronização, definiremos o timeslice como : 0, 1, 2 ... N, onde N é o número de elementos no vetor.

Existem parâmetros que dependem do timeslice, e alguns representam relações entre o timeslice e outros fatores. Abaixo está a lista de fatores e como os mesmos se alteram a partir do timeslice. CapacityFactor, SpecifiedDemand, ProfileYearSplit. Para resolver isso, faremos uma média dos valores.

O propósito da tarefa é : Manipular o número de timeslices, fazendo mudanças nos dados que dependem dos mesmos de forma automática.

