from routes import *
from errors import *
from api import *

app=Flask(__name__, template_folder="templates", static_folder="static")

if __name__ == "__main__":
    app.run(debug=True)
