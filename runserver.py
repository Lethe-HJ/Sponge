from os import environ
from front.api import app

if __name__ == '__main__':
    # gevent异步WEB服务---------------------------------------------------
    from gevent import monkey, pywsgi
    monkey.patch_all()
    app.debug = True
    gevent_server = pywsgi.WSGIServer(('0.0.0.0', app.config["PORT"]), app)
    gevent_server.serve_forever()


    


