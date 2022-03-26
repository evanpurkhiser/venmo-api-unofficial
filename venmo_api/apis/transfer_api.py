from venmo_api import (
    ApiClient,
    TransferType,
    TransferOptions,
    TransferTarget,
    deserialize,
    wrap_callback,
    NotTransferOptionsException,
)
from typing import Union


class TransferApi(object):
    def __init__(self, profile, api_client: ApiClient):
        super().__init__()
        self.__profile = profile
        self.__api_client = api_client

    def get_transfer_options(self, callback=None) -> Union[TransferOptions, None]:
        """
        Get a list of available transfer options
        """

        wrapped_callback = wrap_callback(callback=callback, data_type=TransferOptions)

        resource_path = "/transfers/options"
        response = self.__api_client.call_api(
            resource_path=resource_path, method="GET", callback=wrapped_callback
        )
        # return the thread
        if callback:
            return

        return deserialize(response=response, data_type=TransferOptions)

    def initiate_transfer(
        self,
        amount: float,
        target: TransferTarget = None,
        transfer_type: TransferType = None,
        callback=None,
    ) -> Union[bool, None]:
        """
        Transfer [amount] money into the [destination_id] account.
        :param amount: <int> the ammount to transfer (in cents)
        :param target: <TransferTarget> The destination of the transfer. If left unset the first traget will be used
        :param transfer_type <TransferType> The type of transfer (instant or standard)
        :param callback: <function> Passing callback will run it in a distinct thread, and returns Thread
        :return: <bool> Either the transfer was successfully initiated or an exception will rise.
        """
        amount = abs(amount)

        if transfer_type is None:
            transfer_type = TransferType.STANDARD

        if not target:
            options = self.get_transfer_options()
            if not options:
                raise NotTransferOptionsException()
            target = options.transfer_targets[0]
            if not target:
                raise NotTransferOptionsException()

        body = {
            "amount": amount,
            "destination_id": target.id,
            "final_amount": amount,
            "transfer_type": transfer_type.value,
        }

        resource_path = "/transfers"
        wrapped_callback = wrap_callback(callback=callback, data_type=None)

        self.__api_client.call_api(
            resource_path=resource_path,
            method="POST",
            body=body,
            callback=wrapped_callback,
        )

        if callback:
            return

        return True
