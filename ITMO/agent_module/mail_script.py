import smtplib
import os
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

def send_email(email, message, file):
    sender = "popset26@gmail.com"
    password = "vlwh zmql rlvo crtg"


    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEMultipart()
        msg["Subject"] = "AI-ДА РЕШЕНИЕ"
        msg.attach(MIMEText(message))

        if file:
            fp = open(file, 'rb')
            att = MIMEApplication(fp.read(), _subtype = 'txt')
            fp.close()
            att.add_header('Content-Disposition','attachment',filename=file)
            
            msg.attach(att)

        
        server.sendmail(sender, email, msg.as_string())


        return "The message was sent successfully!"
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"

    


if __name__ == "__main__":
    print(send_email('popset26@gmail.com',"олдам ку", 'C:\\Users\\Askar\\VS_CODE\\Python\\HACKATON\\ITMO\\аналитика.docx'))
