# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(email, okta_id):
    message = Mail(
        from_email='leebusiness197@gmail.com',
        to_emails='114220313@umail.ucc.ie',
        subject='Please confirm you email address',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    message.template_id = 'd-6fbcb19bc78341fb903894020db811c7'
    message.dynamic_template_data = {'okta_id': okta_id}
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        raise e
