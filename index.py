from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3307/plantsDatabase'
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


def __repr__(self):
    return '<Config %r>' % self.param1


@app.route('/')
def index():
    connection = db.session.connection()
    names = connection.execute(
        "SELECT id, name FROM plant")
    return render_template('index.html', plantNames=names)


@app.route('/save_plant', methods=['POST'])
def save_plant():
    if request.method == 'POST':
        config = request.form.get('configSave', '')
        print(config)
        confid = Config.query.filter_by(id='1').first()
        confid.plantId = config
        db.session.commit()
        return redirect('/')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
