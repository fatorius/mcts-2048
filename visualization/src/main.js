import Display from "./display";
import Game from "./game";
import MCTS from "./mcts";

import { updateTreeVisualization } from "./sketch";

import "./style.css";

const game = new Game();
const display = new Display(game);

document.getElementById("start").onclick = () => {
	display.updateDisplay(game);

    const mcts = new MCTS(80000);
    const result = mcts.search(game);

	updateTreeVisualization(mcts.rootNode);

    display.updateLastMove(result.action);

    game.applyAction(result.action);
	display.updateDisplay(game);
}


