# Projeto Final - MO824A/MC859A - Tópicos em Otimização Combinatória
## Unicamp - 2º semestre de 2020

## Implementação de heurística híbrida para problema SDCTOP

### Equipe 16:

Bruno Mendes Richau - RA 157743

Érico Iago Maldonado Faustino - RA 170609

### Descrição

O problema SDCTOP (*The Split Delivery Capacitated Team Orienteering Problem*) utiliza uma frota de veículos com capacidades de carga para servir um conjunto de clientes, de modo a maximizar o lucro. 
Existem restrições no tempo máximo de duração de cada rota e na capacidade dos veículos. As entregas podem ser divididas permitindo que um cliente seja atendido por mais de um veículo. Este projeto
desenvolvido em Python implementa uma combinação de uma heurística Busca Tabu e um modelo de programação linear inteira mista para solucionar o problema SDCTOP, embasado na proposta do artigo de referência [1](https://core.ac.uk/download/pdf/187990784.pdf).

### Referências

1. [The Split Delivery Capacitated Team Orienteering Problem](https://core.ac.uk/download/pdf/187990784.pdf)
2. [The Team Orienteering Problem: Formulations and Branch-Cut and Price](https://core.ac.uk/download/pdf/62915615.pdf)