from unittest import TestCase
from unittest.mock import patch

from user.okta_operations import create_okta_user, activate_okta_user


class OktaOperationTest(TestCase):

    def setUp(self) -> None:
        self.payload = {'email': 'test@gmail.com',
                        'first_name': 'fisrt name',
                        'last_name': 'last name',
                        'password': 'testpw'
                        }

    def tearDown(self) -> None:
        self.payload = None

    @patch('user.okta_operations.UsersClient')
    @patch('user.okta_operations.User')
    def test_create_okta_user_success(self, mock_user, mock_user_client):
        """test creating user with valid payload is successful"""
        client_instance = mock_user_client.return_value
        user_instance = mock_user.return_value
        user_instance.id = "OKTAUSERIDHAHAHAHA"
        client_instance.create_user.return_value = user_instance

        okta_test_id = create_okta_user(self.payload)

        self.assertEqual(okta_test_id, "OKTAUSERIDHAHAHAHA")

    @patch('user.okta_operations.UsersClient')
    @patch('user.okta_operations.User')
    def test_create_okta_user_failed(self, mock_user, mock_user_client):
        client_instance = mock_user_client.return_value
        user_instance = mock_user.return_value
        user_instance.id = "OKTAUSERIDHAHAHAHA"
        test_exception = Exception("id is wrong")
        client_instance.create_user.side_effect = test_exception

        with self.assertRaises(Exception): create_okta_user(self.payload)

    @patch('user.okta_operations.UsersClient')
    def test_activate_okta_user_failed(self, mock_user_client):
        client_instance = mock_user_client.return_value
        client_instance.activate_user = None
        with self.assertRaises(Exception): activate_okta_user(1)

    @patch('user.okta_operations.User')
    @patch('user.okta_operations.UsersClient')
    def test_activate_okta_user_success(self, mock_user_client, mock_user):
        okta_user_id = 0
        client_instance = mock_user_client.return_value
        user_instance = mock_user.return_value
        user_instance.id = okta_user_id
        client_instance.activate_user.return_value = user_instance
        self.assertEqual(activate_okta_user(okta_user_id), okta_user_id)
