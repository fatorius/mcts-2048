class Display{
    constructor(game){
        this.game = game;
        this.NUMBER_OF_CELLS = 16;
        this.NUMBER_OF_ROWS_AND_COLUMNS = parseInt(Math.sqrt(this.NUMBER_OF_CELLS));

        this.NEW_TILES_VALUES = [2, 4];
        this.NEW_TILES_WEIGHTS = [0.75, 0.25];

        this.tile_values = [];
        this.cells = [];

        this.scoreElement = document.getElementById("score");
        this.lastMove = document.getElementById("last-move");

        this.createGrid();
        this.updateDisplay();
    }

    createGrid(){
        const grid = document.getElementById("grid");
        grid.style.gridTemplateRows = `repeat(${this.NUMBER_OF_ROWS_AND_COLUMNS}, 1fr)`;
        grid.style.gridTemplateColumns = `repeat(${this.NUMBER_OF_ROWS_AND_COLUMNS}, 1fr)`;

        for (let i = 0; i < this.NUMBER_OF_CELLS; i++){

            const cell = document.createElement("div");

            cell.setAttribute("class", "cell");
            grid.appendChild(cell);

            this.cells.push(cell);
        }
    }

    updateDisplay(){
        const state = this.game.tileValues;
        this.scoreElement.innerText = this.game.getScore();

        state.forEach((tileValue, cellNumber) => {
            this.cells[cellNumber].innerHTML = "";

            if (tileValue === 0){
                return;
            }

            const newTile = this.createTileElement(tileValue);

		    this.cells[cellNumber].append(newTile);
        })
    }

    updateLastMove(lastMove){
        this.lastMove.innerHTML = lastMove
    }

    createTileElement(value){
        const tile = document.createElement("div");
        tile.classList.add("tile");
        tile.classList.add(`tile-${value}`);
        tile.innerText = value;

        return tile;
    }
}

export default Display;