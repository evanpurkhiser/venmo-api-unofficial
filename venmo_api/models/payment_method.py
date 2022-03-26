from venmo_api import BaseModel
from typing import Dict
from enum import Enum
import logging


class PaymentMethod(BaseModel):
    def __init__(self, id: str, role: str, name: str, type: str, json=None):
        """
        Payment method model (with different types like, venmo balance, bank account, ...)
        """
        super().__init__()

        self.id = id
        self.role = PaymentRole(role)
        self.name = name
        self.type = payment_type.get(type)
        self._json = json

    @classmethod
    def from_json(cls, json: Dict):

        id = json.get("id")
        role = json.get("peer_payment_role")
        name = json.get("name")
        type = json.get("type")

        # Get the class for this payment, must be either VenmoBalance or BankAccount
        payment_class = payment_type.get(type)
        if not payment_class:
            logging.warning(
                f"Skipped a payment_method; No schema existed for the payment_method: {type}"
            )
            return

        return payment_class(id=id, role=role, name=name, type=type, json=json)


class VenmoBalance(PaymentMethod, BaseModel):
    def __init__(self, id, role, name, type, json=None):
        super().__init__(id, role, name, type, json)


class BankAccount(PaymentMethod, BaseModel):
    def __init__(self, id, role, name, type, json=None):
        super().__init__(id, role, name, type, json)


class Card(PaymentMethod, BaseModel):
    def __init__(self, id, role, name, type, json=None):
        super().__init__(id, role, name, type, json)


class PaymentRole(Enum):
    DEFAULT = "default"
    BACKUP = "backup"
    NONE = "none"


class PaymentPrivacy(Enum):
    PRIVATE = "private"
    PUBLIC = "public"
    FRIENDS = "friends"


payment_type = {"bank": BankAccount, "balance": VenmoBalance, "card": Card}
