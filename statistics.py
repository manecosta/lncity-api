
import arrow, logging, json

from peewee import fn

from lncityapi.models import Log
from lncityapi.models.user import User
from lncityapi.models.balance import Deposit, Withdrawal


logger = logging.getLogger('peewee')
logger.setLevel(logging.INFO)


def print_section(title, statistics):

    print('\n')

    print(''.join(['#' for _ in range(len(title) + 4)]))
    print(f'# {title} #')
    print(''.join(['#' for _ in range(len(title) + 4)]))

    print('')

    for statistic in statistics:
        print(f'# {statistic.get("title")} {statistic.get("value")}')


def run():

    users_count = User.select().count()
    last_24h_users_count = User.select().where(User.created_time > arrow.get().shift(days=-1).float_timestamp).count()
    last_7d_users_count = User.select().where(User.created_time > arrow.get().shift(days=-7).float_timestamp).count()

    wealthier_10_users = [u for u in User.select().order_by(User.balance.desc()).limit(10)]
    last_10_users = [u for u in User.select().order_by(User.created_time.desc()).limit(10)]

    user_statistics = [
        {
            'title': 'User Count:',
            'value': f'{users_count}'
        },
        {
            'title': 'Last 24h User Count:',
            'value': f'{last_24h_users_count}'
        },
        {
            'title': 'Last Week User Count:',
            'value': f'{last_7d_users_count}'
        },
        {
            'title': 'Wealthier 10 Users:',
            'value': '\n\t' + '\n\t'.join([f'{u.username if u.username else u.id} - Balance: {u.balance} - Created: {arrow.get(u.created_time).humanize()}' for u in wealthier_10_users])
        },
        {
            'title': 'Last 10 Users:',
            'value': '\n\t' + '\n\t'.join([f'{u.username if u.username else u.id} - Balance: {u.balance} - Created: {arrow.get(u.created_time).humanize()}' for u in last_10_users])
        }
    ]

    print_section('User Statistics', user_statistics)

    owed_balance = ''.join([f'{int(u.balance_sum)}' for u in User.select(fn.Sum(User.balance).alias('balance_sum'))])
    total_deposits = ''.join([f'{int(d.amount_sum)}' for d in Deposit.select(fn.Sum(Deposit.amount).alias('amount_sum'))])
    total_withdrawals = ''.join([f'{int(d.amount_sum)}' for d in Withdrawal.select(fn.Sum(Withdrawal.amount).alias('amount_sum'))])

    w_d_ratio = round((float(total_withdrawals)/float(total_deposits)) * 100, 1)

    profit_sat = int(total_deposits) - (int(total_withdrawals) + int(owed_balance))
    profit_btc = profit_sat / 100000000

    balance_statistics = [
        {
            'title': 'Owed Balance',
            'value': f'{owed_balance}'
        },
        {
            'title': 'Total Deposits',
            'value': f'{total_deposits}'
        },
        {
            'title': 'Total Withdrawals',
            'value': f'{total_withdrawals}'
        },
        {
            'title': 'Withdrawal/Deposit Ratio',
            'value': f'{w_d_ratio}%'
        },
        {
            'title': 'Current Profit',
            'value': f'{profit_sat} satoshi ({profit_btc} btc)'
        }
    ]

    print_section('Balance Statistics', balance_statistics)

    slot_bet = 0
    slot_prize = 0

    for l in Log.select().where(Log.event == 'play', Log.game == 1):
        info = json.loads(l.info)
        slot_bet += info.get('bet')
        slot_prize += info.get('prize')

    game_statistics = [
        {
            'title': 'Slot Bet',
            'value': f'{slot_bet}'
        },
        {
            'title': 'Slot Prize',
            'value': f'{slot_prize}'
        },
        {
            'title': 'Slot Profit',
            'value': f'{slot_bet - slot_prize} ({round(((slot_bet/slot_prize) - 1) * 100, 2) if slot_prize > 0 else "N/A"}%)'
        }
    ]

    print_section('Game Statistics', game_statistics)


if __name__ == '__main__':
    run()
