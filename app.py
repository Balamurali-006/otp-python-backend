from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

EMAIL = "balammuu0023@gmail.com"
APP_PASSWORD = "your_16_digit_app_password"  # replace with Gmail app password

@app.post("/send-otp")
def send_otp():
    data = request.get_json()
    email = data["email"]
    otp = data["otp"]

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = email
    msg["Subject"] = "Your OTP Code"
    msg.attach(MIMEText(f"<h1>Your OTP is: {otp}</h1>", "html"))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL, APP_PASSWORD)
        server.sendmail(EMAIL, email, msg.as_string())
        server.quit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
