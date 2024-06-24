#from settings import app as application
from settings import *
from routes import *
from errors import *
from api import *

#app=application

if __name__ == "__main__":
    app.run(debug=True)
