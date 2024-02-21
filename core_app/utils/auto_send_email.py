import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

mail_host = "smtp.gmail.com"  # 设置服务器
mail_user = "MetaRomiOneee"  # 用户名
mail_pass = "wvqlwjlypt"  # 口令


def send_email(incident_info, receiver):
    sender = ''
    message = MIMEMultipart("alternative")
    message['From'] = Header("ASE Group-9", 'utf-8')
    message['To'] = ', '.join(receiver)
    part = MIMEText('Urban disaster occurs：' + incident_info, 'plain', 'utf-8')
    message.attach(part)

    subject = 'Urban Disaster Occurs'
    message['Subject'] = Header(subject, 'utf-8')

    server = smtplib.SMTP_SSL(mail_host, 465)
    server.login(mail_user, mail_pass)
    server.sendmail(sender, receiver, message.as_string())
    server.quit()
    print("Send success")


if __name__ == '__main__':
    code = "76983"
    receiver = ''
    send_email(code, receiver)
