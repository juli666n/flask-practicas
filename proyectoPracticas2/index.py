from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import jsonify
from flask import Flask, render_template

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://plantAdmin@localhost/plantsDatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Plants(db.Model):

    __tablename__= 'plant'

    id = db.Column(db.Integer, primary_key=True)
    plantName = db.Column(db.String(50), nullable=False)
    plantTemperature = db.Column(db.Integer, nullable=False, unique=False)
    plantLux = db.Column(db.Integer, nullable=False, unique=False)
    soilMoisture = db.Column(db.Integer, nullable=False, unique=False)
    plantDetails = db.Column(db.Text, nullable=True, unique=False)

    def __repr__(self):
        return '< >' % self.plantName


@app.route("/", methods=['GET'])
def index():
    try:
        nombre = request.args.get('nombre')
        if (nombre != ''):
            return 'Hola ' + nombre
        else:
            return render_template('index.html')
    except:
        return render_template('index.html')

    plants = Plants.query.all()
    plants = jsonify(str(plants))

if __name__=='main':
    app.run()
