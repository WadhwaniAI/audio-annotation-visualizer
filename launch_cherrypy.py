import sys
import cherrypy
from cherrypy.process.plugins import Daemonizer

from main import app

# make the process a daemon
#Daemonizer(cherrypy.engine).subscribe()

# Process port as argument
try:
    port = int(sys.argv[1])
except:
    port = 30100


print('Starting cherrypy on port:', port)
cherrypy.tree.graft(app.wsgi_app, '/')
cherrypy.config.update({
    'global': {'environment': 'production',
               'log.screen': True,
               'log.error_file': 'cherrypy_logs/error.log',
               'log.access_file': 'cherrypy_logs/access.log',
               'server.socket_host': '0.0.0.0',
               'server.socket_port': port,
               'response.stream': True},
})

if __name__ == '__main__':
    cherrypy.engine.start()

