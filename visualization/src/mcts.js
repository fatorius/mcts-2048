class MCTSNode {
    constructor(gameState, parent = null, isPlayerTurn = true) {
        this.gameState = gameState;
        this.parent = parent;
        this.children = {};
        this.isPlayerTurn = isPlayerTurn;
        this.visits = 0;
        this.value = 0;
    }

    uct(explorationWeight = Math.sqrt(2)) {
        if (this.visits === 0) {
            return Infinity;
        }

        const exploitation = this.value / this.visits;
        const exploration = explorationWeight * Math.sqrt(Math.log(this.parent.visits + 1) / this.visits);

        return exploitation + exploration;
    }

    isFullyExpanded() {
        return Object.keys(this.children).length === 4;
    }

    bestChild(explorationWeight = 1.0) {
        return Object.values(this.children).reduce((best, child) => {
            const score = child.value / (child.visits + 1e-6) + 
                explorationWeight * Math.sqrt(Math.log(this.visits + 1) / (child.visits + 1e-6));
            return score > best.score ? { node: child, score } : best;
        }, { node: null, score: -Infinity }).node;
    }

    bestAction(explorationWeight = 1.0) {
        return Object.entries(this.children).reduce((best, [action, child]) => {
            const score = child.value / (child.visits + 1e-6) + 
                explorationWeight * Math.sqrt(Math.log(this.visits + 1) / (child.visits + 1e-6));
            return score > best.score ? { action, score } : best;
        }, { action: null, score: -Infinity }).action;
    }

    selectChild() {
        if (this.isPlayerTurn) {
            return this.bestAction();
        } else {
            const actions = Object.entries(this.children);
            return actions[Math.floor(Math.random() * actions.length)];
        }
    }

    addChild(action, childNode) {
        this.children[action] = childNode;
    }
}

class MCTS {
    constructor(iterations = 1000) {
        this.iterations = iterations;
        this.rootNode;
    }

    search(rootState) {
        this.rootNode = new MCTSNode(rootState);

        for (let i = 0; i < this.iterations; i++) {
            let node = this.rootNode;
            let state = rootState.clone()

            // Selection
            while (!this.isTerminal(state)) {
                if (!Object.keys(node.children).length || (node.parent && node.uct() > Math.max(...Object.values(node.children).map(child => child.uct())))) {
                    break;
                }

                if (!node.isFullyExpanded()) {
                    this.expand(node);
                    break;
                }

                const action = node.selectChild();
                node = node.children[action];
                state = this.applyAction(state, action);
            }

            // Expansion
            if (!this.isTerminal(state)) {
                this.expand(node);
            }

            // Simulation
            const rolloutResult = this.rollout(state);

            // Backpropagation
            this.backpropagate(node, rolloutResult);
        }

        return { action: this.rootNode.bestAction(0), state: this.rootNode.bestChild(0) };
    }

    expand(node) {
        if (node.isPlayerTurn) {
            for (const action of this.getPossibleActions(node.gameState)) {
                if (!(action in node.children)) {
                    let nextState = node.gameState.clone();
                    this.applyAction(nextState, action);
                    const childNode = new MCTSNode(nextState, node, false);
                    node.addChild(action, childNode);
                }
            }
        } else {
            const emptyCells = node.gameState.getEmptyCells();
            for (const cell of emptyCells) {
                for (const value of [2, 4]) {
                    let nextState = node.gameState.clone();
                    nextState.tileValues[cell] = value;
                    nextState.updateScore();
                    const childNode = new MCTSNode(nextState, node, true);
                    node.addChild([cell, value], childNode);
                }
            }
        }
    }

    getPossibleActions(gameState) {
        return gameState.getPossibleActions();
    }

    applyAction(gameState, action) {
        if (action === 'up') {
            gameState.moveUp();
        } else if (action === 'down') {
            gameState.moveDown();
        } else if (action === 'left') {
            gameState.moveLeft();
        } else if (action === 'right') {
            gameState.moveRight();
        }
        return gameState;
    }

    isTerminal(gameState) {
        return this.getPossibleActions(gameState).length === 0;
    }

    rollout(gameState, maxRolloutDepth = 20) {
        for (let i = 0; i < maxRolloutDepth; i++) {
            const possibleActions = this.getPossibleActions(gameState);
            if (!possibleActions.length) {
                break;
            }
            const action = possibleActions[Math.floor(Math.random() * possibleActions.length)];
            this.applyAction(gameState, action);
        }

        const nonZeroTiles = gameState.tileValues.filter(v => v > 0).length;
        return 1 / nonZeroTiles;
    }

    backpropagate(node, reward) {
        while (node !== null) {
            node.visits += 1;
            node.value += reward;
            node = node.parent;
        }
    }
}

export default MCTS