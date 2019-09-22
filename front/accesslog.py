# from datetime import datetime
# from time import clock
#
# from flask import request, g
#
# from front import app
# from front.models.rest_accesslog import RestAccesslog, session
#
#
# @app.before_request
# def before_request():
#     request.start = clock()
#
#     if request.endpoint:
#         endpoint = request.endpoint
#         view_name = str(endpoint)
#         view_description = app.view_functions[endpoint].__doc__
#     else:
#         view_description = ''
#
#     accesslog = RestAccesslog(
#         remote_addr=request.remote_addr,
#         tm=datetime.now(),
#         method=request.method,
#         url=request.url,
#         description=view_description
#     )
#
#     if request.url.find("/static/") == -1 and request.url.find("/schedule/run") == -1:
#         session.add(accesslog)
#         session.commit()
#
#     g.accesslog = accesslog
#
#
# @app.after_request
# def after_request(response):
#     request.finish = clock()
#
#     accesslog = g.accesslog
#
#     accesslog.duration = 1000 * (request.finish - request.start)
#     accesslog.status = response.status_code
#
#     if response.content_length:
#         accesslog.length = response.content_length
#     else:
#         accesslog.length = len(response.data)
#
#     if hasattr(g, 'user'):
#         accesslog.name = g.user.staff_name
#
#     if response.status_code >= 400 and response.status_code <= 500:
#         accesslog.error_message = response.data[:255]
#         app.logger.info("%s@%s %4d ms %6s bytes %s %s %s %s" % (
#             accesslog.name,
#             accesslog.remote_addr,
#             accesslog.duration,
#             accesslog.length,
#             accesslog.status,
#             accesslog.method,
#             accesslog.url,
#             response.data))
#
#     if request.url.find("/static/") == -1 and request.url.find("/schedule/run") == -1:
#         session.commit()
#
#     if request.url.find("/schedule/run") == -1:
#         app.logger.info("%s@%s %4d ms %6s bytes %s %s %s" % (
#             accesslog.name,
#             accesslog.remote_addr,
#             accesslog.duration,
#             accesslog.length,
#             accesslog.status,
#             accesslog.method,
#             accesslog.url))
#
#     if request.url.find("/static/") >= 0:
#         response.headers['Access-Control-Allow-Origin'] = '*'
#
#     return response
