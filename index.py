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
    temperature = db.Column(db.Integer, nullable=False)
    moisture = db.Column(db.Integer, nullable=False)
    lux = db.Column(db.Integer, nullable=False)
    is_selected = db.Column(db.Boolean)

    def __repr__(self):
        return '<Plant %r>' % self.name


class Sensor(db.Model):

    __tablename__ = 'sensor'

    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Integer, nullable=False)
    moisture = db.Column(db.Integer, nullable=False)
    lux = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return '<Sensor %r>' % self.temperature


@app.route('/')
def index():
    return render_template('index.html')

# API

class PlantSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'temperature', 'moisture', 'lux', 'is_selected')


class SensorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'temperature', 'moisture', 'lux')


# Init Schemas
plants_schema = PlantSchema(many=True)
sensor_schema = SensorSchema(many=True)

class Plants(Resource):
    def get(self):
        connection = db.session.connection()
        names = connection.execute("SELECT id, name FROM plant")
        plants = plants_schema.dump(names)
        return plants

class PlantParam(Resource):
    def get(self, id):
        connection = db.session.connection()
        name = connection.execute("SELECT * FROM plant WHERE id={}".format(id))
        plant = plants_schema.dump(name)
        return plant

    def post(self, id):
        data = request.get_json()
        connection = db.session.connection()
        connection.execute(
            "UPDATE plant SET is_selected=%s WHERE id=%s", (data['is_selected'],id)
        )
        connection.execute(
            "UPDATE plant SET is_selected=%s WHERE id!=%s", (0,id)
        )
        db.session.commit()
        return "seleccionada"


class Sensors(Resource):
    def get(self):
        connection = db.session.connection()
        sensingPlant=connection.execute("SELECT * FROM sensor")
        sensors = sensor_schema.dump(sensingPlant)
        return sensors

    def post(self):
        data = request.get_json()
        connection = db.session.connection()
        connection.execute("UPDATE sensor SET temperature=%s, moisture=%s, lux=%s WHERE id=1",(data['temperature'], data['moisture'], data['lux']))
        db.session.commit()
        return "Created"


api.add_resource(Plants, '/api/plants')
api.add_resource(PlantParam, '/api/plants/<string:id>')
api.add_resource(Sensors, '/api/sensors')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
