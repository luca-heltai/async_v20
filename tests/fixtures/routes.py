from .static import *

routes = {
    ('GET', '/v3/accounts'): list_accounts_response,
    ('GET', '/v3/accounts/123-123-1234567-123'): get_account_details_response,
    ('GET', '/v3/accounts/123-123-1234567-123/summary'): account_summary_response,
    ('GET', '/v3/accounts/123-123-1234567-123/instruments'): account_instruments_response,
    ('PATCH', '/v3/accounts/123-123-1234567-123/configuration'): None,
    ('GET', '/v3/accounts/123-123-1234567-123/changes'): account_changes_response,
    ('GET', '/v3/instruments/AUD_USD/candles'): get_candles_response,
    ('POST', '/v3/accounts/123-123-1234567-123/orders'): create_order_response,
    ('GET', '/v3/accounts/123-123-1234567-123/orders'): list_orders_response,
    ('GET', '/v3/accounts/123-123-1234567-123/pendingOrders'): None,
    ('GET', '/v3/accounts/123-123-1234567-123/orders/123-123-1234567-123/'): None,
    ('PUT', '/v3/accounts/123-123-1234567-123/orders/123-123-1234567-123/'): None,
    ('PUT', '/v3/accounts/123-123-1234567-123/orders/0000/cancel'): None,
    ('PUT', '/v3/accounts/123-123-1234567-123/orders/0000/clientExtensions'): None,
    ('GET', '/v3/accounts/123-123-1234567-123/positions'): list_positions_response,
    ('GET', '/v3/accounts/123-123-1234567-123/openPositions'): None,
    ('GET', '/v3/accounts/123-123-1234567-123/positions/0000'): None,
    ('PUT', '/v3/accounts/123-123-1234567-123/positions/0000'): None,
    ('GET', '/v3/accounts/123-123-1234567-123/pricing'): get_pricing_response,
    ('GET', '/v3/accounts/123-123-1234567-123/pricing/stream'): None,
    ('GET', '/v3/accounts/123-123-1234567-123/trades'): None,
    ('GET', '/v3/accounts/123-123-1234567-123/openTrades'): list_open_trades_response,
    ('GET', '/v3/accounts/123-123-1234567-123/trades/0000'): None,
    ('PUT', '/v3/accounts/123-123-1234567-123/trades/0000/close'): close_all_trades_response,
    ('PUT', '/v3/accounts/123-123-1234567-123/trades/0000/clientExtensions'): None,
    ('PUT', '/v3/accounts/123-123-1234567-123/trades/0000/orders'): None,
    ('GET', '/v3/accounts/123-123-1234567-123/transactions'): None,
    ('GET', '/v3/accounts/123-123-1234567-123/transactions/0000'): None,
    ('GET', '/v3/accounts/123-123-1234567-123/transactions/idrange'): None,
    ('GET', '/v3/accounts/123-123-1234567-123/transactions/sinceid'): None,
    ('GET', '/v3/accounts/123-123-1234567-123/transactions/stream'): None,
    ('GET', '/v3/users/123-123-1234567-123'): None,
    ('GET', '/v3/users/123-123-1234567-123/externalInfo'): None}
