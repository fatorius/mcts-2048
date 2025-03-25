import { getRandomFromArray, getRandomFromArrayWithWeights } from "./random";

class Game {
    constructor(tileValues = null) {
        this.NUMBER_OF_CELLS = 16;
        this.NUMBER_OF_ROWS_AND_COLUMNS = Math.sqrt(this.NUMBER_OF_CELLS);
        
        this.NEW_TILES_VALUES = [2, 4];
        this.NEW_TILES_WEIGHTS = [0.75, 0.25];
        
        this.tileValues = tileValues ? [...tileValues] : [];
        this.score = 0;

        if (!tileValues) {
            this.initGrid();
            this.initTiles();
        }

        this.updateScore();
    }

    clone() {
        return new Game(this.tileValues);
    }

    setState(state) {
        this.tileValues = state;
        this.updateScore();
    }

    initGrid() {
        this.tileValues = Array(this.NUMBER_OF_CELLS).fill(0);
    }

    initTiles() {
        let emptyCells = [...Array(this.NUMBER_OF_CELLS).keys()];
        let chosenCells = emptyCells.sort(() => 0.5 - Math.random()).slice(0, 2);
        
        chosenCells.forEach(cellNumber => {
            this.tileValues[cellNumber] = getRandomFromArrayWithWeights(this.NEW_TILES_VALUES, this.NEW_TILES_WEIGHTS);
        });
    }

    getEmptyCells() {
        return this.tileValues.map((val, index) => val === 0 ? index : -1).filter(index => index !== -1);
    }

    generateNewTile() {
        let newCell = getRandomFromArray(this.getEmptyCells());
        let tileValue = getRandomFromArrayWithWeights(this.NEW_TILES_VALUES, this.NEW_TILES_WEIGHTS);
        this.tileValues[newCell] = tileValue;
        this.updateScore();
    }

    getPossibleActions() {
        let actions = new Set();
        
        for (let pos = 0; pos < this.NUMBER_OF_CELLS; pos++) {
            if (this.tileValues[pos] === 0) continue;
            if (this.findRightmostAvailableTile(pos, this.tileValues[pos]) !== pos) actions.add("right");
            if (this.findLeftmostAvailableTile(pos, this.tileValues[pos]) !== pos) actions.add("left");
            if (this.findTopmostAvailableTile(pos, this.tileValues[pos]) !== pos) actions.add("up");
            if (this.findBottommostAvailableTile(pos, this.tileValues[pos]) !== pos) actions.add("down");
        }
        
        return Array.from(actions);
    }

    getScore(){
        this.updateScore();
        return this.score;
    }

    updateScore() {
        this.score = this.tileValues.reduce((sum, val) => sum + val, 0);
    }

    findLeftmostAvailableTile(pos, value) {
        while (pos % this.NUMBER_OF_ROWS_AND_COLUMNS !== 0) {
            let newPos = pos - 1;
            if (this.tileValues[newPos] !== 0 && this.tileValues[newPos] !== value) break;
            pos = newPos;
        }
        return pos;
    }

    findTopmostAvailableTile(pos, value) {
        while (pos >= this.NUMBER_OF_ROWS_AND_COLUMNS) {
            let newPos = pos - this.NUMBER_OF_ROWS_AND_COLUMNS;
            if (this.tileValues[newPos] !== 0 && this.tileValues[newPos] !== value) break;
            pos = newPos;
        }
        return pos;
    }

    findRightmostAvailableTile(pos, value) {
        while ((pos + 1) % this.NUMBER_OF_ROWS_AND_COLUMNS !== 0) {
            let newPos = pos + 1;
            if (this.tileValues[newPos] !== 0 && this.tileValues[newPos] !== value) break;
            pos = newPos;
        }
        return pos;
    }

    findBottommostAvailableTile(pos, value) {
        while (pos < this.NUMBER_OF_CELLS - this.NUMBER_OF_ROWS_AND_COLUMNS) {
            let newPos = pos + this.NUMBER_OF_ROWS_AND_COLUMNS;
            if (this.tileValues[newPos] !== 0 && this.tileValues[newPos] !== value) break;
            pos = newPos;
        }
        return pos;
    }

    moveTileTo(start, destination) {
        if (start === destination) return;
        let value = this.tileValues[start];
        let destinationValue = this.tileValues[destination];
        let newValue = destinationValue === value ? value * 2 : value;
        this.tileValues[start] = 0;
        this.tileValues[destination] = newValue;
    }

    moveLeft() {
        for (let pos = 0; pos < this.NUMBER_OF_CELLS; pos++) {
            if (this.tileValues[pos] === 0) continue;
            let destination = this.findLeftmostAvailableTile(pos, this.tileValues[pos]);
            this.moveTileTo(pos, destination);
        }
    }

    moveUp() {
        for (let pos = 0; pos < this.NUMBER_OF_CELLS; pos++) {
            if (this.tileValues[pos] === 0) continue;
            let destination = this.findTopmostAvailableTile(pos, this.tileValues[pos]);
            this.moveTileTo(pos, destination);
        }
    }

    moveRight() {
        for (let pos = this.NUMBER_OF_CELLS - 1; pos >= 0; pos--) {
            if (this.tileValues[pos] === 0) continue;
            let destination = this.findRightmostAvailableTile(pos, this.tileValues[pos]);
            this.moveTileTo(pos, destination);
        }
    }

    moveDown() {
        for (let pos = this.NUMBER_OF_CELLS - 1; pos >= 0; pos--) {
            if (this.tileValues[pos] === 0) continue;
            let destination = this.findBottommostAvailableTile(pos, this.tileValues[pos]);
            this.moveTileTo(pos, destination);
        }
    }

    applyAction(action){
        switch (action){
            case "up":
                this.moveUp();
                this.generateNewTile();
                break;
            case "down":
                this.moveDown();
                this.generateNewTile();
                break;
            case "right":
                this.moveRight();
                this.generateNewTile();
                break;
            case "left":
                this.moveLeft();
                this.generateNewTile();
                break;
        }
    }

    showTable() {
        console.log(`Pontuação: ${this.score}`);
        for (let i = 0; i < this.NUMBER_OF_ROWS_AND_COLUMNS; i++) {
            console.log(this.tileValues.slice(i * 4, (i + 1) * 4).join(" "));
        }
    }
}

export default Game