
from random import choice

REGULAR_SYMBOL_COUNT = 36
GREEN_COUNT = 1
SYMBOLS = list(range(REGULAR_SYMBOL_COUNT + GREEN_COUNT))
MIN_BET_AMOUNT = 500
MAX_BET_AMOUNT = 50000
VALID_COUNTS = [1, 2, 4, 12, 18]


def play_roulette(bets):
    result_symbol = choice(SYMBOLS)

    total_prize = 0
    for bet in bets:
        prize = 0
        if result_symbol in bet.get('symbols'):
            prize = bet.get('amount') * bet.get('multiplier')

        total_prize += prize
        bet['prize'] = prize

    return {
        'result': result_symbol,
        'prize': total_prize,
        'bets': bets
    }
