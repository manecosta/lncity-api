
import json

from flask import request, abort
from flask_login import login_required, current_user

from lncityapi import app
from lncityapi.controllers.balancescontroller import add_user_balance
from lncityapi.controllers.logscontroller import add_log
from lncityapi.other.util import route_prefix_v1
from lncityapi.controllers.pokerscontroller import base_bet, min_bet_multiplier, max_bet_multiplier, new_poker_hand, \
    get_pocker_hand, play_poker_hand, prize_infos, settle_poker_hand, cards


@app.route(route_prefix_v1 + '/games/pokers/getparameters', methods=['GET'])
@login_required
def get_poker_parameters():

    pi = [{k: v for k, v in prize_info.items() if k != 'checks'} for prize_info in prize_infos]

    return json.dumps({
        'base_bet': base_bet,
        'max_bet_multiplier': max_bet_multiplier,
        'min_bet_multiplier': min_bet_multiplier,
        'prize_infos': pi,
        'cards': cards
    })


@app.route(route_prefix_v1 + '/games/pokers/get', methods=['POST'])
@login_required
def get_pocker_hand_request():

    payload = request.get_json()

    bet_multiplier = payload.get('bet_multiplier')

    if not bet_multiplier:
        abort(400, 'Please provide bet_multiplier')

    if bet_multiplier > 10 or bet_multiplier < 1:
        abort(400, 'Please provide a bet_multiplier between 1 and 10')

    bet_price = bet_multiplier * base_bet

    success = add_user_balance(current_user, -bet_price)

    if not success:
        abort(400, 'Not enough balance')

    identifier, front_cards = new_poker_hand(current_user, bet_multiplier)

    if identifier is None:
        abort(400, 'Nope.')

    add_log(current_user.id, 3, 'play_get', {
        'front_cards': front_cards,
        'identifier': identifier,
        'multiplier': bet_multiplier
    })

    return json.dumps({
        'front_cards': front_cards,
        'identifier': identifier
    })


@app.route(route_prefix_v1 + '/games/pokers/play', methods=['POST'])
@login_required
def play_poker_hand_request():
    payload = request.get_json()

    hold_indexes = payload.get('hold_indexes')
    identifier = payload.get('identifier')

    if hold_indexes is None:
        abort(400, 'Please provide hold_indexes')

    if identifier is None:
        abort(400, 'Please provide identifier')

    poker_hand = get_pocker_hand(identifier, current_user)

    if poker_hand is None:
        abort(400, 'Invalid identifier')

    deduped_hold_indexes = []
    for index in hold_indexes:
        if not (0 <= index <= 4):
            abort(400, 'Please provide hold_indexes between 0 and 4')
        elif index not in deduped_hold_indexes:
            deduped_hold_indexes.append(index)

    result_cards, matched_indexes, prize_info = play_poker_hand(poker_hand, deduped_hold_indexes)

    settled = settle_poker_hand(poker_hand)

    if not settled:
        # Hand was already played in the meantime
        abort(400, 'Invalid identifier')

    bet = poker_hand.multiplier * base_bet
    prize = 0

    if prize_info is not None:
        prize_multiplier = prize_info.get('multiplier')
        prize = bet * prize_multiplier

    add_user_balance(current_user, prize)

    add_log(current_user.id, 3, 'play', {
        'bet': bet,
        'identifier': identifier,
        'result_cards': result_cards,
        'prize': prize
    })

    return json.dumps({
        'identifier': identifier,
        'result_cards': result_cards,
        'prize': prize,
        'matched_indexes': matched_indexes,
        'prize_info': prize_info
    })
