from app import app
import sys
from intercepts.controllers import intercepts

app.register_blueprint(intercepts, url_prefix='/intercepts')

# Sets the port, or defaults to 80
if (len(sys.argv) > 1):
    port = int(sys.argv[1])
else:
    port=80

app.run(debug=True, host='0.0.0.0', port=port)
