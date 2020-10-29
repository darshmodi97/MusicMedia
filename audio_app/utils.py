from django.core.mail import EmailMessage


def mail_sending(subject, body, to):
    print("subject:", subject)
    print(body)
    print(to)

    msg = EmailMessage(subject=subject, body= body, to=to)
    msg.send()
    return True
