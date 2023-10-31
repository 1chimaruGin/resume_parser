import requests
from typing import List

API_KEY = "4bfcdebc53614ce80abd810201d3f4cd-77316142-3f919939"
DOMAIN = "sorci.ai"
MAILGUN_API_URL = f"https://api.eu.mailgun.net/v3/{DOMAIN}/messages"


def send_email(email_from: str, email_to: List[str], subject: str, message: str):
    try:
        response = requests.post(
            MAILGUN_API_URL,
            auth=("api", API_KEY),
            data={
                "from": email_from,
                "to": email_to,
                "subject": subject,
                "text": message,
            },
        )
        if response.status_code == 200:
            print("Email sent successfully")
            return True
        print(response.status_code)

    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    email_to = ["umairkaramat48@gmail.com", "kyitharhein18@gmail.com"]
    email_from = "theirname@sorci.ai"
    subject = "Test Email"
    message = (
        "Hello World, testing mailgun email. Pleae check it out. With love, Sorci.ai"
    )
    send_email(email_from, email_to, subject, message)


# curl -s --user 'api:4bfcdebc53614ce80abd810201d3f4cd-77316142-3f919939' \
#     https://api.mailgun.net/v3/sorci.ai/messages \
#     -F from=mailgun@sorci.ai \
#     -F to=kyitharhein18@gmail.com \
#     -F to=hello@sorci.ai \
#     -F subject='Hello' \
#     -F text='Testing some Mailgun awesomeness!'
