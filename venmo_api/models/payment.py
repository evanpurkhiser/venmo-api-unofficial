from venmo_api import parse_amount, string_to_timestamp, User, BaseModel
from enum import Enum



class Payment(BaseModel):
    def __init__(
        self,
        id,
        actor,
        target,
        action,
        amount,
        audience,
        date_created,
        date_reminded,
        date_completed,
        note,
        status,
        json=None,
    ):
        """
        Payment model
        """
        super().__init__()
        self.id = id
        self.actor = actor
        self.target = target
        self.action = action
        self.amount = amount
        self.audience = audience
        self.date_created = date_created
        self.date_reminded = date_reminded
        self.date_completed = date_completed
        self.note = note
        self.status = status
        self._json = json

    @classmethod
    def from_json(cls, json):
        """
        init a new Payment form JSON
        """
        if not json:
            return

        return cls(
            id=json.get("id"),
            actor=User.from_json(json.get("actor")),
            target=User.from_json(json.get("target").get("user")),
            action=json.get("action"),
            amount=parse_amount(json.get("amount")),
            audience=json.get("audience"),
            date_created=string_to_timestamp(json.get("date_created")),
            date_reminded=string_to_timestamp(json.get("date_reminded")),
            date_completed=string_to_timestamp(json.get("date_completed")),
            note=json.get("note"),
            status=PaymentStatus(json.get("status")),
            json=json,
        )


class PaymentStatus(Enum):
    SETTLED = "settled"
    CANCELLED = "cancelled"
    PENDING = "pending"
    FAILED = "failed"
    EXPIRED = "expired"
