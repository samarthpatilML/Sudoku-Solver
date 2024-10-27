let board = [];
let timer;
let startTime;
const boardElement = document.getElementById("board");
const timeElement = document.getElementById("time");
const scoreElement = document.getElementById("score");

// Generate a 9x9 board with input elements
function generateBoard() {
    boardElement.innerHTML = "";
    for (let i = 0; i < 9; i++) {
        board[i] = [];
        for (let j = 0; j < 9; j++) {
            const input = document.createElement("input");
            input.type = "text";
            input.classList.add("cell");
            input.maxLength = 1;
            input.id = `cell-${i}-${j}`;
            input.addEventListener("input", (e) => {
                if (!/^[1-9]$/.test(e.target.value)) {
                    e.target.value = "";
                }
            });
            board[i][j] = input;
            boardElement.appendChild(input);
        }
    }
}

function getBoardValues() {
    const values = [];
    for (let i = 0; i < 9; i++) {
        values[i] = [];
        for (let j = 0; j < 9; j++) {
            const cellValue = board[i][j].value;
            values[i][j] = cellValue ? parseInt(cellValue) : 0;
        }
    }
    return values;
}

function isValid(board, num, pos) {
    const [row, col] = pos;

    // Check row and column
    for (let i = 0; i < 9; i++) {
        if (board[row][i] === num || board[i][col] === num) {
            return false;
        }
    }

    // Check 3x3 grid
    const startRow = Math.floor(row / 3) * 3;
    const startCol = Math.floor(col / 3) * 3;
    for (let i = startRow; i < startRow + 3; i++) {
        for (let j = startCol; j < startCol + 3; j++) {
            if (board[i][j] === num) {
                return false;
            }
        }
    }

    return true;
}

function solveSudoku(board) {
    for (let row = 0; row < 9; row++) {
        for (let col = 0; col < 9; col++) {
            if (board[row][col] === 0) {
                for (let num = 1; num <= 9; num++) {
                    if (isValid(board, num, [row, col])) {
                        board[row][col] = num;
                        if (solveSudoku(board)) {
                            return true;
                        }
                        board[row][col] = 0;
                    }
                }
                return false;
            }
        }
    }
    return true;
}

function displaySolvedBoard(solvedBoard) {
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            board[i][j].value = solvedBoard[i][j];
        }
    }
}

function startTimer() {
    startTime = Date.now();
    timer = setInterval(() => {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        timeElement.textContent = elapsed;
    }, 1000);
}

function stopTimer() {
    clearInterval(timer);
    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    return elapsed;
}

function saveHighScore(time) {
    const highScore = localStorage.getItem("highScore");
    if (!highScore || time < highScore) {
        localStorage.setItem("highScore", time);
        scoreElement.textContent = time;
    }
}

function loadHighScore() {
    const highScore = localStorage.getItem("highScore");
    if (highScore) {
        scoreElement.textContent = highScore;
    }
}

// Button Actions
document.getElementById("solveButton").addEventListener("click", () => {
    const boardValues = getBoardValues();
    startTimer();
    if (solveSudoku(boardValues)) {
        displaySolvedBoard(boardValues);
        const elapsedTime = stopTimer();
        saveHighScore(elapsedTime);
        alert(`Solved in ${elapsedTime} seconds!`);
    } else {
        alert("No solution exists.");
    }
});

document.getElementById("resetButton").addEventListener("click", () => {
    generateBoard();
    timeElement.textContent = "0";
    clearInterval(timer);
});

// Initial setup
generateBoard();
loadHighScore();
