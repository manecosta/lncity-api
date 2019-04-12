import json

from flask import request, abort
from flask_login import login_required, current_user

from lncityapi import app
from lncityapi.other.util import route_prefix_v1
from lncityapi.controllers.slotscontroller import available_symbols, lines, symbol_names, get_random_board, base_bet,\
    max_bet_multiplier, min_bet_multiplier, wild_symbol_name, bonus_symbol_name
from lncityapi.controllers.balancescontroller import add_user_balance


@app.route(route_prefix_v1 + '/games/slots/getparameters', methods=['GET'])
@login_required
def get_slot_parameters():
    return json.dumps({
        'wild_symbol_name': wild_symbol_name,
        'bonus_symbol_name': bonus_symbol_name,
        'available_symbols': available_symbols,
        'lines': lines,
        'symbol_names': symbol_names,
        'base_bet': base_bet,
        'max_bet_multiplier': max_bet_multiplier,
        'min_bet_multiplier': min_bet_multiplier
    })


@app.route(route_prefix_v1 + '/games/slots/getboard', methods=['POST'])
@login_required
def get_board_request():
    body = request.get_json()

    bet_multiplier = body.get('bet_multiplier')

    bet_price = bet_multiplier * base_bet

    success = add_user_balance(current_user, -bet_price)

    if not success:
        abort(400, 'Not enough balance')

    if not bet_multiplier:
        abort(400, 'Please provide bet_multiplier')

    if bet_multiplier > 10 or bet_multiplier < 1:
        abort(400, 'Please provide a bet_multiplier between 1 and 10')

    board, prize = get_random_board()

    multiplied_prize = prize * bet_multiplier

    if multiplied_prize > 0:
        add_user_balance(current_user, multiplied_prize)

    return json.dumps({
        'board': board,
        'prize': multiplied_prize
    })
