
import arrow

from typing import Tuple, Union

from conf import conf
from lncityapi.models.user import User
from lncityapi.services.lnd import lnd
from lncityapi.models.balance import Deposit


def generate_deposit_invoice(user: User, amount: int) -> Tuple[int, Union[str, dict]]:
    invoice = lnd.generate_invoice(amount, f'Deposit {amount} into ln.city')

    if invoice is None:
        return 503, 'Unable to make a deposit right now'

    r_hash = invoice.get('r_hash')

    Deposit.create(
        user=user.id,
        amount=amount,
        r_hash=r_hash,
        expiration_date=arrow.get().shift(seconds=2*conf.get('INVOICE_TIMEOUT')).datetime,
        settled=0
    )

    return 200, invoice


def try_update_balance_with_deposit_invoice(r_hash: str) -> bool:

    pending_deposit = None
    for pd in Deposit.select().where(Deposit.r_hash == r_hash, Deposit.settled == 0):
        pending_deposit = pd

    if pending_deposit is None:
        return False

    lines_changed = Deposit.update(settled=1)\
        .where(Deposit.settled == 0, Deposit.r_hash == r_hash).execute()

    if lines_changed > 0:
        User.update(balance=User.balance+pending_deposit.amount).where(User.id == pending_deposit.user_id).execute()
        return True

    return False


def verify_pending_deposits_for_user(user: User):
    pending_deposits = []
    for pd in Deposit.select().where(Deposit.user == user.id, Deposit.settled == 0):
        pending_deposits.append(pd)

    if not pending_deposits:
        return user

    balance_updated = False
    for pd in pending_deposits:
        invoice = lnd.get_invoice(pd.r_hash)
        if invoice.get('settled', False):
            balance_updated = balance_updated or try_update_balance_with_deposit_invoice(pd.r_hash)

    if balance_updated:
        for u in User.select().where(User.id == user.id):
            return u

    return user
