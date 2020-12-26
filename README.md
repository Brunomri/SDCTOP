# Projeto Final - MO824A/MC859A - T�picos em Otimiza��o Combinat�ria
## Unicamp - 2� semestre de 2020

## Implementa��o de heur�stica h�brida para problema SDCTOP

### Equipe 16:

Bruno Mendes Richau - RA 157743

�rico Iago Maldonado Faustino - RA 170609

### Descri��o

O problema SDCTOP (*The Split Delivery Capacitated Team Orienteering Problem*) utiliza uma frota de ve�culos com capacidades de carga para servir um conjunto de clientes, de modo a maximizar o lucro. 
Existem restri��es no tempo m�ximo de dura��o de cada rota e na capacidade dos ve�culos. As entregas podem ser divididas permitindo que um cliente seja atendido por mais de um ve�culo. Este projeto
desenvolvido em Python implementa uma combina��o de uma heur�stica Busca Tabu e um modelo de programa��o linear inteira mista para solucionar o problema SDCTOP, embasado na proposta do artigo de refer�ncia [1](https://core.ac.uk/download/pdf/187990784.pdf).

### Refer�ncias

1. [The Split Delivery Capacitated Team Orienteering Problem](https://core.ac.uk/download/pdf/187990784.pdf)
2. [The Team Orienteering Problem: Formulations and Branch-Cut and Price](https://core.ac.uk/download/pdf/62915615.pdf)
3. [The Capacitated Team Orienteering and Profitable Tour Problems](https://www.researchgate.net/publication/220636563_The_Capacitated_Team_Orienteering_and_Profitable_Tour_Problems)
4. [The capacitated team orienteering problem](https://ink.library.smu.edu.sg/cgi/viewcontent.cgi?article=5331&context=sis_research)