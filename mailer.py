import smtplib
from email.message import EmailMessage
import logging
import json

class Mailer:
    def __init__(self, config):
        email_config = config.get("email", {})
        self.smtp_server = email_config.get("smtp_server", "smtp.gmail.com")
        self.smtp_port = email_config.get("smtp_port", 587)
        self.smtp_user = email_config.get("smtp_user", "")
        self.smtp_password = email_config.get("smtp_password", "")
        self.sender_email = email_config.get("sender_email", "noreply@example.com")
        self.simulate_email = email_config.get("simulate_email", True)

    def send_notification(self, recipient_email, zip_code, state):
        if not recipient_email or "@" not in str(recipient_email):
            logging.warning(f"Invalid email: {recipient_email}")
            return False

        subject = f"Your Zip Code {zip_code} matches {state}"
        body = f"""
        Hello,
        
        You provided the zip code {zip_code}. According to our records, this corresponds to {state}.
        
        Thank you!
        """

        if self.simulate_email:
            logging.info(f"[SIMULATED EMAIL] To: {recipient_email} | Subject: {subject} | Body: {body.strip()}")
            return True

        try:
            msg = EmailMessage()
            msg.set_content(body)
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = recipient_email

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()
            logging.info(f"Email sent successfully to {recipient_email}")
            return True
        except Exception as e:
            logging.error(f"Failed to send email to {recipient_email}: {e}")
            return False
