import pyshorteners
from django.core.mail import EmailMessage


def mail_sending(subject, body, to):
    print("subject:", subject)
    print(body)
    print(to)

    msg = EmailMessage(subject=subject, body=body, to=to)
    msg.send()
    return True


# using dagd... https://pyshorteners.readthedocs.io/en/latest/apis.html#tinyurl-com
def short_url(link):
    shorted_url = pyshorteners.Shortener()
    return shorted_url.dagd.short(link)
