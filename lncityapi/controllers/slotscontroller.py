
from random import choice, random


base_bet = 500
min_bet_multiplier = 1
max_bet_multiplier = 10

num_lines = 3
num_columns = 5

wildcard_chance = 0.03
bonus_chance = 0.04

lines = [
    [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]],
    [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1]],
    [[0, 2], [1, 2], [2, 2], [3, 2], [4, 2]],
    [[0, 0], [1, 1], [2, 2], [3, 1], [4, 0]],
    [[0, 2], [1, 1], [2, 0], [3, 1], [4, 2]]
]

available_symbols = {
    'Grapes': {
        'imagePath': 'assets/img/slot/grapes.png',
        'prize': [0, 0, 250, 1000, 4000],
        'isWild': False,
        'isBonus': False
    },
    'Lemon': {
        'imagePath': 'assets/img/slot/lemon.png',
        'prize': [0, 0, 500, 2000, 8000],
        'isWild': False,
        'isBonus': False
    },
    'Seven': {
        'imagePath': 'assets/img/slot/seven.png',
        'prize': [0, 0, 750, 3000, 12000],
        'isWild': False,
        'isBonus': False
    },
    'Clover': {
        'imagePath': 'assets/img/slot/clover.png',
        'prize': [0, 0, 1000, 4000, 16000],
        'isWild': False,
        'isBonus': False
    },
    'Diamond': {
        'imagePath': 'assets/img/slot/diamond.png',
        'prize': [0, 0, 1500, 6000, 24000],
        'isWild': False,
        'isBonus': False
    },
    'Bitcoin': {
        'imagePath': 'assets/img/slot/bitcoin.png',
        'prize': [0, 0, 1250, 2500, 10000, 50000],
        'isWild': False,
        'isBonus': True
    },
    'Satoshi': {
        'imagePath': 'assets/img/slot/satoshi.png',
        'prize': [0, 0, 0, 0, 100000],
        'isWild': True,
        'isBonus': False
    }
}

wild_symbol_name = None
bonus_symbol_name = None
symbol_names = []

for symbol_name, symbol_info in available_symbols.items():
    if symbol_info.get('isWild'):
        wild_symbol_name = symbol_name
    elif symbol_info.get('isBonus'):
        bonus_symbol_name = symbol_name
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

        if consecutive_symbols[0] == bonus_symbol_name:
            continue

        prizes = available_symbols.get(consecutive_symbols[0]).get('prize')

        prize = prizes[len(consecutive_symbols) - 1]
        if prize > 0:
            winning_lines_info.append((line_symbols, consecutive_symbols, line, prize))

    bonus_coordinates = []
    for column in range(num_columns):
        for line in range(num_lines):
            if board[column][line] == bonus_symbol_name:
                bonus_coordinates.append([column, line])

    bonus_prize = 0
    if len(bonus_coordinates) > 0:
        bonus_prize = available_symbols.get(bonus_symbol_name).get('prize')[len(bonus_coordinates) - 1]

    bonus_line_symbols = [bonus_symbol_name for _ in bonus_coordinates]
    winning_lines_info.append((bonus_line_symbols, bonus_line_symbols, bonus_coordinates, bonus_prize))

    return winning_lines_info


def get_random_board():

    board = []
    bonus_count = 0

    for column in range(num_columns):
        board.append([])
        for line in range(num_lines):
            special_symbols_selection = random()
            if special_symbols_selection < wildcard_chance:
                board[column].append(wild_symbol_name)
            elif bonus_count < len(available_symbols.get(bonus_symbol_name).get('prize')) and special_symbols_selection < wildcard_chance + bonus_chance:
                board[column].append(bonus_symbol_name)
                bonus_count += 1
            else:
                board[column].append(choice(symbol_names))

    winning_lines_info = get_winning_lines(board)

    total_prize = 0
    for winning_line_info in winning_lines_info:
        total_prize += winning_line_info[-1]

    return board, total_prize, winning_lines_info


def test_profitabiity():
    total_spent = 0
    total_won = 0

    iterations = 200000
    win_count = 0

    win_combinations_count = {}

    for i in range(iterations):
        board, prize, wlsi = get_random_board()
        total_spent += base_bet
        total_won += prize
        if prize > 0:
            win_count += 1

        for wli in wlsi:
            if wli[3] > 0:
                key = ''.join(wli[1])
                current_count = win_combinations_count.get(key)
                if current_count is None:
                    win_combinations_count[key] = 1
                else:
                    win_combinations_count[key] += 1

    print(f'Spent: {total_spent}. Won: {total_won}.'
          f'Win Ratio: {(total_won/total_spent)*100}%. Win Count Ratio: {(win_count/iterations)*100}%')

    print('\n\n')
    wcclist = []
    for wc, count in win_combinations_count.items():
        wcclist.append((wc, count))

    wcclist.sort(key=lambda x: x[1], reverse=True)

    for wcc in wcclist:
        s_name = wcc[0][0:5 + wcc[0][5:-1].index(wcc[0][0:5])]
        print(f'{wcc[1]} -> {len(wcc[0]) / len(s_name)}x {s_name}')


def test_play():
    initial_balance = 10000
    iterations = 1000
    doubled_count = 0
    bust_count = 0
    multiplier = 1

    for i in range(iterations):
        balance = initial_balance
        while True:
            board, prize, wlsi = get_random_board()
            balance -= base_bet * multiplier
            balance += prize * multiplier

            if balance < base_bet:
                bust_count += 1
                break
            elif balance >= initial_balance * 2:
                doubled_count += 1
                break

    print(f'Doubled: {doubled_count} ({(doubled_count/iterations)*100}%).')
    print(f'Bust: {bust_count} ({(bust_count/iterations)*100}%).')


def test_to_zero():
    initial_balance = 50000
    iterations = 1000
    multiplier = 5

    total_spent = 0
    total_won = 0
    play_count = 0
    win_count = 0

    to_zero_infos = {}

    for i in range(iterations):
        balance = initial_balance
        round_index = 0
        while True:
            round_index += 1
            board, prize, wlsi = get_random_board()
            balance -= base_bet * multiplier
            balance += prize * multiplier

            play_count += 1
            if prize > 0:
                win_count += 1
            total_spent += base_bet * multiplier
            total_won += prize * multiplier

            if balance < base_bet:
                to_zero_count = to_zero_infos.get(str(round_index))
                if to_zero_count is None:
                    to_zero_infos[str(round_index)] = 1
                else:
                    to_zero_infos[str(round_index)] = to_zero_count + 1

                break

    to_zero_rounds = [int(count) for count in to_zero_infos.keys()]

    to_zero_rounds.sort()

    aux = 1
    to_zero_iteration_count = 0
    for round_i in to_zero_rounds:
        to_zero_iteration_count += to_zero_infos.get(str(round_i))
        if aux == 1 and to_zero_iteration_count >= iterations * 0.25:
            print(f'25% of iterations reached 0 balance until round {round_i}')
            aux += 1
        elif aux == 2 and to_zero_iteration_count >= iterations * 0.5:
            print(f'Half of iterations reached 0 balance until round {round_i}')
            aux += 1
        elif aux == 3 and to_zero_iteration_count >= iterations * 0.75:
            print(f'75% of iterations reached 0 balance until round {round_i}')
            aux += 1
        elif aux == 4 and to_zero_iteration_count >= iterations * 0.9:
            print(f'90% of iterations reached 0 balance until round {round_i}')
            break

    print(f'\nSpent: {total_spent}. Won: {total_won}.'
          f'Win Ratio: {(total_won/total_spent)*100}%. Win Count Ratio: {(win_count/play_count)*100}%')


if __name__ == '__main__':

    test_number = 1

    if test_number == 1:
        test_profitabiity()
    elif test_number == 2:
        test_play()
    elif test_number == 3:
        test_to_zero()
