// ========================================
// GAME CONSTANTS
// ========================================

const PLAYER_X = 'X';
const PLAYER_O = 'O';
const MODE_PVP = 'pvp';
const MODE_PVC = 'pva';
const DIFFICULTY_EASY = 'easy';
const DIFFICULTY_MEDIUM = 'medium';
const DIFFICULTY_HARD = 'hard';

const WINNING_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
];

const CELL_POSITIONS = [
    [3, 3], [103, 3], [203, 3],
    [3, 103], [103, 103], [203, 103],
    [3, 203], [103, 203], [203, 203]
];

const HUMAN = 'X';
const AI = 'O';