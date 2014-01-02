#/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
import logging
from BeautifulSoup import BeautifulSoup
import time

text_tmp = """
<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    <FuncFlag>0</FuncFlag>
</xml> 
            """

class  weixin(tornado.web.RequestHandler):

    def prepare(self):
        if self.request.method == 'POST':
            print '\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            print 'body:',self.request.body
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            soup = BeautifulSoup(self.request.body)
            self.userid  = soup.find('fromusername').text
            self.createtime = soup.find('createtime').text
            self.msgtype = soup.find('msgtype').text
            self.myid = soup.find('ToUserName').text
            if self.msgtype == 'text':
                self.wxtext = soup.find('content').text
                print 'text:',self.wxtext  
            elif self.msgtype == 'location':
                self.location_x = soup.find('Location_X').text 
                self.location_y = soup.find('Location_Y').text 
                self.location_scale = soup.find('Scale').text 
                self.location_lable = soup.find('Label').text 
                print 'x:',self.location_x  
                print 'y:',self.location_y
            elif self.msgtype == 'image':
                self.picurl = soup.find('PicUrl').text 
                print 'pic url:',self.picurl 
        else:
            logging.info('request:%s'%self.request) 

    def get(self):
        logging.info('arguments:%s'%str(self.get_arguments('echostr','')))
        self.finish(self.get_argument('echostr',''))

    def post(self):
        if self.msgtype == 'text':
            pass
        elif self.msgtype == 'location':
            pass
        elif self.msgtype == 'image':
            pass
        self.send_text('我收到你消息啦!!')

    def send_text(self,msg):
        #self.set_header("Content-Type","application/xml; charset=UTF-8")
        line = text_tmp%(self.userid,self.myid,int(time.time()),msg) 
        self.finish(line)
            
class Application(tornado.web.Application):
    def __init__(self):
        app_settings={
            'debug':True,
        }
        handlers = [
            (r'/',weixin),
        ]
        tornado.web.Application.__init__(self,handlers,**app_settings)

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(request_callback=Application())
    http_server.listen(7070)
    tornado.ioloop.IOLoop.instance().start()
