# Projeto Final - MO824A/MC859A - Tópicos em Otimização Combinatória
## Unicamp - 2º semestre de 2020

## Implementação de heurística híbrida para problema SDCTOP

### Equipe 16:

Bruno Mendes Richau - RA 157743

Érico Iago Maldonado Faustino - RA 170609

### Descrição

O problema SDCTOP (*The Split Delivery Capacitated Team Orienteering Problem*) utiliza uma frota de veículos com capacidades de carga para servir um conjunto de clientes, de modo a maximizar o lucro. 
Existem restrições no tempo máximo de duração de cada rota e na capacidade dos veículos. As entregas podem ser fracionadas, permitindo que um cliente seja atendido por mais de um veículo. No entanto, o lucro de cada cliente atendido
deverá ser coletado uma única vez, quando sua demanda for completamente atendida. Este projeto desenvolvido em Python implementa uma heurística Busca Tabu 
para solucionar o problema SDCTOP, embasado na proposta do artigo de referência [[1]](https://core.ac.uk/download/pdf/187990784.pdf).

### Utilização

Há dois modos de execução do programa. O primeiro deles gera uma nova instância, um grafo orientado representando a rede de clientes e o depósito. O lucro e a demanda
associados a cada vértice e o tempo associado a cada aresta são gerados aleatoriamente. O grafo é salvo no diretório raiz do projeto em um arquivo .gpl
gerado pela biblioteca *Networkx* [[5]](https://networkx.org/), podendo ser importado em uma execução posterior.

```
python sdctop.py -c <#clientes> <capacidade> <#veiculos> <tempo_limite>
```

Parâmetros de execução:
- -c: modo para criação de uma nova instância (novo grafo)
- #clientes: número de potenciais clientes existentes na rede
- capacidade: capacidade máxima de cada veículo
- #veiculos: número de veículos disponíveis
- tempo_limite: tempo máximo de duração de cada rota

O segundo modo permite a importação de uma instância gerada anteriormente a partir do modo de execução anterior.

```
python sdctop.py -g <arquivo_gpl> <capacidade> <#veiculos> <tempo_limite>
```

Parâmetros de execução:
- -g: modo para importação de uma instância já existente (grafo salvo no formato .gpl)
- arquivo_gpl: caminho do arquivo .gpl que representa uma instância
- capacidade: capacidade máxima de cada veículo
- #veiculos: número de veículos disponíveis
- tempo_limite: tempo máximo de duração de cada rota

Em ambos os modos, um arquivo results.csv é gerado no diretório raiz do projeto, contendo informações sobre a solução encontrada. Caso não exista
solução para uma determinada combinação de instância e restrições, uma mensagem de erro aparecerá no console. A execução será abortada e nenhum resultado será armazenado.

### Referências

1. [The Split Delivery Capacitated Team Orienteering Problem](https://core.ac.uk/download/pdf/187990784.pdf)
2. [The Team Orienteering Problem: Formulations and Branch-Cut and Price](https://core.ac.uk/download/pdf/62915615.pdf)
3. [The Capacitated Team Orienteering and Profitable Tour Problems](https://www.researchgate.net/publication/220636563_The_Capacitated_Team_Orienteering_and_Profitable_Tour_Problems)
4. [The capacitated team orienteering problem](https://ink.library.smu.edu.sg/cgi/viewcontent.cgi?article=5331&context=sis_research)
5. [Networkx - Network Analysis in Python](https://networkx.org/)