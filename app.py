from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

MAIL_USERNAME = "balammuu0023@gmail.com"   # your Gmail
MAIL_PASSWORD = "knko rtwx oank wozv"        # replace with real app password

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # TLS


def send_email(to_email, otp):
    try:
        msg = MIMEText(f"Your OTP is: {otp}")
        msg["Subject"] = "Your OTP Code"
        msg["From"] = MAIL_USERNAME
        msg["To"] = to_email

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(MAIL_USERNAME, [to_email], msg.as_string())
        server.quit()

        return True
    except Exception as e:
        print("Error:", e)
        return False


@app.route("/send-otp", methods=["POST"])
def send_otp():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    email = data.get("email")
    otp = data.get("otp")

    if not email or not otp:
        return jsonify({"status": "error", "message": "Email & OTP required"}), 400

    if send_email(email, otp):
        return jsonify({"status": "success", "message": "OTP sent successfully!"})
    else:
        return jsonify({"status": "error", "message": "Failed to send OTP"}), 500


if __name__ == "__main__":
    app.run(debug=True)
