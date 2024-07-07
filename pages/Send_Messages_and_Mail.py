import streamlit as st
from twilio.rest import Client
import smtplib
import os

st.set_page_config(page_title="Send Messages and Mail")

recipient = st.text_input("Enter Recipient Number or Email Id: ")


def send_mail(receiver_email, subject, message):
    try:
        # Create an SMTP connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Start TLS encryption
        server.login(sender_email, sender_password)

        # Compose the email
        email_body = f'Subject: {subject}\n\n{message}'

        # Send the email
        server.sendmail(sender_email, receiver_email, email_body)

        # Close the SMTP server
        server.quit()

        return 'Email sent successfully'
    except Exception as e:
        print(f'Email could not be sent. Error: {str(e)}')


if recipient and '@' in recipient:
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  
    sender_email = os.environ['EMAIL']
    sender_password = os.environ['EMAIL_APP_PASSWORD']

    recipient_email = recipient
    subject = st.text_input('Subtect')
    message = st.text_area('Message')

    clicked = st.button("Send")
    if clicked:
        feedback = send_mail(recipient_email, subject, message)
        st.write(feedback)

elif recipient:
    # Find your Account SID and Auth Token at 👉 https://www.twilio.com/console
    # Set environment variables. 👉 https://www.twilio.com/blog/how-to-set-environment-variables-html
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)


    phone_number = int(recipient)
    from_number = int(st.text_input("Enter Senders Number:"))
    message_body = st.text_area('Enter Message: ')

    # Sending messaging
    try:
        message = client.messages\
            .create(
                body=message_body,
                from_ =  from_number,
                to = phone_number
            )
        print(f"Message sent Successfully message id {message.sid}!")
        
    except Exception as e:
        print(f'SMS could not be sent. Error: {str(e)}')



