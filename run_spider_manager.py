import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from app import app
app.debug = True
app.run(host="0.0.0.0")
