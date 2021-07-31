
import arrow
import logging

from typing import Tuple, Union

from flask_login import current_user

from conf import conf
from lncityapi.controllers.notificationscontroller import add_notification
from lncityapi.models import User, Deposit, Withdrawal
from lncityapi.services import lnd

from lncityapi import db


def expire_deposit_invoices():
    Deposit.delete().where(Deposit.expired_time > arrow.get().timestamp()).execute()


def generate_deposit_invoice_for_user(user: User, amount: int) -> Tuple[int, Union[str, dict]]:
    invoice = lnd.generate_invoice(amount, f'Deposit {amount} into ln.city')

    if invoice is None:
        return 503, 'Unable to make a deposit right now'

    r_hash = invoice.get('r_hash')

    created_time = arrow.get().timestamp()
    expired_time = created_time + 2 * conf.get('INVOICE_TIMEOUT')

    Deposit.create(
        user=user.id,
        amount=amount,
        r_hash=r_hash,
        created_time=created_time,
        expired_time=expired_time,
        settled=0
    )

    return 200, invoice


def try_update_balance_with_deposit_invoice(r_hash: str) -> bool:

    pending_deposit = None
    for pd in Deposit.select().where(Deposit.r_hash == r_hash, Deposit.settled == 0):
        pending_deposit = pd

    if pending_deposit is None:
        return False

    lines_changed = Deposit.update(settled=1, expired_time=None)\
        .where(Deposit.settled == 0, Deposit.r_hash == r_hash).execute()

    if lines_changed > 0:
        User.update(balance=User.balance+pending_deposit.amount).where(User.id == pending_deposit.user_id).execute()

        add_notification(current_user, None, 'deposit', {
            'amount': pending_deposit.amount
        }, True)

        return True

    return False


def verify_pending_deposits_for_user(user: User) -> User:
    pending_deposits = []
    for pd in Deposit.query.filter_by(user_id=user.id, settled=0):
        pending_deposits.append(pd)

    if not pending_deposits:
        return user

    balance_updated = False
    for pd in pending_deposits:
        invoice = lnd.get_invoice(pd.r_hash)
        if invoice.get('settled', False):
            balance_updated = balance_updated or try_update_balance_with_deposit_invoice(pd.r_hash)

    if balance_updated:
        db.session.refresh(user)

    return user


def withdraw_balance_for_user(user: User, payment_request: str) -> Tuple[int, Union[str, dict]]:

    decoded_payment_request = lnd.decode_payment_request(payment_request)

    if decoded_payment_request is None:
        return 400, 'Unable to decode payment request'

    amount = decoded_payment_request.get('num_satoshis')

    if not amount:
        return 400, 'Unable to decode amount'

    amount = int(amount)

    if amount == 0:
        return 400, 'Please specify an amount'

    for _ in Withdrawal.select().where(Withdrawal.user == user.id, Withdrawal.settled == 0):
        return 400, 'Another withdrawal already ongoing'

    withdrawal = Withdrawal.create(
        user=user.id,
        amount=amount,
        created_time=arrow.get().timestamp(),
        settled=0
    )

    for w in Withdrawal.select().where(Withdrawal.user == user.id, Withdrawal.settled == 0):
        if withdrawal.id != w.id:
            withdrawal.delete_instance()
            return 400, 'Another withdrawal already ongoing'

    updated_user = None
    for u in User.select().where(User.id == user.id):
        updated_user = u

    if updated_user is None:
        withdrawal.delete_instance()
        return 400, 'Unknown error'

    success = add_user_balance(updated_user, -amount)

    if not success:
        withdrawal.delete_instance()
        return 412, 'Not enough balance'

    try:
        result = lnd.pay_payment_request(payment_request)

        if result.get('payment_error') is not None:
            add_user_balance(updated_user, amount)
            withdrawal.delete_instance()
            return 503, 'Unable to process request'
    except Exception as e:
        logging.debug(f'Exception: {e}', exc_info=True)
        add_user_balance(updated_user, amount)
        withdrawal.delete_instance()
        return 400, 'Unknown error'

    withdrawal.settled = 1
    withdrawal.save()

    add_notification(current_user, None, 'withdraw', {
        'amount': amount
    }, True)

    return 200, 'Payment sent'


def add_user_balance(user, amount):
    if amount >= 0:
        user.balance += amount
        db.session.commit()
        db.session.refresh(user)
        return True
    else:
        db_user = User.query.filter(User.id == user.id, User.balance >= -amount).with_for_update().first()
        if db_user is not None:
            db_user.balance += amount

        db.session.commit()
        db.session.refresh(user)

        return db_user is not None
