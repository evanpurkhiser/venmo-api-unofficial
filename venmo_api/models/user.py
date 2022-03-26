from venmo_api import string_to_timestamp, BaseModel


class User(BaseModel):
    def __init__(
        self,
        user_id,
        username,
        first_name,
        last_name,
        display_name,
        phone,
        profile_picture_url,
        about,
        date_joined,
        is_group,
        is_active,
        balance,
        json=None,
    ):
        """
        User model
        """
        super().__init__()

        self.id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.display_name = display_name
        self.phone = phone
        self.profile_picture_url = profile_picture_url
        self.about = about
        self.date_joined = date_joined
        self.is_group = is_group
        self.is_active = is_active
        self.balance = balance
        self._json = json

    @classmethod
    def from_json(cls, json, is_profile=False):
        """
        init a new user form JSON
        """
        if not json:
            return

        parser = UserParser(json, is_profile=is_profile)

        date_joined_timestamp = string_to_timestamp(parser.get_date_created())

        return cls(
            user_id=parser.get_user_id(),
            username=parser.get_username(),
            first_name=parser.get_first_name(),
            last_name=parser.get_last_name(),
            display_name=parser.get_full_name(),
            phone=parser.get_phone(),
            profile_picture_url=parser.get_picture_url(),
            about=parser.get_about(),
            date_joined=date_joined_timestamp,
            is_group=parser.get_is_group(),
            is_active=parser.get_is_active(),
            balance=parser.get_balance(),
            json=json,
        )


class UserParser:
    def __init__(self, json, is_profile=False):

        if not json:
            return

        self.json = json
        self.user = json["user"]
        self.is_profile = is_profile

        if is_profile:
            self.parser = profile_json_format
        else:
            self.parser = user_json_format

    def get_user_id(self):
        return self.user.get(self.parser.get("user_id"))

    def get_username(self):
        return self.user.get(self.parser.get("username"))

    def get_first_name(self):
        return self.user.get(self.parser.get("first_name"))

    def get_last_name(self):
        return self.user.get(self.parser.get("last_name"))

    def get_full_name(self):
        return self.user.get(self.parser.get("full_name"))

    def get_phone(self):
        return self.user.get(self.parser.get("phone"))

    def get_picture_url(self):
        return self.user.get(self.parser.get("picture_url"))

    def get_about(self):
        return self.user.get(self.parser.get("about"))

    def get_date_created(self):
        return self.user.get(self.parser.get("date_created"))

    def get_balance(self):
        if self.is_profile:
            return None
        return self.json.get(self.parser.get("balance"))

    def get_is_group(self):
        if self.is_profile:
            return False
        return self.user.get(self.parser.get("is_group"))

    def get_is_active(self):
        if self.is_profile:
            return False
        return self.json.get(self.parser.get("is_active"))


user_json_format = {
    "user_id": "id",
    "username": "username",
    "first_name": "first_name",
    "last_name": "last_name",
    "full_name": "display_name",
    "phone": "phone",
    "picture_url": "profile_picture_url",
    "about": "about",
    "date_created": "date_joined",
    "is_group": "is_group",
    "is_active": "is_active",
    "balance": "balance",
}

profile_json_format = {
    "user_id": "external_id",
    "username": "username",
    "first_name": "firstname",
    "last_name": "lastname",
    "full_name": "name",
    "phone": "phone",
    "picture_url": "picture",
    "about": "about",
    "date_created": "date_created",
    "is_business": "is_business",
    "balance": "balance",
}
