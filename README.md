# Monte Carlo Tree Search (MCTS) com Value Network para 2048

Este projeto implementa uma abordagem baseada em Monte Carlo Tree Search (MCTS) para o jogo 2048.

## 🧠 Sobre o Monte Carlo Tree Search (MCTS)

O Monte Carlo Tree Search (MCTS) é um algoritmo de busca amplamente utilizado em jogos de tomada de decisão. Ele equilibra exploração e exploração ao expandir uma árvore de possíveis jogadas e simular partidas para estimar a qualidade de cada ação. O MCTS consiste em quatro etapas principais:

1. **Seleção**: Percorre a árvore escolhendo os nós com maior Upper Confidence Bound for Trees (UCT), até encontrar um nó folha.

2. **Expansão**: Se o nó selecionado não for terminal, novos nós filhos são adicionados à árvore.

3. **Simulação (Rollout)**: A partir do nó expandido, são feitas simulações de jogo para estimar a recompensa.

4. **Retropropagação**: Os resultados da simulação são propagados de volta pela árvore para atualizar as estimativas dos nós ancestrais.

No contexto deste projeto, o MCTS é utilizado para simular jogadas do 2048 e gerar dados de treinamento para a Value Network.

## Estrutura do Projeto

- `game.py` - Implementação do jogo 2048 e suas regras.
- `mcts.py` - Implementação do algoritmo Monte Carlo Tree Search (MCTS).
- `play.py` - Ponto de entrada do jogo.
- `/visualization` - Código para visualizar a árvore no seu navegador (em desenvolvimento)

## Como Funciona

### 1. Execução do MCTS
O algoritmo MCTS é utilizado para simular jogos e determinar a melhor ação a ser tomada com base nas explorações da árvore de busca.

### 2. Heuristica usada
O algoritmo avalia o quanto a linha é promissora através de uma heurística com base na quantidade de células no tabuleiro e na pontuação geral.

### 3. Value network baseada em CNN (em desenvolvimento)
A Value Network é treinada supervisionadamente com os dados coletados para aprender a avaliar estados do jogo sem precisar rodar o MCTS. Após o treinamento, a Value Network pode substituir a simulação do MCTS durante a busca, permitindo decisões mais rápidas.

## Contribuições
Sinta-se à vontade para abrir issues e pull requests para melhorias no código e na documentação.

## Licença
Este projeto é open-source e está sob a licença MIT.

