from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
with app.app_context():

    print(current_app)

app.config['SECRET_KEY'] = '121312132123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assetData.db'


db = SQLAlchemy(app)


from routes import *







if __name__ == '__main__':
    app.run(debug=True)
