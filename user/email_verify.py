import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(email, okta_id):
    message = Mail(
        from_email='leebusiness197@gmail.com',
        to_emails=email,
        subject='Please confirm you email address',
        html_content='test content')
    message.template_id = 'd-6fbcb19bc78341fb903894020db811c7'
    message.dynamic_template_data = {'okta_id': okta_id}
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        return sg.send(message).status_code
    except Exception as e:
        raise e
