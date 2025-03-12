from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clicks.db'
db = SQLAlchemy(app)
CORS(app)

class Clicks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

@app.route('/click', methods=['POST'])
def increment_click():
    click_data = Clicks.query.first()
    if not click_data:
        click_data = Clicks(count=0)
        db.session.add(click_data)

    click_data.count += 1
    db.session.commit()
    return jsonify({'count': click_data.count})

@app.route('/clicks', methods=['GET'])
def get_clicks():
    click_data = Clicks.query.first()
    return jsonify({'count': click_data.count if click_data else 0})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

