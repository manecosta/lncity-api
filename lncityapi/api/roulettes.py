
import json

from flask import request, abort
from flask_login import login_required, current_user

from lncityapi import app
from lncityapi.controllers.balancescontroller import add_user_balance
from lncityapi.controllers.logscontroller import add_log
from lncityapi.other.util import route_prefix_v1
from lncityapi.controllers.roulettescontroller import GREEN_COUNT, VALID_COUNTS, REGULAR_SYMBOL_COUNT, MIN_BET_AMOUNT,\
    MAX_BET_AMOUNT, play_roulette


@app.route(route_prefix_v1 + '/games/roulettes/getparameters', methods=['GET'])
@login_required
def get_roulette_parameters():
    return json.dumps({
        'valid_counts': VALID_COUNTS,
        'green_count': GREEN_COUNT,
        'regular_symbol_count': REGULAR_SYMBOL_COUNT,
        'min_bet_amount': MIN_BET_AMOUNT,
        'max_bet_amount': MAX_BET_AMOUNT
    })


@app.route(route_prefix_v1 + '/games/roulettes/play', methods=['POST'])
@login_required
def play_roulette_request():

    payload = request.get_json()

    bets = payload.get('bets')

    if not isinstance(bets, list):
        abort(400, 'Malformed request (#1)')

    if len(bets) == 0:
        abort(400, 'Please provide some bets')

    total_bet_amount = 0

    # Check
    for bet in bets:
        symbols = bet.get('symbols')
        if symbols is None or not isinstance(symbols, list) or len(symbols) not in VALID_COUNTS:
            abort(400, 'Unexpected symbols')

        amount = bet.get('amount')
        if not isinstance(amount, int) or amount == 0:
            abort(400, 'Invalid bet amount')

        bet['multiplier'] = REGULAR_SYMBOL_COUNT / len(symbols)

        total_bet_amount += amount

    if not (MIN_BET_AMOUNT <= total_bet_amount <= MAX_BET_AMOUNT):
        abort(400, 'Invalid total bet amount')

    success = add_user_balance(current_user, -total_bet_amount)

    if not success:
        abort(400, 'Not enough balance')

    result = play_roulette(bets)

    prize = result.get('prize')
    if prize > 0:
        add_user_balance(current_user, prize)

    add_log(current_user.id, 2, 'play', {
        'prize': prize,
        'bet': total_bet_amount,
        'result': result.get('result')
    })

    return json.dumps(result)
