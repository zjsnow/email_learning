#发送纯文本的邮件
from email.header import Header
from email.mime.text import MIMEText
import smtplib

from_addr='me@163.com'#输入email的地址
password='*******' #输入口令(注意不是你的登陆密码，而是授权码）
to_addr='friend@qq.com'#输入收件人地址
smtp_server= 'smtp.163.com'##输入SMTP服务器地址，如是163邮箱为smtp.163.com

msg=MIMEText('hello','plain','utf-8') #邮件正文。第一个参数为邮件内容，第二个参数是邮件的类型纯文本，采用utf-8编码

#邮件头
msg['From'] =from_addr   #发件人显示
msg['To'] =to_addr    #收件人显示，但收件人的名字可能会替换为用户注册的名字
msg['Subject'] =Header('来自SMTP的问候1','utf-8')  #邮件的主题

#发邮件
server=smtplib.SMTP(smtp_server,25) #SMTP协议的默认端口是25
server.set_debuglevel(1)  #打印出所有SMTP服务器交互的信息
server.login(from_addr,password) #登陆SMTP服务器
server.sendmail(from_addr,[to_addr],msg.as_string()) #发邮件。收件人可以为多个，所以是一个list，as_string把MIMEText对象变为str
server.quit()#关闭连接

