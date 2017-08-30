import os


bind_ip = os.getenv('bind_ip', '0.0.0.0')
bind_port = os.getenv('bind_port', '7010')
bind = '{0}:{1}'.format(bind_ip, bind_port)
capture_output = True
keyfile = None
certfile = None