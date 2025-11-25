from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    allow_headers=["Content-Type"],
    methods=["POST", "OPTIONS"],
)

# Your Resend API Key
RESEND_API_KEY = "re_SMzZvDtm_BVEK3LfzQNScssWpacu88bqc"


def send_email(to_email, otp):
    try:
        url = "https://api.resend.com/emails"

        payload = {
            "from": "OTP Service <onboarding@resend.dev>",
            "to": [to_email],
            "subject": "Your OTP Code",
            "html": f"<h2>Your OTP is: <strong>{otp}</strong></h2>",
        }

        headers = {
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.post(url, json=payload, headers=headers)
        print("Resend Response:", response.text)

        return response.status_code == 200
    except Exception as e:
        print("Error:", e)
        return False


@app.route("/send-otp", methods=["POST", "OPTIONS"])
def send_otp():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

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


@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "running", "message": "OTP Backend Live"})


# Railway uses dynamic port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
