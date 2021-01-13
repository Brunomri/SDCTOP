# Projeto Final - MO824A/MC859A - T�picos em Otimiza��o Combinat�ria
## Unicamp - 2� semestre de 2020

## Implementa��o de heur�stica h�brida para problema SDCTOP

### Equipe 16:

Bruno Mendes Richau - RA 157743

�rico Iago Maldonado Faustino - RA 170609

### Descri��o

O problema SDCTOP (*The Split Delivery Capacitated Team Orienteering Problem*) utiliza uma frota de ve�culos com capacidades de carga para servir um conjunto de clientes, de modo a maximizar o lucro. 
Existem restri��es no tempo m�ximo de dura��o de cada rota e na capacidade dos ve�culos. As entregas podem ser fracionadas, permitindo que um cliente seja atendido por mais de um ve�culo. No entanto, o lucro de cada cliente atendido
dever� ser coletado uma �nica vez, quando sua demanda for completamente atendida. Este projeto desenvolvido em Python implementa uma heur�stica Busca Tabu 
para solucionar o problema SDCTOP, embasado na proposta do artigo de refer�ncia [[1]](https://core.ac.uk/download/pdf/187990784.pdf).

### Utiliza��o

H� dois modos de execu��o do programa. O primeiro deles gera uma nova inst�ncia, um grafo orientado representando a rede de clientes e o dep�sito. O lucro e a demanda
associados a cada v�rtice e o tempo associado a cada aresta s�o gerados aleatoriamente. O grafo � salvo no diret�rio raiz do projeto em um arquivo .gpl
gerado pela biblioteca *Networkx* [[5]](https://networkx.org/), podendo ser importado em uma execu��o posterior.

```
python sdctop.py -c <#clientes> <capacidade> <#veiculos> <tempo_limite>
```

Par�metros de execu��o:
- -c: modo para cria��o de uma nova inst�ncia (novo grafo)
- #clientes: n�mero de potenciais clientes existentes na rede
- capacidade: capacidade m�xima de cada ve�culo
- #veiculos: n�mero de ve�culos dispon�veis
- tempo_limite: tempo m�ximo de dura��o de cada rota

O segundo modo permite a importa��o de uma inst�ncia gerada anteriormente a partir do modo de execu��o anterior.

```
python sdctop.py -g <arquivo_gpl> <capacidade> <#veiculos> <tempo_limite>
```

Par�metros de execu��o:
- -g: modo para importa��o de uma inst�ncia j� existente (grafo salvo no formato .gpl)
- arquivo_gpl: caminho do arquivo .gpl que representa uma inst�ncia
- capacidade: capacidade m�xima de cada ve�culo
- #veiculos: n�mero de ve�culos dispon�veis
- tempo_limite: tempo m�ximo de dura��o de cada rota

Em ambos os modos, um arquivo results.csv � gerado no diret�rio raiz do projeto, contendo informa��es sobre a solu��o encontrada. Caso n�o exista
solu��o para uma determinada combina��o de inst�ncia e restri��es, uma mensagem de erro aparecer� no console. A execu��o ser� abortada e nenhum resultado ser� armazenado.

### Refer�ncias

1. [The Split Delivery Capacitated Team Orienteering Problem](https://core.ac.uk/download/pdf/187990784.pdf)
2. [The Team Orienteering Problem: Formulations and Branch-Cut and Price](https://core.ac.uk/download/pdf/62915615.pdf)
3. [The Capacitated Team Orienteering and Profitable Tour Problems](https://www.researchgate.net/publication/220636563_The_Capacitated_Team_Orienteering_and_Profitable_Tour_Problems)
4. [The capacitated team orienteering problem](https://ink.library.smu.edu.sg/cgi/viewcontent.cgi?article=5331&context=sis_research)
5. [Networkx - Network Analysis in Python](https://networkx.org/)