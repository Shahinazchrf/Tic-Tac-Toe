// ========================================
// BOARD LOGIC
// ========================================

const Board = {
    cells: Array(9).fill(null),
    cellsElement: document.getElementById('cells'),
    winlineElement: document.getElementById('winline'),
    
    init() {
        this.cells = Array(9).fill(null);
        this.winlineElement.innerHTML = '';
        this.renderCells();
    },
    
    renderCells() {
        this.cellsElement.innerHTML = '';
        CELL_POSITIONS.forEach((pos, index) => {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.style.left = pos[0] + 'px';
            cell.style.top = pos[1] + 'px';
            cell.dataset.index = index;
            cell.innerHTML = `<svg viewBox="0 0 96 96" width="96" height="96"></svg>`;
            this.cellsElement.appendChild(cell);
        });
    },
    
    placeMark(index, symbol) {
        if (this.cells[index] !== null) return false;
        this.cells[index] = symbol;
        const cellElement = this.cellsElement.children[index];
        this.drawMark(cellElement, symbol);
        return true;
    },
    
    drawMark(cellElement, symbol) {
        const svg = cellElement.querySelector('svg');
        svg.innerHTML = '';
        
        if (symbol === 'X') {
            const path1 = this.createPath("M18 20 C 40 46, 55 60, 78 78", 'var(--marker-red)');
            const path2 = this.createPath("M78 18 C 55 44, 40 58, 18 78", 'var(--marker-red)');
            svg.appendChild(path1);
            svg.appendChild(path2);
            this.animatePath([path1, path2]);
        } else {
            const path = this.createPath("M48 16 C 20 16, 16 48, 48 80 C 80 80, 82 16, 48 16 Z", 'var(--marker-blue)');
            svg.appendChild(path);
            this.animatePath([path]);
        }
    },
    
    createPath(d, stroke) {
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', d);
        path.setAttribute('class', 'mark');
        path.setAttribute('stroke', stroke);
        path.setAttribute('stroke-width', 9);
        return path;
    },
    
    animatePath(paths) {
        paths.forEach(path => {
            const length = path.getTotalLength();
            path.style.strokeDasharray = length;
            path.style.strokeDashoffset = length;
            path.getBoundingClientRect();
            path.style.transition = 'stroke-dashoffset .35s ease';
            requestAnimationFrame(() => {
                path.style.strokeDashoffset = 0;
            });
        });
    },
    
    checkWin(symbol) {
        return WINNING_COMBINATIONS.some(([a, b, c]) => {
            return this.cells[a] === symbol && this.cells[b] === symbol && this.cells[c] === symbol;
        });
    },
    
    getWinningCombination(symbol) {
        return WINNING_COMBINATIONS.find(([a, b, c]) => {
            return this.cells[a] === symbol && this.cells[b] === symbol && this.cells[c] === symbol;
        });
    },
    
    isFull() {
        return this.cells.every(cell => cell !== null);
    },
    
    getEmptyCells() {
        return this.cells.map((cell, index) => cell === null ? index : null).filter(index => index !== null);
    },
    
    drawWinLine(winningCells) {
        const centers = winningCells.map(index => {
            const pos = CELL_POSITIONS[index];
            return [pos[0] + 48, pos[1] + 48];
        });
        
        const [x1, y1] = centers[0];
        const [x2, y2] = centers[2];
        
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', x1);
        line.setAttribute('y1', y1);
        line.setAttribute('x2', x1);
        line.setAttribute('y2', y1);
        line.setAttribute('stroke', 'var(--highlight)');
        line.setAttribute('stroke-width', '16');
        line.setAttribute('stroke-linecap', 'round');
        line.setAttribute('opacity', '0.55');
        
        this.winlineElement.appendChild(line);
        
        requestAnimationFrame(() => {
            line.style.transition = 'x2 .3s ease, y2 .3s ease';
            line.setAttribute('x2', x2);
            line.setAttribute('y2', y2);
        });
    },
    
    clear() {
        this.cells = Array(9).fill(null);
        this.winlineElement.innerHTML = '';
        this.renderCells();
    }
};