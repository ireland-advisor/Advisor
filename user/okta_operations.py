from okta import UsersClient
from okta.models.user import User

from core.models import Config

config = Config()


def create_okta_user(data):
    users_client = UsersClient(config.org_url, config.token)
    okta_user = User(login=data['email'],
                     email=data['email'],
                     firstName=data['first_name'],
                     lastName=data['last_name'],
                     password=data['password'])
    try:
        return users_client.create_user(okta_user, activate=False).id
    except Exception as e:
        raise e


def activate_okta_user(user_id):
    users_client = UsersClient(config.org_url, config.token)
    try:
        users_client.activate_user(user_id)
        return user_id
    except Exception as e:
        raise e
