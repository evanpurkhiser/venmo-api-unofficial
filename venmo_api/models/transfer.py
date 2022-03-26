from typing import Dict
from venmo_api import (
    BaseModel,
)
from enum import Enum


class TransferOptions(BaseModel):
    def __init__(self, preferred_transfer_type, transfer_targets, json=None):
        """
        Represents available transfer options for instant and standard transfers
        """
        super().__init__()

        self.preferred_transfer_type = preferred_transfer_type
        self.transfer_targets = transfer_targets
        self._json = json

    @classmethod
    def from_json(cls, json: Dict):
        return cls(
            preferred_transfer_type=TransferType(
                json.get("preferred_transfer_type", {}).get("out")
            ),
            transfer_targets=[
                TransferTarget.from_json(target)
                for target in json.get("standard", {}).get("eligible_destinations", [])
            ],
        )


class TransferTarget(BaseModel):
    def __init__(
        self, id, name, asset_name, type, last_four, is_default, transfer_to_estimate, json=None
    ):
        self.id = id
        self.name = name
        self.asset_name = asset_name
        self.type = type
        self.last_four = last_four
        self.is_default = is_default
        self.transfer_to_estimate = transfer_to_estimate
        self._json = json

    @classmethod
    def from_json(cls, json: Dict):
        return cls(
            id=json.get("id"),
            name=json.get("name"),
            asset_name=json.get("asset_name"),
            type=json.get("type"),
            last_four=json.get("last_four"),
            is_default=json.get("is_default"),
            transfer_to_estimate=json.get("transfer_to_estimate"),
            json=json,
        )


class TransferType(Enum):
    STANDARD = "standard"
    INSTANT = "instant"
