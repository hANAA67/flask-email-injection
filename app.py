from flask import Flask, request, render_template
import smtplib
from email.mime.text import MIMEText
import yaml

app = Flask(__name__)

def load_config():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

config = load_config()

def send_email(to_email, subject, body):
    from_email = config["email"]["from_email"]
    smtp_server = config["email"]["smtp_server"]
    smtp_port = config["email"]["smtp_port"]
    smtp_password = config["email"]["smtp_password"]

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_email, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())

@app.route("/", methods=["GET", "POST"])
def invite():
    if request.method == "POST":
        to_email = request.form.get("email")
        custom_message = request.form.get("message")

        email_body = f"""
        <html>
        <body style='font-family: Arial, sans-serif; line-height: 1.6;'>
            <h2 style='color: #333;'>You have been invited to join our platform!</h2>
            <p>Message from your friend:</p>
            <blockquote style='border-left: 4px solid #ccc; margin: 10px 0; padding-left: 10px; color: #555;'>
                {custom_message}
            </blockquote>
            <p><a href='https://google.com' style='color: white; background-color: #007bff; padding: 10px 15px; text-decoration: none; border-radius: 5px;'>Click here to join!</a></p>
            <p style='color: #777;'>If you have any questions, feel free to contact our support team.</p>
        </body>
        </html>
        """

        try:
            send_email(to_email, "You're Invited!", email_body)
            return render_template("invite.html", success=True)
        except Exception as e:
            return render_template("invite.html", success=False, error=str(e))

    return render_template("invite.html", success=None)

if __name__ == "__main__":
    app.run()

