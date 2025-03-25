import p5 from "p5";

const colors = {
    2: '#9FB798',
    4: '#788D71',
    8: '#58744e',
    16: '#58744e',
    32: '#2f4f3b',
    64: '#2e5052',
    128: '#1f1c3c',
    256: '#26143e',
    512: '#2a0730',
    1024: '#2e012a',
    2048: '#6e0516'
};

const drawing = (sketch) => {
    sketch.setup = () => {
        sketch.createCanvas(400, 400);
        sketch.rootNode = null;
        sketch.noLoop();
        sketch.redraw();
    };

    sketch.draw = () => {
        sketch.background(255, 255, 255);
        sketch.renderTree()
    };

    sketch.renderTree = () => {
        if (sketch.rootNode === null){
            return;
        }

        sketch.renderNode(sketch.rootNode, 200, 200);
    }

    sketch.renderNode = (node, startX, startY) => {
        console.log(node)
        const grid = node.gameState.tileValues;

        const cellSize = 25;
        const fontSize = 20;
        const textMargin = 10;
    
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                const value = grid[i * 4 + j];
                const x = j * (cellSize) + startX;
                const y = i * (cellSize) + startY;

                sketch.fill(colors[value] || '#ffffff');

                sketch.stroke(0);
                sketch.strokeWeight(1)

                sketch.rect(x, y, cellSize, cellSize);

                if (value) {
                    sketch.textAlign(sketch.CENTER, sketch.CENTER);
                    sketch.textSize(fontSize);
                    sketch.fill(value >= 8 ? '#f9f6f2' : '#000000');
                    sketch.text(value, x + cellSize / 2, y + cellSize / 2);
                }
            }
        }
  
        sketch.rect(startX, (25*4) + startY, 25*4, 25*2);
        sketch.fill("#000000");
        sketch.strokeWeight(0);
        sketch.textSize(fontSize / 1.75);
        sketch.text(`Visits: ${node.visits}`, startX + textMargin * 4, 25*4 + textMargin + startY);
        sketch.text(`Value: ${node.value}`, startX + textMargin * 4, 25*4 + (textMargin * 2) + startY);
    }
};

const drawingLib = new p5(drawing, "sketch");

function updateTreeVisualization(newNode) {
  	drawingLib.rootNode = newNode; 
  	drawingLib.redraw(); 
}

export {updateTreeVisualization};
