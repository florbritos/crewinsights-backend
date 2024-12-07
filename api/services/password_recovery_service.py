from api.services.users_service import UsersService
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

class PasswordRecoveryService:
    def __init__(self):
        load_dotenv()
        self.users_service = UsersService()

    def sendOTP(self, email, otp):  
        user = self.users_service.getUserByEmail(email)
        if user:
            smtp_server = "smtp.gmail.com"
            smtp_port = 587 
            sender_email = os.getenv("SENDER_EMAIL")
            sender_password = os.getenv("EMAIL_PASSWORD")
            print(sender_email)
            print(sender_password)
            try:
                subject = "CrewInsights - PASSWORD RECOVERY"
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = email
                message["Subject"] = subject

                body = f"""
                <p>Hello,</p>
                <p>Your OTP code is: <strong>{otp}</strong></p>
                """
                message.attach(MIMEText(body, "html"))

                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email, message.as_string())
                server.quit()

                print(f"OTP sent successfully to {email}")
                return {"status": "success", "message": "OTP sent successfully"}
            except Exception as e:
                return {"status": "failed", "message": "Something went wront while trying to send otp to user"}
        else:
            return {"status": "failed", "message": "Validation failed", "errors": {"email": "Email not found"}}
        
    def resetPassword(self, email, password):  
        user = self.users_service.getUserByEmail(email)
        if user:
            try:
                self.users_service.updateUser(user.id_user, {'password': password})
                return {"status": "success", "message": "Password changed successfully"}
            except Exception as e:
                return {"status": "failed", "message": "Something went wront while trying to change the password"}
        else:
            return {"status": "failed", "message": "Validation failed", "errors": {"email": "Email not found"}}