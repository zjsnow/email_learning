from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import poplib

def guess_charset(msg):
    charset = msg.get_charset() #从msg获取编码
    if charset is None:
        content_type = msg.get('Content-Type').lower() #获取不到，从Content-Type字段获取
        pos = content_type.find('charset=') #Content-Type字段中的charset=字段指明了编码方式
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def print_info(msg):
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('part %s' % n)
            print_info(part)  # 递归
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg) #检测文本的编码
            if charset:
                content = content.decode(charset)
            print('Text:%s' % content)
        else:
            print("Attachment:%s" % content_type) #是文本的作为附件处理，打印出附件的类型

#输入邮件地址，口令和POP3服务地址
email='friend@qq.com'
password='****************' #qq邮箱的16位授权码
pop3_server='pop.qq.com'

server=poplib.POP3_SSL(pop3_server,995)#链接到POP3服务器
#server.set_debuglevel(1) #打开调试信息

#身份认证
server.user(email)
server.pass_(password)

print('Messages:%s Size:%s\n'% server.stat()) #stat()返回是一个列表，第一项是邮件数，第二项是占用字节数
resp,mails,octets=server.list() #list()返回所有邮箱的编号mails和大小octcts,resp是状态信息

#获取最新的6封邮件
index=len(mails)
for i in range(index-5,index+1):
    resp,lines,octets=server.retr(i) #retr()获取邮件文本，lines存储了邮件原始文本的每一行
    msg_content=b'\r\n'.join(lines).decode('utf-8')
    #print(msg_content) #输出邮件原始的文本
    # 把邮件内容解析为Message对象
    msg = Parser().parsestr(msg_content)
    # 解码邮件头
    From = parseaddr(msg.get('From'))[1]
    To = parseaddr(msg.get('To'))[1]
    value, charset = decode_header(msg.get('Subject'))[0]  # 由于decode_header(msg.get('Subject'))返回的是一个list形式，但我们只需要list中的第一个tuple元素，该tuple元素包含的第一个元素是subject的值，第二个元素是它的编码
    Subject = value.decode(charset) #得到的value需要解码才能供用户阅读
    print("From:%s\nTo:%s\nSubject:%s\n" % (From, To, Subject))
    #解析邮件正文及附件
    print_info(msg)
    print('\n################################\n')

server.quit()  # 关闭连接




