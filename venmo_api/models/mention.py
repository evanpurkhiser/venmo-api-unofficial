from venmo_api import BaseModel, User


class Mention(BaseModel):
    def __init__(self, username, user, json=None):
        """
        Mention model
        """
        super().__init__()

        self.username = username
        self.user = user

        self._json = json

    @classmethod
    def from_json(cls, json):
        """
        Create a new Mention from the given json.
        """

        if not json:
            return

        return cls(
            username=json.get("username"),
            user=User.from_json(json.get("user")),
            json=json,
        )
