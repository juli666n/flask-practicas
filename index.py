from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow


app = Flask(__name__)
#Config Api
api = Api(app)
ma = Marshmallow(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456789*@localhost:3307/plantsDatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Plant(db.Model):

    __tablename__ = 'plant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    plantTemperature = db.Column(db.Integer, nullable=False)
    soilMoisture = db.Column(db.Integer, nullable=False)
    plantLux = db.Column(db.Integer, nullable=False)
    config = db.relationship("Config", uselist=False, back_populates="plant")

    def __repr__(self):
        return '<Plant %r>' % self.name


class Config(db.Model):

    __tablename__ = 'config'

    id = db.Column(db.Integer, primary_key=True)
    plantId = db.Column(db.Integer, db.ForeignKey(
        'plant.id'), nullable=False)
    plant = db.relationship("Plant", back_populates="config")


class Sensor(db.Model):

    __tablename__ = 'sensor'

    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Integer, nullable=False)
    moisture = db.Column(db.Integer, nullable=False)
    lux = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return '<Config %r>' % self.temperature


@app.route('/')
def index():
    return render_template('index.html')

# API

class PlantSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'plantTemperature', 'soilMoisture', 'lux')


class SensorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'temperature', 'moisture', 'plantLux')


# Init Schemas
plant_schema = PlantSchema(many=True)
sensor_schema = SensorSchema(many=True)

class Plants(Resource):
    def get(self):
        connection = db.session.connection()
        names = connection.execute("SELECT id, name FROM plant")
        sensingPlant=connection.execute("SELECT * FROM sensor")
        plants = plant_schema.dump(names)
        sensors = sensor_schema.dump(sensingPlant)
        return {
            "plants": plants,
            "sensors": sensors
        }

    def post(self):
        data = request.get_json()
        config= Config(plantId=data['plantId'])
        db.session.add(config)
        db.session.commit()
        return {
            "msg": "Configuración cargada"
        }

api.add_resource(Plants, '/api/plants')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
