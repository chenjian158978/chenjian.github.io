# -*- coding:utf8 -*-

"""
@author: chenjian158978@gmail.com

@date: Thu, Aug 10 2017

@time: 10:05:18 GMT+8
"""
from ftplib import FTP


def ftpconnect(host, username, password, port=21):
    """ ftp链接

    :param host: ftp HOST
    :param username: ftp 用户名
    :param password: ftp 密码
    :param port: ftp 端口
    :return: ftp实例
    """
    try:
        ftp_obj = FTP()
        ftp_obj.set_debuglevel(2)
        ftp_obj.connect(host, port)
        ftp_obj.login(username, password)

        # 打印欢迎语
        print 'getwelcome:', ftp_obj.getwelcome()

        # 进入目录'/1111/'
        # ftp_obj.cwd('/1111/')

        # 打印当前目录内的文件
        for i, file_name in enumerate(ftp_obj.nlst()):
            print 'file_name_%s' % str(i), file_name

        # 打印当前的路径
        print 'current_path:', ftp_obj.pwd()

        # 新建远程目录
        ftp_obj.mkd('/new_mkdir_file')

        # 删除远程目录
        ftp_obj.rmd('/new_mkdir_file')

        # 删除远程文件
        # ftp_obj.delete('/dddd.txt')

        return ftp_obj
    except Exception as e:
        print str(e)


def downloadfile(ftp_obj, remotepath, localpath):
    """ 下载文件

    :param ftp_obj: ftp实例
    :param remotepath: 远程路径
    :param localpath: 本地路径
    :return:
    """
    try:
        # 设置的缓冲区大小
        bufsize = 1024
        fp = open(localpath, 'wb')
        ftp_obj.retrbinary('RETR ' + remotepath, fp.write, bufsize)
        ftp_obj.set_debuglevel(0)
    except Exception as e:
        print str(e)
    finally:
        fp.close()


def uploadfile(ftp_obj, remotepath, localpath):
    """ 上传文件

    :param ftp_obj: ftp实例
    :param remotepath: 远程路径
    :param localpath: 本地路径
    :return:
    """
    try:
        bufsize = 1024
        fp = open(localpath, 'rb')
        ftp_obj.storbinary('STOR ' + remotepath, fp, bufsize)
        ftp_obj.set_debuglevel(0)
    except Exception as e:
        print str(e)
    finally:
        fp.close()

if __name__ == '__main__':
    ftp = ftpconnect(host="192.168.1.179", username="chenjian", password="chenjian")
    downloadfile(ftp_obj=ftp, remotepath='dddd.jpg', localpath='/Users/jianchan/Documents/dddd1.jpg')
    uploadfile(ftp_obj=ftp, remotepath='/eeee1.jpg', localpath='/Users/jianchan/Documents/eeee.jpg')

    # FTP.quit():发送QUIT命令给服务器并关闭掉连接。
    # 这是一个比较“缓和”的关闭连接方式，但是如果服务器对QUIT命令返回错误时，会抛出异常
    # FTP.close()：单方面的关闭掉连接，不应该用在已经关闭的连接之后，例如不应用在FTP.quit()之后。
    ftp.quit()
