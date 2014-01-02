#/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
import logging
import tornado.options

class  weixin(tornado.web.RequestHandler):

    def prepare(self):
        logging.info('request:%s'%self.request) 

    def get(self):
        logging.info('arguments:%s'%str(self.get_arguments('echostr')))
        self.finish(self.get_argument('echostr'))

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
