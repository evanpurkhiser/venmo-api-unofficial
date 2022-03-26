from venmo_api import string_to_timestamp, BaseModel, User, Mention


class Comment(BaseModel):
    def __init__(self, id, message, date_created, mentions, user, json=None):
        """
        Comment model
        """
        super().__init__()

        self.id = id
        self.message = message
        self.user = user

        self.date_created = date_created

        self.mentions = mentions
        self._json = json

    @classmethod
    def from_json(cls, json):
        """
        Create a new Comment from the given json.
        """

        if not json:
            return

        mentions = json.get("mentions", {}).get("data")
        mentions = [Mention.from_json(mention) for mention in mentions] if mentions else []

        return cls(
            id=json.get("id"),
            message=json.get("message"),
            date_created=string_to_timestamp(json.get("date_created")),
            user=User.from_json(json.get("user")),
            mentions=mentions,
            json=json,
        )
