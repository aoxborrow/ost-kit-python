# ost-kit-python
[![PyPI version](https://badge.fury.io/py/ost-kit-python.svg)](https://badge.fury.io/py/ost-kit-python)

An unofficial [OST Kit API](https://dev.ost.com/) wrapper for Python 2/3. Supports all functionality of OST Kit API v1.1.

# Installation

```
pip install ost-kit-python
```

# Usage #

```python
from ost_kit_python import OSTKit

# instantiate OST Kit with API credentials
ostkit = OSTKit(api_url='https://sandboxapi.ost.com/v1.1',
                api_key='OSTKIT_API_KEY',
                api_secret='OSTKIT_API_SECRET')

# execute API endpoint methods
r = ostkit.users.create('Jason')

# response JSON is automatically converted to a dictionary
user_id = r['data']['user']['id']
```

# More Examples #

```python

# https://dev.ost.com/docs/api_users_create.html
r = ostkit.users.create(name='James')

# https://dev.ost.com/docs/api_users_edit.html
r = ostkit.users.update(user_id='abcd-1234-some-guid', name='Jimothy')

# https://dev.ost.com/docs/api_users_retrieve.html
r = ostkit.users.retrieve(user_id='abcd-1234-some-guid')

# https://dev.ost.com/docs/api_users_list.html
r = ostkit.users.list(limit=100)

# https://dev.ost.com/docs/api_airdrop_execute.html
r = ostkit.airdrops.execute(amount=6.66, user_ids=('abcd-1234-some-guid',))

# https://dev.ost.com/docs/api_airdrop_retrieve.html
r = ostkit.airdrops.retrieve(airdrop_id='abcd-1234-some-guid')

# https://dev.ost.com/docs/api_airdrop_list.html
r = ostkit.airdrops.list()

# https://dev.ost.com/docs/api_actions_create.html
r = ostkit.actions.create(name='Bonus',
                          kind='company_to_user',
                          amount=3.33,
                          arbitrary_amount='false')

# https://dev.ost.com/docs/api_actions_update.html
r = ostkit.actions.update(action_id=1234, name='MajorBonus')

# https://dev.ost.com/docs/api_actions_retrieve.html
r = ostkit.actions.retrieve(action_id=1234)

# https://dev.ost.com/docs/api_actions_list.html
r = ostkit.actions.list()

# https://dev.ost.com/docs/api_action_execute.html
r = ostkit.transactions.execute(from_user_id='abcd-1234-some-guid',
                                to_user_id='abcd-1234-some-guid',
                                action_id=1234)

# https://dev.ost.com/docs/api_transaction_retrieve.html
r = ostkit.transactions.retrieve(transaction_id='abcd-1234-some-guid')

# https://dev.ost.com/docs/api_transaction_list.html
r = ostkit.transactions.list()

# https://dev.ost.com/docs/api_balance.html
r = ostkit.balances.retrieve(user_id='abcd-1234-some-guid')

# https://dev.ost.com/docs/api_ledger.html
r = ostkit.ledger.retrieve(user_id='abcd-1234-some-guid')

# https://dev.ost.com/docs/api_transfers_create.html
r = ostkit.transfers.create(to_address='0x123456', amount=6.66)

# https://dev.ost.com/docs/api_transfers_retrieve.html
r = ostkit.transfers.retrieve(transfer_id='abcd-1234-some-guid')

# https://dev.ost.com/docs/api_transfers_list.html
r = ostkit.transfers.list()

# https://dev.ost.com/docs/api_token.html
r = ostkit.token.retrieve()

```
