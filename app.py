import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def send_email():
    try:
        data = request.json
        msg_content = data.get('message')

        sender_email = "abdullahalahadkafi@gmail.com" 
        app_password = "mbce ezjw mkqo czqm" 
        receiver_email = "abdullahalahadkafi@gmail.com"

        html_template = f"""
        <html>
        <body style="font-family: sans-serif; background: #0b0e14; color: #ecf0f1; padding: 20px;">
            <div style="max-width: 600px; margin: auto; border: 1px solid #f39c12; padding: 20px; border-radius: 10px;">
                <h2 style="color: #f39c12;">নোহার বার্তা - রূপকথা ❤️</h2>
                <p style="font-size: 1.1rem; padding: 15px; background: rgba(0,0,0,0.5);">{msg_content}</p>
                <p style="font-size: 0.8rem; color: #7f8c8d;">- এই বার্তাটি আপনার ১৯ জানুয়ারি পেজ থেকে সরাসরি এসেছে।</p>
            </div>
        </body>
        </html>
        """

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        
        email_msg = MIMEMultipart()
        email_msg['Subject'] = "নোহার বার্তা আপনার কাছে সংরক্ষিত..."
        email_msg['From'] = sender_email
        email_msg['To'] = receiver_email
        email_msg.attach(MIMEText(html_template, 'html'))
        
        server.send_message(email_msg)
        server.quit()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(str(e))
        return jsonify({"status": "error"}), 500

if __name__ == "__main__":
    app.run()