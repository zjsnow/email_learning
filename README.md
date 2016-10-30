# 电子邮件发送与接收程序

## 一、基本过程的理解

- 发件人邮箱：me@163.com

- 收件人邮箱：friend@qq.com   （**注意是虚构，测试代码时需用真实的邮箱**）

- 电子邮件的发送接收过程：用Outlook或者Foxmail之类的软件写好邮件，填上对方的Email地址，点“发送”，电子邮件就发出去了。这些电子邮件软件被称为MUA：Mail User Agent——邮件用户代理。

  Email从MUA发出去，不是直接到达对方电脑，而是发到MTA：Mail Transfer Agent——邮件传输代理，就是那些Email服务提供商，比如网易、腾讯等等。由于我们自己的电子邮件是163.com，所以，Email首先被投递到网易提供的MTA，再由网易的MTA发到对方服务商，也就是腾讯的MTA。这个过程中间可能还会经过别的MTA。

  Email到达腾讯的MTA后，由于对方使用的是@qq.com的邮箱，因此，腾讯的MTA会把Email投递到邮件的最终目的地MDA：Mail Delivery Agent——邮件投递代理。Email到达MDA后，就静静地躺在腾讯的某个服务器上，存放在某个文件或特殊的数据库里，我们将这个长期保存邮件的地方称之为电子邮箱。

  Email不会直接到达对方的电脑，因为对方电脑不一定开机，开机也不一定联网。对方要取到邮件，必须通过MUA从MDA上把邮件取到自己的电脑上。

- 编写程序来发送和接受邮件的本质：

  1. 编写MUA把邮件发到MTA
  2. 编写MUA从MDA上收邮件

  发邮件时，MUA和MTA使用的协议就是SMTP：Simple Mail Transfer Protocol，后面的MTA到另一个MTA也是用SMTP协议。

  收邮件时，MUA和MDA使用的协议有两种：POP：Post Office Protocol，目前版本是3，俗称POP3

  IMAP：Internet Message Access Protocol，目前版本是4，优点是不但能取邮件，还可以直接操作MDA上存储的邮件，比如从收件箱移到垃圾箱，等等。

  邮件客户端软件在发邮件时，会让你先配置SMTP服务器，也就是你要发到哪个MTA上。假设你正在使用163的邮箱，你就不能直接发到新浪的MTA上，因为它只服务新浪的用户，所以，你得填163提供的SMTP服务器地址：smtp.163.com，为了证明你是163的用户，SMTP服务器还要求你填写邮箱地址和邮箱口令，这样，MUA才能正常地把Email通过SMTP协议发送到MTA。

  类似的，从MDA收邮件时，MDA服务器也要求验证你的邮箱口令，确保不会有人冒充你收取你的邮件，所以，Outlook之类的邮件客户端会要求你填写POP3或IMAP服务器地址、邮箱地址和口令，这样，MUA才能顺利地通过POP或IMAP协议从MDA取到邮件。

  **(目前大多数邮件服务商都需要手动打开SMTP发信和POP收信的功能，否则只允许在网页登录，所以在编写程序前要保证所用邮箱的SMTP发信和POP收信的功能已打开）**

## 二、SMTP发送邮件

**smtp.py**:发送纯文本邮件程序

**smtp_pluse.py**:发送文本加附件的程序

主要利用email模块构造邮件，smtplib模块发送文件

Python的smtplib发送邮件十分简单，只要掌握了各种邮件类型的构造方法，正确设置好邮件头，就可以顺利发出。构造一个邮件对象就是一个Messag对象，如果构造一个MIMEText对象，就表示一个文本邮件对象，如果构造一个MIMEImage对象，就表示一个作为附件的图片，要把多个对象组合起来，就用MIMEMultipart对象，而MIMEBase可以表示任何对象。它们的继承关系如下：

    Message
    +- MIMEBase
       +- MIMEMultipart
       +- MIMENonMultipart
         +- MIMEMessage
         +- MIMEText
         +- MIMEImage
**注意**：使用标准的25端口连接SMTP服务器时，使用的是明文传输，发送邮件的整个过程可能会被窃听。要更安全地发送邮件，可以加密SMTP会话，实际上就是先创建SSL安全连接，然后再使用SMTP协议发送邮件。只需修改一行代码：

将

    server = smtplib.SMTP(smtp_server, 25)
改为

    server=smtplib.SMTP_SSL(smtp_server,465)
下面是163邮箱的SSL协议端口号：

![SSL是什么？如何使用？](http://img3.cache.netease.com/help/2011/2/1/20110201092607e93ce.jpg)

## 三、POP3收取邮件

未完待续....







参考资料：

1.廖雪峰官方网站

http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000













