#发送带附件的邮件
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart,MIMEBase
from email import encoders
import smtplib

from_addr='18810940231@163.com'#输入email的地址
password='oppo7226' #输入口令(注意不是你的登陆密码，而是授权码）
to_addr='826580369@qq.com'#输入收件人地址
smtp_server= 'smtp.163.com'##输入SMTP服务器地址，如是163邮箱为smtp.163.com

msg=MIMEMultipart()  #构造MIMEMultipart对象作为邮件本身，包含邮件正文+附件
msg.attach(MIMEText('hello','plain','utf-8')) #添加MIMEText作为邮件正文
#构造附件（附件可有多个）
with open('picture.jpg','rb') as f: #with as 的用法对文件读取出错会进行处理。附件是本地的一张图片,写明保存的路径（因为程序与图片在同一目录，所以可以只写图片名）
    mime=MIMEBase('image','jpg',filename='picture.jpg') #设置附件中的MIME
    mime.add_header('Content-Disposition', 'attachment', filename='picture.jpg')    #MIME头中的Content-Disposition字段。指明是一个附件
    mime.set_payload(f.read())#把附件内容读进来
    encoders.encode_base64(mime) #采用Base64编码，因为图片是二进制数据，使用此编码方式可将二进制文本安全的发送
    msg.attach(mime) #添加附件到邮件中

#邮件头
msg['From'] =from_addr   #发件人显示
msg['To'] =to_addr    #收件人显示，但收件人的名字可能会替换为用户注册的名字
msg['Subject'] =Header('来自SMTP的问候2','utf-8')  #邮件的主题

#发送邮件
server=smtplib.SMTP(smtp_server,25) #SMTP协议的默认端口是25
server.set_debuglevel(1)  #打印出所有SMTP服务器交互的信息
server.login(from_addr,password) #登陆SMTP服务器
server.sendmail(from_addr,[to_addr],msg.as_string()) #发邮件。收件人可以为多个，所以是一个list，as_string把MIMEText对象变为str
server.quit()#关闭连接

