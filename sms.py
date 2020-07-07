from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "ACe6d431ce6512b621ef38fc8a37c50965"
# Your Auth Token from twilio.com/console
auth_token = "5037a7b0635e6292184fddafc004eb40"


def send_message(message_content):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+8613126822017",
        from_="+12058947739",
        body=message_content)


send_message('hello my name is sheldon, this is my sms!')