import hashlib
import hmac
import time
import requests
import urllib3

# USAGE:
# instantiate OST Kit with API credentials
# ostkit = OSTKit(api_url=OSTKIT_API_URL,
#                 api_key=OSTKIT_API_KEY,
#                 api_secret=OSTKIT_API_SECRET)
#
# execute API endpoint methods
# r = ostkit.users.create('Jason')
#
# response JSON is automatically converted to a dictionary
# user_id = r['data']['user']['id']


class OSTKitBase(object):
    def __init__(self, api_url, api_key, api_secret):
        if not api_url or not api_key or not api_secret:
            raise Exception("OSTKit is improperly configured")

        # strip trailing slash of api base url
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.api_secret = api_secret


class OSTKit(OSTKitBase):
    def __init__(self, *args, **kwargs):
        super(OSTKit, self).__init__(*args, **kwargs)

        # instantiate all supported endpoints for convenience
        self.users = UsersEndpoint(self.api_url, self.api_key, self.api_secret)
        self.airdrops = AirdropsEndpoint(self.api_url, self.api_key, self.api_secret)
        self.actions = ActionsEndpoint(self.api_url, self.api_key, self.api_secret)
        self.transactions = TransactionsEndpoint(self.api_url, self.api_key, self.api_secret)
        self.balances = BalancesEndpoint(self.api_url, self.api_key, self.api_secret)
        self.ledger = LedgerEndpoint(self.api_url, self.api_key, self.api_secret)
        self.transfers = TransfersEndpoint(self.api_url, self.api_key, self.api_secret)
        self.token = TokenEndpoint(self.api_url, self.api_key, self.api_secret)


class OSTKitEndpoint(OSTKitBase):
    endpoint = None

    def get(self, endpoint=None, params=None):
        return self.signed_request(method='get', endpoint=endpoint, params=params)

    def post(self, endpoint=None, params=None):
        return self.signed_request(method='post', endpoint=endpoint, params=params)

    def signed_request(self, method, endpoint=None, params=None):
        if method not in ('get', 'post'):
            raise Exception("Invalid method for OSTKit signed request")

        # use configured endpoint if none supplied
        if endpoint is None:
            endpoint = self.endpoint

        if not endpoint:
            raise Exception("Invalid endpoint for OSTKit signed request")

        # it's OK if there are no additional request params
        if params is None:
            params = {}

        # required params that go with each api request
        auth_params = {
            'api_key': self.api_key,
            'request_timestamp': int(time.time()),
        }

        # merge request-specific params
        params.update(auth_params)

        # build alphabetically sorted querystring
        querystring = urllib3.request.urlencode(sorted(params.items()))

        # sign our request using the endpoint plus all the params
        string_to_sign = endpoint + '?' + querystring

        # SHA256 hash the request using our secret key
        signature = hmac.new(self.api_secret.encode('utf-8'), msg=string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

        # now add our signature to request params
        params['signature'] = signature

        # API url for OST Kit Alpha
        request_url = self.api_url + endpoint

        if method == 'get':
            # GET request: params are in querystring
            r = requests.get(url=request_url, params=params)
        else:
            # POST request: parms are in form-encoded POST body
            r = requests.post(url=request_url, data=params)

        # parse response json
        return r.json()


class UsersEndpoint(OSTKitEndpoint):
    endpoint = '/users/'

    # https://dev.ost.com/docs/api_users_create.html
    def create(self, name):
        if not name:
            raise Exception("Invalid name for OSTKit create user")

        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.post(params={
            'name': name,
        })

    # https://dev.ost.com/docs/api_users_edit.html
    def update(self, user_id, name):
        if not user_id or not name:
            raise Exception("Invalid user id or username for OSTKit update user")

        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.post(endpoint=self.endpoint + user_id, params={
            'name': name
        })

    # https://dev.ost.com/docs/api_users_retrieve.html
    def retrieve(self, user_id):
        if not user_id:
            raise Exception("Invalid user id for OSTKit retrieve user")

        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.get(endpoint=self.endpoint + user_id)

    # https://dev.ost.com/docs/api_users_list.html
    def list(self, **kwargs):
        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.get(params=dict(kwargs))


class AirdropsEndpoint(OSTKitEndpoint):
    endpoint = '/airdrops/'

    # https://dev.ost.com/docs/api_airdrop_execute.html
    def execute(self, amount, user_ids, **kwargs):
        if not amount or not user_ids:
            raise Exception("Invalid amount or user ids for OSTKit execute airdrop")

        # required params
        params = {
            'amount': amount,
            'user_ids': ",".join(user_ids) if isinstance(user_ids, (list, tuple)) else user_ids,  # allows string or list
        }

        # merge additional params
        params.update(dict(kwargs))

        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.post(params=params)

    # https://dev.ost.com/docs/api_airdrop_retrieve.html
    def retrieve(self, airdrop_id):
        if not id:
            raise Exception("Invalid airdrop id for OSTKit retrieve airdrop")

        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.get(endpoint=self.endpoint + airdrop_id)

    # https://dev.ost.com/docs/api_airdrop_list.html
    def list(self, **kwargs):
        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.get(params=dict(kwargs))


class ActionsEndpoint(OSTKitEndpoint):
    endpoint = '/actions/'

    # https://dev.ost.com/docs/api_actions_create.html
    def create(self, name, kind, currency='BT', **kwargs):
        if not name \
                or kind not in ('user_to_user', 'company_to_user', 'user_to_company') \
                or currency not in ('BT', 'USD'):
            raise Exception("Invalid configuration for OSTKit create action")

        # required params
        params = {
            'name': name,
            'kind': kind,
            'currency': currency,
        }

        # merge additional params
        params.update(dict(kwargs))

        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.post(params=params)

    # https://dev.ost.com/docs/api_actions_update.html
    def update(self, action_id, **kwargs):
        if not action_id:
            raise Exception("Invalid action ID for OSTKit update action")

        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.post(endpoint=self.endpoint + str(action_id), params=dict(kwargs))

    # https://dev.ost.com/docs/api_actions_retrieve.html
    def retrieve(self, action_id):
        if not action_id:
            raise Exception("Invalid action ID for OSTKit retrieve action")

        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.get(endpoint=self.endpoint + str(action_id))

    # https://dev.ost.com/docs/api_actions_list.html
    def list(self, **kwargs):
        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.get(params=dict(kwargs))


class TransactionsEndpoint(OSTKitEndpoint):
    endpoint = '/transactions/'

    # https://dev.ost.com/docs/api_action_execute.html
    def execute(self, from_user_id, to_user_id, action_id, **kwargs):
        if not from_user_id or not to_user_id or not action_id:
            raise Exception("Invalid parameters for OSTKit execute transaction")

        # required params
        params = {
            'from_user_id': from_user_id,
            'to_user_id': to_user_id,
            'action_id': action_id,
        }

        # merge additional params
        params.update(dict(kwargs))

        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.post(params=params)

    # https://dev.ost.com/docs/api_transaction_retrieve.html
    def retrieve(self, transaction_id):
        if not transaction_id:
            raise Exception("Invalid transaction ID for OSTKit retrieve transaction")

        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.get(endpoint=self.endpoint + transaction_id)

    # https://dev.ost.com/docs/api_transaction_list.html
    def list(self, **kwargs):
        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.get(params=dict(kwargs))


class BalancesEndpoint(OSTKitEndpoint):
    endpoint = '/balances/'

    # https://dev.ost.com/docs/api_balance.html
    def retrieve(self, user_id):
        if not user_id:
            raise Exception("Invalid user id for OSTKit retrieve balance")

        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.get(endpoint=self.endpoint + user_id)


class LedgerEndpoint(OSTKitEndpoint):
    endpoint = '/ledger/'

    # https://dev.ost.com/docs/api_ledger.html
    def retrieve(self, user_id, **kwargs):
        if not user_id:
            raise Exception("Invalid user id for OSTKit retrieve ledger")

        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.get(endpoint=self.endpoint + user_id, params=dict(kwargs))


class TransfersEndpoint(OSTKitEndpoint):
    endpoint = '/transfers/'

    # https://dev.ost.com/docs/api_transfers_create.html
    def create(self, to_address, amount, **kwargs):
        if not to_address or not amount:
            raise Exception("Invalid address or amount for OSTKit create transfer")

        # required params
        params = {
            'to_address': to_address,
            'amount': amount,
        }

        # merge additional params
        params.update(dict(kwargs))

        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.post(params=params)

    # https://dev.ost.com/docs/api_transfers_retrieve.html
    def retrieve(self, transfer_id):
        if not transfer_id:
            raise Exception("Invalid transfer ID for OSTKit retrieve transfer")

        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.get(endpoint=self.endpoint + str(transfer_id))

    # https://dev.ost.com/docs/api_transfers_list.html
    def list(self, **kwargs):
        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.get(params=dict(kwargs))


class TokenEndpoint(OSTKitEndpoint):
    endpoint = '/token/'

    # https://dev.ost.com/docs/api_token.html
    def retrieve(self):
        # make signed request to OST Kit, return parsed JSON -> dictionary
        return self.get()
