import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app) # নোহা অন্য ডোমেইন থেকে মেসেজ দিলেও যেন আসে

@app.route('/send-message', methods=['POST'])
def send_email():
    data = request.json
    msg_content = data.get('message')

    # ইমেইল কনফিগারেশন
    sender_email = "abdullahalahadkafi@gmail.com" # আপনার জিমেইল
    app_password = "mbce ezjw mkqo czqm" # গুগল থেকে নেওয়া App Password
    receiver_email = "abdullahalahadkafi@gmail.com"

    # ইমেইল টেমপ্লেট ডিজাইন (এখান থেকেই টেমপ্লেট আকারে যাবে)
    html_template = f"""
    <html>
    <body style="font-family: 'Hind Siliguri', sans-serif; background: #0b0e14; padding: 20px; color: #ecf0f1;">
        <div style="max-width: 600px; margin: auto; background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border-left: 5px solid #f39c12;">
            <h2 style="color: #f39c12;">নতুন রূপকথা এসেছে ❤️</h2>
            <p style="font-size: 1.1rem; line-height: 1.6;">কাফি ভাই,</p>
            <p style="font-style: italic;">"আপনার কলিজার কাছ থেকে একটি বিশেষ বার্তা নিচের পাতায় সংরক্ষিত আছে:"</p>
            <hr style="opacity: 0.1;">
            <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; border: 1px dashed #f39c12;">
                <p style="color: #fff; font-size: 1.2rem;">{msg_content}</p>
            </div>
            <p style="margin-top: 30px; font-size: 0.8rem; opacity: 0.6;">এটি ১৯ জানুয়ারি পূর্তি উপলক্ষ্যে তৈরি কোড থেকে সরাসরি আপনার ইনবক্সে এল।</p>
        </div>
    </body>
    </html>
    """

    try:
        # SMTP সেটআপ
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, app_password)
        
        email_msg = MIMEMultipart()
        email_msg['Subject'] = f"কলিজার বার্তা - রূপকথা {msg_content[:20]}..."
        email_msg['From'] = sender_email
        email_msg['To'] = receiver_email
        email_msg.attach(MIMEText(html_template, 'html'))
        
        server.send_message(email_msg)
        server.quit()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(e)
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    app.run(debug=True)