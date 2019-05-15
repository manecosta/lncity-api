
from random import sample
from time import time
from uuid import uuid4

if __name__ != '__main__':
    from lncityapi.models import Pokerhand

base_bet = 500
min_bet_multiplier = 1
max_bet_multiplier = 10

low_ace_value = 1
high_ace_value = 14
jack_value = 11

cards = [
    {'name': 'two', 'suit': 'clubs', 'value': 2},
    {'name': 'three', 'suit': 'clubs', 'value': 3},
    {'name': 'four', 'suit': 'clubs', 'value': 4},
    {'name': 'five', 'suit': 'clubs', 'value': 5},
    {'name': 'six', 'suit': 'clubs', 'value': 6},
    {'name': 'seven', 'suit': 'clubs', 'value': 7},
    {'name': 'eight', 'suit': 'clubs', 'value': 8},
    {'name': 'nine', 'suit': 'clubs', 'value': 9},
    {'name': 'ten', 'suit': 'clubs', 'value': 10},
    {'name': 'jack', 'suit': 'clubs', 'value': jack_value},
    {'name': 'queen', 'suit': 'clubs', 'value': 12},
    {'name': 'king', 'suit': 'clubs', 'value': 13},
    {'name': 'ace', 'suit': 'clubs', 'value': high_ace_value},

    {'name': 'two', 'suit': 'diamonds', 'value': 2},
    {'name': 'three', 'suit': 'diamonds', 'value': 3},
    {'name': 'four', 'suit': 'diamonds', 'value': 4},
    {'name': 'five', 'suit': 'diamonds', 'value': 5},
    {'name': 'six', 'suit': 'diamonds', 'value': 6},
    {'name': 'seven', 'suit': 'diamonds', 'value': 7},
    {'name': 'eight', 'suit': 'diamonds', 'value': 8},
    {'name': 'nine', 'suit': 'diamonds', 'value': 9},
    {'name': 'ten', 'suit': 'diamonds', 'value': 10},
    {'name': 'jack', 'suit': 'diamonds', 'value': jack_value},
    {'name': 'queen', 'suit': 'diamonds', 'value': 12},
    {'name': 'king', 'suit': 'diamonds', 'value': 13},
    {'name': 'ace', 'suit': 'diamonds', 'value': high_ace_value},

    {'name': 'two', 'suit': 'hearts', 'value': 2},
    {'name': 'three', 'suit': 'hearts', 'value': 3},
    {'name': 'four', 'suit': 'hearts', 'value': 4},
    {'name': 'five', 'suit': 'hearts', 'value': 5},
    {'name': 'six', 'suit': 'hearts', 'value': 6},
    {'name': 'seven', 'suit': 'hearts', 'value': 7},
    {'name': 'eight', 'suit': 'hearts', 'value': 8},
    {'name': 'nine', 'suit': 'hearts', 'value': 9},
    {'name': 'ten', 'suit': 'hearts', 'value': 10},
    {'name': 'jack', 'suit': 'hearts', 'value': jack_value},
    {'name': 'queen', 'suit': 'hearts', 'value': 12},
    {'name': 'king', 'suit': 'hearts', 'value': 13},
    {'name': 'ace', 'suit': 'hearts', 'value': high_ace_value},

    {'name': 'two', 'suit': 'spades', 'value': 2},
    {'name': 'three', 'suit': 'spades', 'value': 3},
    {'name': 'four', 'suit': 'spades', 'value': 4},
    {'name': 'five', 'suit': 'spades', 'value': 5},
    {'name': 'six', 'suit': 'spades', 'value': 6},
    {'name': 'seven', 'suit': 'spades', 'value': 7},
    {'name': 'eight', 'suit': 'spades', 'value': 8},
    {'name': 'nine', 'suit': 'spades', 'value': 9},
    {'name': 'ten', 'suit': 'spades', 'value': 10},
    {'name': 'jack', 'suit': 'spades', 'value': jack_value},
    {'name': 'queen', 'suit': 'spades', 'value': 12},
    {'name': 'king', 'suit': 'spades', 'value': 13},
    {'name': 'ace', 'suit': 'spades', 'value': high_ace_value}
]


def high_card_value(hand_cards):
    highest_card = None
    for card in hand_cards:
        if highest_card is None:
            highest_card = card
        elif card.get('value') > highest_card.get('value'):
            highest_card = card

    return highest_card.get('value')


def is_flush(hand_cards):
    suit = None
    for card in hand_cards:
        if suit is None:
            suit = card.get('suit')
        elif suit != card.get('suit'):
            return False, []

    return True, list([i for i in range(5)])


def is_straight(hand_cards):
    values = []
    for card in hand_cards:
        values.append(card.get('value'))

    if sorted(values) == list(range(min(values), max(values)+1)):
        return True, list([i for i in range(5)])

    if high_ace_value in values:
        values.remove(high_ace_value)
        values.append(low_ace_value)

        if sorted(values) == list(range(min(values), max(values) + 1)):
            return True, list([i for i in range(5)])

    return False, []


def is_four_of_a_kind(hand_cards):
    values_count = {}
    for card in hand_cards:
        value_key = str(card.get('value'))
        values_count.setdefault(value_key, 0)
        values_count[value_key] += 1

    high_value = None
    high_count = 0
    for value, count in values_count.items():
        if count > high_count:
            high_value = int(value)
            high_count = count

    if high_count == 4:
        return True, [i for i in range(len(hand_cards)) if hand_cards[i].get('value') == high_value]

    return False, []


def is_full_house(hand_cards):
    values_count = {}
    for card in hand_cards:
        value_key = str(card.get('value'))
        values_count.setdefault(value_key, 0)
        values_count[value_key] += 1

    if sorted(values_count.values()) == [2, 3]:
        return True, list([i for i in range(5)])

    return False, []


def is_three_of_a_kind(hand_cards):
    values_count = {}
    for card in hand_cards:
        value_key = str(card.get('value'))
        values_count.setdefault(value_key, 0)
        values_count[value_key] += 1

    high_value = None
    high_count = 0
    for value, count in values_count.items():
        if count > high_count:
            high_value = int(value)
            high_count = count

    if high_count == 3:
        return True, [i for i in range(len(hand_cards)) if hand_cards[i].get('value') == high_value]

    return False, []


def is_two_pairs(hand_cards):
    values_count = {}
    for card in hand_cards:
        value_key = str(card.get('value'))
        values_count.setdefault(value_key, 0)
        values_count[value_key] += 1

    if sorted(values_count.values()) == [1, 2, 2]:
        values = []
        for value, count in values_count.items():
            if count == 2:
                values.append(int(value))

        return True, [i for i in range(len(hand_cards)) if hand_cards[i].get('value') in values]

    return False, []


def is_high_pair(hand_cards):
    values_count = {}
    for card in hand_cards:
        value = card.get('value')
        if value >= jack_value:
            value_key = str(value)
            values_count.setdefault(value_key, 0)
            values_count[value_key] += 1

    if len(values_count.values()) > 0 and sorted(values_count.values())[-1] == 2:
        for value, count in values_count.items():
            if count == 2:
                return True, [i for i in range(len(hand_cards)) if hand_cards[i].get('value') == int(value)]

    return False, []


prize_infos = [
    {
        'name': 'royal_flush',
        'title': 'Royal Flush',
        'multiplier': 250,
        'checks': [is_straight, is_flush, lambda x: (high_card_value(x) == high_ace_value, [])]
    },
    {
        'name': 'straight_flush',
        'title': 'Straight Flush',
        'multiplier': 50,
        'checks': [is_straight, is_flush]
    },
    {
        'name': 'four_of_a_kind',
        'title': 'Four of a Kind',
        'multiplier': 25,
        'checks': [is_four_of_a_kind]
    },
    {
        'name': 'full_house',
        'title': 'Full House',
        'multiplier': 9,
        'checks': [is_full_house]
    },
    {
        'name': 'flush',
        'title': 'Flush',
        'multiplier': 6,
        'checks': [is_flush]
    },
    {
        'name': 'straight',
        'title': 'Straight',
        'multiplier': 4,
        'checks': [is_straight]
    },
    {
        'name': 'three_of_a_kind',
        'title': 'Three of a Kind',
        'multiplier': 3,
        'checks': [is_three_of_a_kind]
    },
    {
        'name': 'two_pairs',
        'title': 'Two Pairs',
        'multiplier': 2,
        'checks': [is_two_pairs]
    },
    {
        'name': 'pair_jacks_or_better',
        'title': 'Pair (Jacks or Better)',
        'multiplier': 1,
        'checks': [is_high_pair]
    },
]


def get_game_cards():
    game_cards = sample(cards, k=10)

    return {
        'front': game_cards[0:5],
        'back': game_cards[5:10]
    }


def check_hand_cards(hand_cards):
    for prize_info in prize_infos:
        check_result = True
        matched_indexes = None
        for check in prize_info.get('checks'):
            is_match, mi = check(hand_cards)
            check_result = check_result and is_match
            if is_match and matched_indexes is None:
                matched_indexes = mi
            if not check_result:
                break

        if check_result:
            return matched_indexes, {k: v for k, v in prize_info.items() if k != 'checks'}

    return [], None


def new_poker_hand(user, multiplier):

    identifier = None
    hand_cards = None
    matched_indexes = []
    prize_info = None
    recovered = False

    for ph in Pokerhand.select().where(Pokerhand.user == user.id, Pokerhand.settled == 0):
        identifier = ph.identifier
        hand_cards = ph.info.get('front')
        multiplier = ph.multiplier
        recovered = True

    if identifier is None:
        game_cards = get_game_cards()
        hand_cards = game_cards.get('front')

        identifier = uuid4().hex

        poker_hand = Pokerhand.create(
            identifier=identifier,
            user=user.id,
            info=game_cards,
            settled=0,
            multiplier=multiplier,
            time=time()
        )

        # Checking if two hands were added in the meantime
        user_unsettled_hands_count = Pokerhand.select().where(Pokerhand.user == user.id, Pokerhand.settled == 0).count()

        if user_unsettled_hands_count > 1:
            poker_hand.delete_instance()
            identifier = None
            hand_cards = None

    if hand_cards is not None:
        matched_indexes, prize_info = check_hand_cards(hand_cards)

    return identifier, hand_cards, matched_indexes, prize_info, recovered, multiplier


def get_pocker_hand(identifier, user):

    ph_query = (
        Pokerhand.select()
            .where(Pokerhand.identifier == identifier, Pokerhand.user == user.id, Pokerhand.settled == 0)
    )

    for ph in ph_query:
        return ph

    return None


def play_poker_hand(poker_hand, hold_indexes):

    game_cards = poker_hand.info
    front_cards = game_cards.get('front')
    back_cards = game_cards.get('back')

    result_cards = []
    for i in range(5):
        if i in hold_indexes:
            result_cards.append(front_cards[i])
        else:
            result_cards.append(back_cards[i])

    matched_indexes, prize_info = check_hand_cards(result_cards)

    return result_cards, matched_indexes, prize_info


def settle_poker_hand(poker_hand):
    lines_changed = Pokerhand.update(settled=1).where(Pokerhand.id == poker_hand.id, Pokerhand.settled == 0).execute()

    return lines_changed != 0


if __name__ == '__main__':

    cs = [
        {'name': 'two', 'suit': 'clubs', 'value': 2},
        {'name': 'two', 'suit': 'spades', 'value': 2},
        {'name': 'two', 'suit': 'diamonds', 'value': 2},
        {'name': 'three', 'suit': 'diamonds', 'value': 3},
        {'name': 'four', 'suit': 'clubs', 'value': 4},
    ]

    is_three_of_a_kind(cs)
