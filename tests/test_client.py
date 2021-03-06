import asyncio
import inspect
import os
import re
import time

import pytest

from async_v20 import AccountID
from async_v20.client import OandaClient
from async_v20.endpoints.annotations import Authorization
from .fixtures import server as server_module
from .fixtures.client import client
from .test_definitions.helpers import get_valid_primitive_data
from async_v20.definitions.types import Account
from .fixtures import changes_response_two
from .fixtures import all_trades_open_closed
from .fixtures.static import close_all_trades_response
from itertools import chain

client = client
server = server_module.server
changes_response_two = changes_response_two


# prevent pycharm from removing the import


def test_oanda_client_has_correct_version(client):
    try:
        path = r'C:\Users\James\PycharmProjects\async_v20\setup.py'
        print(path)
        with open(path, 'r') as f:
            setup = f.read()
    except FileNotFoundError as e:
        print(e)
    else:
        setup_version = re.findall(r"(?<=version\s=\s').*?(?='\n)", setup)[0]
        assert setup_version == client.version


def test_oanda_client_finds_token():
    os.environ['OANDA_TOKEN'] = 'test_environ_token'
    client = OandaClient()
    assert client.default_parameters[Authorization] == 'Bearer test_environ_token'


def test_oanda_client_accepts_token():
    client = OandaClient(token='test_token')
    assert client.default_parameters[Authorization] == 'Bearer test_token'


def test_oanda_client_constructs_url(client):
    assert client.hosts['REST'](path='test').human_repr() == 'http://127.0.0.1:8080/test'
    assert client.hosts['STREAM'](path='test').human_repr() == 'http://127.0.0.1:8080/test'


@pytest.mark.asyncio
async def test_client_initializes(client, server):
    server.status = 200
    try:
        await client.initialize()
        assert client.default_parameters[AccountID] == AccountID('123-123-1234567-123')
    except:
        assert 0
    finally:
        client.close()
        assert client.session.closed == True


error_status = [i for i in range(400, 600)]


@pytest.mark.asyncio
@pytest.mark.parametrize('error_status', error_status)
async def test_client_raises_error_on_first_initialisation_failure(client, server, error_status):
    server_module.status = 400
    with pytest.raises(ConnectionError):
        await client.initialize()
    assert client.initialized == False
    assert client.initializing == False


@pytest.mark.asyncio
@pytest.mark.parametrize('error_status', error_status)
async def test_client_raises_error_on_second_initialisation_failure(client, server, error_status):
    server_module.status = iter([200, 400])
    with pytest.raises(ConnectionError):
        await client.initialize()
    assert client.initialized == False
    assert client.initializing == False


@pytest.mark.asyncio
async def test_initialize_works_with_preset_account_id(client, server):
    client.account_id = '123-123-1234567-123'
    async with client as client:
        assert client.account_id == '123-123-1234567-123'


@pytest.mark.asyncio
async def test_aenter_and_aexit(client, server):
    global status
    status = 200
    async with client as client:
        assert client.session.closed == False
    assert client.session.closed == True


@pytest.mark.asyncio
async def test_async_with_initializes(client, server):
    global status
    status = 200
    async with client as client:
        assert client.default_parameters[AccountID] == AccountID('123-123-1234567-123')


@pytest.mark.asyncio
async def test_response_boolean_evaluation(client, server):
    global status
    status = 200
    async with client as client:
        response = await client.list_accounts()
    assert bool(response) == True


@pytest.mark.asyncio
async def test_response_returns_json(client, server):
    global status
    status = 200
    async with client as client:
        accounts = await client.list_accounts()
        account_details = await client.get_account_details()
        pricing = await client.get_pricing()

    assert accounts.dict()
    assert account_details.dict()
    assert pricing.dict()


@pytest.mark.asyncio
async def test_enter_causes_warning(client, server, capsys):
    with client as client:
        assert capsys.readouterr()[0] == 'Warning: <with> used rather than <async with>\n'


def test_client_request_limiter_minimum_value(client):
    client.max_requests_per_second = 0
    assert client.max_requests_per_second == 1


@pytest.mark.asyncio
async def test_request_limiter_limits(client, server, event_loop):
    client.max_simultaneous_connections = 0
    client.max_requests_per_second = 1000
    concurrent_requests = 100
    start = time.time()
    async with client as client:
        await asyncio.gather(*[client.list_orders() for _ in range(concurrent_requests)])
    time_taken = time.time() - start
    print(time_taken)
    assert time_taken >= (concurrent_requests / client.max_requests_per_second)


@pytest.mark.asyncio
async def test_client_time_out(client, server):
    server_module.sleep_time = 10
    client.poll_timeout = 0.1
    with pytest.raises(TimeoutError):
        async with client as client:
            pass


@pytest.mark.asyncio
@pytest.mark.parametrize('method', inspect.getmembers(OandaClient, lambda x: True if hasattr(x, 'shortcut') or
                                                                                     hasattr(x, 'endpoint') else False))
async def test_client_handles_multiple_concurrent_initializations(client, server, method):
    # Method is a tuple of attribute, function
    client.initialization_sleep = 0  # Make this small to speed up tests
    data = tuple(get_valid_primitive_data(param.annotation)
                 for param in method[1].__signature__.parameters.values()
                 if param.name not in 'self cls')
    method = getattr(client, method[0])
    try:
        await asyncio.gather(*[method(*data) for _ in range(5)])
    except (AttributeError, ConnectionError):
        # Don't care if incorrect data or status is returned)
        # Just want to make sure the client always initializes correctly
        pass
    assert client.initialized

@pytest.mark.asyncio
async def test_account_method(client, server):
    async with client as client:
        assert len(client._account.trades) == 0
        account = await client.account()
        assert len(client._account.trades) == 1
        assert type(account)== Account



@pytest.mark.asyncio
async def test_max_transaction_history_limits(client, server, changes_response_two):
    async with client as client:
        rsp = await client.account_changes()
    assert len(client.transactions) == client.max_transaction_history

@pytest.mark.asyncio
async def test_close_all_trades_returns_false_when_trades_are_open(client, server):
    """Test that calling closed trades closes all trades"""
    async with client as client:
        trades_response = await client.list_open_trades()
        result, close_responses = await client.close_all_trades()
        closed_trades = {i.orderFillTransaction.trades_closed[0].trade_id :i.json()
                         for i in close_responses}
        for trade in trades_response.trades:
            assert trade.id in closed_trades
        # close_all_trades checks that no trades are open after giving the close command
        # Due to the mocked test server, not reflecting the closed state. result should
        # be false indicating that not all trades were closed
        assert result == False

@pytest.mark.asyncio
async def test_close_all_trades_returns_true_when_trades_are_closed(client, server, all_trades_open_closed):
    """Test that calling closed trades closes all trades"""

    # all_trades_open_closed fixture mocks changing server response
    # to closing all trades
    server_module.routes.update()
    async with client as client:
        result, close_responses = await client.close_all_trades()
        assert result == True


@pytest.mark.asyncio
async def test_close_all_trades_error_first_list_trades_request(client, server):
    async with client as client:
        server_module.status = 401
        with pytest.raises(ConnectionError):
            response = await client.close_all_trades()


@pytest.mark.asyncio
async def test_close_all_trades_error_second_list_trades_request(client, server):
    # status 200 for list_open_trades request
    # status 200 for all close_trades request
    # status 400 for second list_open_trades request
    server_status = (i for i in chain((200,),(200 for _ in range(len(close_all_trades_response))),(400,)))
    async with client as client:
        server_module.status = server_status
        with pytest.raises(ConnectionError):
            response = await client.close_all_trades()

@pytest.mark.asyncio
async def test_initialize_timeout_resets_initialization(client, server):
    with pytest.raises(TimeoutError):
        server_module.sleep_time = 10
        client.poll_timeout = 0.1
        async with client as client:
            assert client.initializing == False
            assert client.initialized == False

@pytest.mark.asyncio
async def test_initialize_connection_error_resets_initialization(client, server):
    with pytest.raises(ConnectionError):
        server_module.status = 400
        async with client as client:
            assert client.initializing == False
            assert client.initialized == False
