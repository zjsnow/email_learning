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

**smtp_pluse.py**:发送文本加附件的邮件程序

发送邮件分两步：

1. 用email构造邮件
2. 用smtplib发送邮件

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

**pop.py**:获取最新的6封邮件并解析输出

POP3协议收取的不是一个已经可以阅读的邮件本身，而是邮件的原始文本，这和SMTP协议很像，SMTP发送的也是经过编码后的一大段文本。要把POP3收取的文本变成可以阅读的邮件，还需要用email模块提供的各种类来解析原始文本，变成可阅读的邮件对象。

收取邮件分两步：

1. 用poplib把邮件的原始文本下载到本地
2. 用email解析原始文本，还原为邮件对象

用poplib获取邮件其实很简单,难点在于把邮件的原始内容解析为可以阅读的邮件对象。

我们可以先把邮件内容解析为Message对象，但这个Message对象本身可能是一个MIMEMultipart对象，即嵌套了其他MIMEBase对象，嵌套可能还不止一层，可以采用递归的方法，依次解析。

## 四、对于邮件结构的理解

在pop.py程序中，通过print(msg_content)可观察到邮件的原始文本，下面我对邮件的结构和重要字段进行解释

-  邮件包括邮件头和邮件体，由空行隔开。邮件头以“字段名：字段值”的格式出现，一些主要的邮件头字段：

  1. Received:基本格式为Received from A by B for C,其中A为发送方的域名，B为接收方的域名，C为收件人的邮箱地址。通常会有多个Received表明邮件经过的传输路径，但注意是要从下往上的顺序。
  2. From:制定发件人地址
  3. To:指定收件人地址
  4. Subject:指定邮件的主题，如果主题内容中包含有ASCII码以外的字符，通常要对其内容进行编码。
  5. Date:邮件发送的地址
  6. cc:邮件抄送的地址
  7. bcc:邮件的暗送地址

-  对于一封MIME邮件，它在RFC822文档中对邮件的头字段进行了扩展：

  1. MIME-Version:MIME协议的版本

  2. Content-Type:邮件体的MIME类型。有“主类型/子类型”构成，主类型有text,image,audio,video,application,multipart,message等，每个主类型都有多个子类型，比如test类型包含plain,html,xml,css等子类型，各个类型所带的参数如下

     ```
     主类型        参数       含义
     text         charset   编码方式
     image         name     图片文件名
     application   name     应用程序的文件名
     mltipart     boundary  MIME消息间的分隔符
     ```

- 邮件体的类型由邮件头的Content-Type定义，当出现的类型是multipart时，邮件体会被分成多段，每段会包含段头和段体两部分，也由空行隔开。常见的multipart类型有三种：multipart/mixed, multipart/related和multipart/alternative，如果在邮件中要添加附件，必须定义multipart/mixed段；如果存在内嵌资源，至少要定义multipart/related段；如果纯文本与超文本共存，至少要定义multipart/alternative段。每个段都有自己的属性，由段头的字段来说明，主要包括：

  1. Content-Type：段体的类型，注意与邮件头的类型区别开，这里是指该段的类型，而前面是整个邮件体的类型。
  2. Content-Transfer-Encoding ：段体的邮件编码方式，通常是base64。
  3. Content-Disposition：用于指定邮件阅读程序处理数据内容的方式，有inline 和attachment 两种标准方式，inline 表示直接处理，而attachment 表示当做附件处理。如果将Content-Disposition 设置attachment，在其后还可以指定filename 属性。

  ​










参考资料：

1.廖雪峰官方网站

http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000

2  MIME协议分析  http://blog.csdn.net/bripengandre/article/details/2192982











