
from random import choice, random


base_bet = 500
min_bet_multiplier = 1
max_bet_multiplier = 10

num_lines = 5
num_columns = 3

wildcard_chance = 0.09

lines = [
    [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]],
    [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1]],
    [[0, 2], [1, 2], [2, 2], [3, 2], [4, 2]],
    [[0, 0], [1, 1], [2, 2], [3, 1], [4, 0]],
    [[0, 2], [1, 1], [2, 0], [3, 1], [4, 2]]
]

available_symbols = {
    'Strawberry': {
        'imagePath': 'assets/img/slot/strawberry.png',
        'prize': [0, 0, 250, 500, 1000],
        'isWild': False
    },
    'Orange': {
        'imagePath': 'assets/img/slot/orange.png',
        'prize': [0, 0, 500, 1000, 2000],
        'isWild': False
    },
    'Heart': {
        'imagePath': 'assets/img/slot/heart.png',
        'prize': [0, 0, 750, 1500, 3000],
        'isWild': False
    },
    'Clover': {
        'imagePath': 'assets/img/slot/clover.png',
        'prize': [0, 0, 1000, 2000, 4000],
        'isWild': False
    },
    'Diamond': {
        'imagePath': 'assets/img/slot/diamond.png',
        'prize': [0, 0, 1250, 2500, 5000],
        'isWild': False
    },
    'Seven': {
        'imagePath': 'assets/img/slot/seven.png',
        'prize': [0, 0, 1500, 3000, 6000],
        'isWild': False
    },
    'Bitcoin': {
        'imagePath': 'assets/img/slot/bitcoin.png',
        'prize': [0, 0, 2000, 4000, 8000],
        'isWild': False
    },
    'Satoshi': {
        'imagePath': 'assets/img/slot/satoshi.png',
        'prize': [0, 0, 0, 0, 10000],
        'isWild': True
    }
}

wild_symbol_name = None
symbol_names = []

for symbol_name, symbol_info in available_symbols.items():
    if symbol_info.get('isWild'):
        wild_symbol_name = symbol_name
    else:
        symbol_names.append(symbol_name)


def get_winning_lines(board):
    winning_lines_info = []
    for line in lines:
        line_symbols = []
        for coordinates in line:
            line_symbols.append(board[coordinates[0]][coordinates[1]])

        consecutive_symbols = []
        for symbol in line_symbols:
            if len(consecutive_symbols) == 0:
                consecutive_symbols = [symbol]
                continue

            last_symbol = consecutive_symbols[-1]
            if last_symbol == wild_symbol_name:
                if symbol == wild_symbol_name:
                    consecutive_symbols.append(wild_symbol_name)
                else:
                    consecutive_symbols = [symbol for _ in range(len(consecutive_symbols) + 1)]
            else:
                if symbol == last_symbol:
                    consecutive_symbols.append(symbol)
                elif symbol == wild_symbol_name:
                    consecutive_symbols.append(last_symbol)
                else:
                    break

        prizes = available_symbols.get(consecutive_symbols[0]).get('prize')

        prize = prizes[len(consecutive_symbols) - 1]
        if prize > 0:
            winning_lines_info.append((line_symbols, consecutive_symbols, line, prize))

    return winning_lines_info


def get_random_board():
    board = [
        [choice(symbol_names) if random() > wildcard_chance else wild_symbol_name for _ in range(num_columns)]
        for _ in range(num_lines)
    ]

    winning_lines_info = get_winning_lines(board)

    total_prize = 0
    for winning_line_info in winning_lines_info:
        total_prize += winning_line_info[-1]

    return board, total_prize
