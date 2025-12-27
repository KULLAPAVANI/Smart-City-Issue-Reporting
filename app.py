from flask import Flask, render_template, request
import sqlite3
import uuid
import smtplib
from email.message import EmailMessage

app = Flask(__name__)


def init_db():
    con = sqlite3.connect("issues.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS issues(
            ref_id TEXT,
            city TEXT,
            area TEXT,
            street TEXT,
            issue TEXT,
            email TEXT
        )
    """)
    con.commit()
    con.close()
def send_confirmation(receiver_email, ref_id):
    """
    Email confirmation using SMTP.
    For demo purposes, email sending can be simulated.
    """

    SENDER_EMAIL = "pavanikulla1245@gmail.com"      
    APP_PASSWORD = "uacm hzen rswa zomr"   

    msg = EmailMessage()
    msg["Subject"] = "Smart City Issue Confirmation"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg.set_content(
        f"""
Hello Citizen,

Your infrastructure issue has been submitted successfully.

Reference ID: {ref_id}

Our team will review the issue shortly.

Thank you for helping make the city smarter!

– Smart City Support Team
"""
    )

    try:
        # ---------- REAL EMAIL ----------
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("pavanikulla1245@gmail.com","uacm hzen rswa zomr")
        server.send_message(msg)
        server.quit()
        print("Email sent successfully")

    except Exception as e:
        
        print("Email simulation mode")
        print("Reference ID:", ref_id)
        print("Reason:", e)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ref_id = str(uuid.uuid4())[:8]

        city = request.form["city"]
        area = request.form["area"]
        street = request.form["street"]
        issue = request.form["issue"]
        email = request.form["email"]


        con = sqlite3.connect("issues.db")
        cur = con.cursor()
        cur.execute(
            "INSERT INTO issues VALUES (?,?,?,?,?,?)",
            (ref_id, city, area, street, issue, email)
        )
        con.commit()
        con.close()

        
        send_confirmation(email, ref_id)

        return render_template("success.html", ref=ref_id)

    return render_template("index.html")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=10000)


