from app import app
import sys
from intercepts.controllers import intercepts
from extract.views import extract
from transform.views import transform
from load.views import load

app.register_blueprint(extract, url_prefix='/extract')
app.register_blueprint(transform, url_prefix='/transform')
app.register_blueprint(load, url_prefix='/load')
app.register_blueprint(intercepts, url_prefix='/intercepts')

# Sets the port, or defaults to 80
if (len(sys.argv) > 1):
    port = int(sys.argv[1])
else:
    port=80

app.run(debug=True, host='0.0.0.0', port=port)
