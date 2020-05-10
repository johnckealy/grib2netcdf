import os




# assumes we're in production if not on my lenovo laptop
if os.uname().nodename == 'leno':
    from .development import *
else:
    from .production import *
