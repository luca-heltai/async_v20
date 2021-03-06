from .decorators import endpoint
from ..definitions.types import ClientExtensions
from ..definitions.types import InstrumentName
from ..definitions.types import StopLossDetails
from ..definitions.types import TakeProfitDetails
from ..definitions.types import TradeID
from ..definitions.types import TradeSpecifier
from ..definitions.types import TradeStateFilter
from ..definitions.types import TrailingStopLossDetails
from ..endpoints.annotations import Count
from ..endpoints.annotations import Ids
from ..endpoints.annotations import Units
from ..endpoints.trade import *

__all__ = ['TradeInterface']


class TradeInterface(object):
    @endpoint(GETTrades)
    def list_trades(self,
                    ids: Ids = ...,
                    state: TradeStateFilter = ...,
                    instrument: InstrumentName = ...,
                    count: Count = ...,
                    trade_id: TradeID = ...):
        """
        Get a list of Trades for an Account

        Args:
            ids: :class:`~async_v20.endpoints.annotations.Ids`
                List of Trade IDs to retrieve.
            state: :class:`~async_v20.definitions.primitives.TradeStateFilter`
                The state to filter the requested Trades by.
            instrument: :class:`~async_v20.definitions.primitives.InstrumentName`
                The instrument to filter the requested Trades by.
            count: :class:`~async_v20.endpoints.annotations.Count`
                The maximum number of Trades to return.
            trade_id: :class:`~async_v20.definitions.primitives.TradeID`
                The maximum Trade ID to return. If not provided the most recent
                Trades in the Account are returned.

        Returns:

            status [200]
                :class:`~async_v20.interface.response.Response`
                (trades= :class:`~async_v20.definitions.types.ArrayTrade`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

        """
        pass

    @endpoint(GETOpenTrades)
    def list_open_trades(self):
        """
        Get the list of open Trades for an Account

        Returns:

            status [200]
                :class:`~async_v20.interface.response.Response`
                (trades= :class:`~async_v20.definitions.types.ArrayTrade`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)
        """
        pass

    @endpoint(GETTradeSpecifier)
    def get_trades(self, trade_specifier: TradeSpecifier = ...):
        """
        Get the details of a specific Trade in an Account

        Args:

            trade_specifier: :class:`~async_v20.definitions.primitives.TradeSpecifier`
                Specifier for the Trade

        Returns:

            status [200]
                :class:`~async_v20.interface.response.Response`
                (trade= :class:`~async_v20.definitions.types.Trade`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

        """
        pass

    @endpoint(PUTTradeSpecifierClose)
    def close_trade(self,
                     trade_specifier: TradeSpecifier = ...,
                     units: Units = ...):
        """
        Close (partially or fully) a specific open Trade in an Account

        Args:

            trade_specifier: :class:`~async_v20.definitions.primitives.TradeSpecifier`
                Specifier for the Trade
            units: :class:`~async_v20.endpoints.annotations.Units`
                Indication of how much of the Trade to close. Either the string
                "ALL" (indicating that all of the Trade should be closed), or a
                DecimalNumber representing the number of units of the open
                Trade to Close using a TradeClose MarketOrder. The units
                specified must always be positive, and the magnitude of the
                value cannot exceed the magnitude of the Trade's open units.

        Returns:

            status [200]
                :class:`~async_v20.interface.response.Response`
                (orderCreateTransaction= :class:`~async_v20.definitions.types.MarketOrderTransaction`,
                orderFillTransaction= :class:`~async_v20.definitions.types.OrderFillTransaction`,
                orderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.MarketOrderRejectTransaction`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

            status [401]
                :class:`~async_v20.interface.response.Response`
                (orderRejectTransaction= :class:`~async_v20.definitions.types.MarketOrderRejectTransaction`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)
        """
        pass

    @endpoint(PUTTradeSpecifierClientExtensions)
    def set_client_extensions_trade(self,
                                    trade_specifier: TradeSpecifier = ...,
                                    client_extensions: ClientExtensions = ...):
        """
        Update the Client Extensions for a Trade. Do not add, update, or delete
        the Client Extensions if your account is associated with MT4.

        Args:

            trade_specifier: :class:`~async_v20.definitions.primitives.TradeSpecifier`
                Specifier for the Trade
            client_extensions: :class:`~async_v20.definitions.types.ClientExtensions`
                The Client Extensions to update the Trade with. Do not add,
                update, or delete the Client Extensions if your account is
                associated with MT4.

        Returns:

            status [200]
                :class:`~async_v20.interface.response.Response`
                (tradeClientExtensionsModifyTransaction=
                :class:`~async_v20.definitions.types.TradeClientExtensionsModifyTransaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (tradeClientExtensionsModifyRejectTransaction=
                :class:`~async_v20.definitions.types.TradeClientExtensionsModifyRejectTransaction`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)

            status [401]
                :class:`~async_v20.interface.response.Response`
                (tradeClientExtensionsModifyRejectTransaction=
                :class:`~async_v20.definitions.types.TradeClientExtensionsModifyRejectTransaction`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)
        """
        pass

    @endpoint(PUTTradesSpecifierOrders)
    def set_dependent_orders_trade(self,
                                   trade_specifier: TradeSpecifier = ...,
                                   take_profit: TakeProfitDetails = ...,
                                   stop_loss: StopLossDetails = ...,
                                   trailing_stop_loss: TrailingStopLossDetails = ...):
        """
        Create, replace and cancel a Trade's dependent Orders (Take Profit,
        Stop Loss and Trailing Stop Loss) through the Trade itself

        Args:

            trade_specifier: :class:`~async_v20.definitions.primitives.TradeSpecifier`
                Specifier for the Trade
            take_profit: :class:`~async_v20.definitions.types.TakeProfitDetails`
                The specification of the Take Profit to create/modify/cancel.
                If takeProfit is set to null, the Take Profit Order will be
                cancelled if it exists. If takeProfit is not provided, the
                existing Take Profit Order will not be modified. If a sub-
                field of takeProfit is not specified, that field will be set to
                a default value on create, and be inherited by the replacing
                order on modify.
            stop_loss: :class:`~async_v20.definitions.types.StopLossDetails`
                The specification of the Stop Loss to create/modify/cancel. If
                stopLoss is set to null, the Stop Loss Order will be cancelled
                if it exists. If stopLoss is not provided, the existing Stop
                Loss Order will not be modified. If a sub-field of stopLoss is
                not specified, that field will be set to a default value on
                create, and be inherited by the replacing order on modify.
            trailing_stop_loss: :class:`~async_v20.definitions.types.TrailingStopLossDetails`
                The specification of the Trailing Stop Loss to
                create/modify/cancel. If trailingStopLoss is set to null, the
                Trailing Stop Loss Order will be cancelled if it exists. If
                trailingStopLoss is not provided, the existing Trailing Stop
                Loss Order will not be modified. If a sub-field of
                trailingStopLoss is not specified, that field will be set to a
                default value on create, and be inherited by the replacing
                order on modify.

        Returns:

            status [200]
                :class:`~async_v20.interface.response.Response`
                (takeProfitOrderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                takeProfitOrderTransaction= :class:`~async_v20.definitions.types.TakeProfitOrderTransaction`,
                takeProfitOrderFillTransaction= :class:`~async_v20.definitions.types.OrderFillTransaction`,
                takeProfitOrderCreatedCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                stopLossOrderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                stopLossOrderTransaction= :class:`~async_v20.definitions.types.StopLossOrderTransaction`,
                stopLossOrderFillTransaction= :class:`~async_v20.definitions.types.OrderFillTransaction`,
                stopLossOrderCreatedCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                trailingStopLossOrderCancelTransaction= :class:`~async_v20.definitions.types.OrderCancelTransaction`,
                trailingStopLossOrderTransaction= :class:`~async_v20.definitions.types.TrailingStopLossOrderTransaction`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`)

            status [400]
                :class:`~async_v20.interface.response.Response`
                (takeProfitOrderCancelRejectTransaction=
                :class:`~async_v20.definitions.types.OrderCancelRejectTransaction`,
                takeProfitOrderRejectTransaction= :class:`~async_v20.definitions.types.TakeProfitOrderRejectTransaction`,
                stopLossOrderCancelRejectTransaction= :class:`~async_v20.definitions.types.OrderCancelRejectTransaction`,
                stopLossOrderRejectTransaction= :class:`~async_v20.definitions.types.StopLossOrderRejectTransaction`,
                trailingStopLossOrderCancelRejectTransaction=
                :class:`~async_v20.definitions.types.OrderCancelRejectTransaction`,
                trailingStopLossOrderRejectTransaction=
                :class:`~async_v20.definitions.types.TrailingStopLossOrderRejectTransaction`,
                lastTransactionID= :class:`~async_v20.definitions.primitives.TransactionID`,
                relatedTransactionIDs= :class:`~async_v20.definitions.types.ArrayTransactionID`,
                errorCode= :class:`~builtins.str`,
                errorMessage= :class:`~builtins.str`)
        """
        pass
