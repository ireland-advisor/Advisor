from unittest import TestCase
from unittest.mock import patch

from user.email_verify import send_email


class EmailVerifyTest(TestCase):

    @patch('user.email_verify.Mail')
    @patch('user.email_verify.SendGridAPIClient')
    def test_send_email_success(self, send_grid_client, mail):
        send_grid_client_instance = send_grid_client.return_value
        mail_instance = mail.return_value
        send_grid_client_instance.send(mail_instance).status_code = 202

        self.assertEqual(send_email("test@gmail.com", "1234"), 202)
