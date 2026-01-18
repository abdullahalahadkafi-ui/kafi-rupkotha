import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)

# হোম রুট: ইনডেক্স পেজটি দেখাবে
@app.route('/')
def home():
    return render_template('index.html')

# ইমেইল পাঠানোর রুট
@app.route('/send-message', methods=['POST'])
def send_email():
    try:
        data = request.json
        msg_content = data.get('message')

        # আপনার ইমেইল তথ্য (যেখানে আপনি সেভ করেছেন)
        sender_email = "abdullahalahadkafi@gmail.com" 
        app_password = "mbce ezjw mkqo czqm" # আপনার দেওয়া অ্যাপ পাসওয়ার্ড
        receiver_email = "abdullahalahadkafi@gmail.com"

        # এইচটিএমএল ইমেইল টেমপ্লেট
        html_template = f"""
        <html>
        <body style="font-family: 'Hind Siliguri', sans-serif; background: #0b0e14; color: #ecf0f1; padding: 20px;">
            <div style="max-width: 600px; margin: auto; border: 1px solid #f39c12; padding: 20px; border-radius: 10px;">
                <h2 style="color: #f39c12;">কলিজার বার্তা - ১৯ জানুয়ারি ❤️</h2>
                <p style="font-size: 1.1rem; border: 1px dashed #f39c12; padding: 15px; background: rgba(0,0,0,0.5);">
                    {msg_content}
                </p>
                <p style="font-size: 0.8rem; color: #7f8c8d;">- এই বার্তাটি আপনার ১ মাসের স্মৃতি পেজ থেকে সরাসরি এসেছে।</p>
            </div>
        </body>
        </html>
        """

        # SMTP কনফিগারেশন
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, app_password)
        
        email_msg = MIMEMultipart()
        email_msg['Subject'] = "নোহার একটি বার্তা সংরক্ষিত হয়েছে..."
        email_msg['From'] = sender_email
        email_msg['To'] = receiver_email
        email_msg.attach(MIMEText(html_template, 'html'))
        
        server.send_message(email_msg)
        server.quit()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000)) # পোর্ট খুঁজে নেওয়ার জন্য
    app.run(host='0.0.0.0', port=port) # হোস্ট ০.০.০.০ রাখা বাধ্যতামূলক