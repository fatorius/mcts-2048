# Monte Carlo Tree Search (MCTS) com Value Network para 2048

Este projeto implementa uma abordagem baseada em Monte Carlo Tree Search (MCTS) para o jogo 2048.

## 🧠 Sobre o Monte Carlo Tree Search (MCTS)

O Monte Carlo Tree Search (MCTS) é um algoritmo de busca amplamente utilizado em jogos de tomada de decisão. Ele equilibra exploração e exploração ao expandir uma árvore de possíveis jogadas e simular partidas para estimar a qualidade de cada ação. O MCTS consiste em quatro etapas principais:

1. **Seleção**: Percorre a árvore escolhendo os nós com maior Upper Confidence Bound for Trees (UCT), até encontrar um nó folha.
2. **Expansão**: Se o nó selecionado não for terminal, novos nós filhos são adicionados à árvore.
3. **Simulação (Rollout)**: A partir do nó expandido, são feitas simulações de jogo para estimar a recompensa.
4. **Retropropagação**: Os resultados da simulação são propagados de volta pela árvore para atualizar as estimativas dos nós ancestrais.

No contexto deste projeto, o MCTS é utilizado para simular jogadas do 2048 e gerar dados de treinamento para a Value Network.

## 📂 Estrutura do Projeto

```
mcts-2048/
│── visualization/              # Código para visualizar a árvore do MCTS (em desenvolvimento)
│── game.py                     # Implementação do jogo 2048 e suas regras
│── mcts.py                     # Implementação do algoritmo Monte Carlo Tree Search (MCTS)
│── play.py                     # Ponto de entrada do jogo
│── train_value_network.py      # Script para treinar a Value Network
│── train_value_network.py      # Script para coletar dados de treino simulando jogos
│── README.md                   # Documentação do projeto
```

## 🚀 Como Executar o Projeto

### **1. Configuração do Ambiente**
Certifique-se de ter o Python 3.8+ instalado. Em seguida, instale as dependências:

```bash
pip install -r requirements.txt
```

### **2. Rodar o MCTS**
Para executar o MCTS no jogo 2048:

```bash
python play.py
```

Isso iniciará o jogo utilizando o MCTS para tomar decisões.

### **3. Coletar Dados para Treinamento**
Se quiser gerar dados para treinar a Value Network:

```bash
python collect_training_data.py
```

Os dados serão salvos em `data/training_data.npy`.

### **4. Treinar a Value Network**
Após gerar os dados, você pode treinar a rede neural executando:

```bash
python train_value_network.py
```

Isso criará um modelo salvo em `models/value_network.pth`.

### **5. Usar a Value Network no MCTS**
Depois de treinada, a Value Network pode ser usada para substituir os rollouts no MCTS, acelerando o processo de busca e melhorando a qualidade das decisões.

## 📌 Contribuições
Sinta-se à vontade para abrir issues e pull requests para melhorias no código e na documentação.

## 📜 Licença
Este projeto é open-source e está sob a licença MIT.
