from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clicks.db'
db = SQLAlchemy(app)
CORS(app)

# Update the model to include a name field
class Clicks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # Name of the action (student_click, etc.)
    count = db.Column(db.Integer, default=0)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/student_click', methods=['POST'])
def student_click():
    return increment_click('student_click')

@app.route('/student_write', methods=['POST'])
def student_write():
    return increment_click('student_write')

@app.route('/staff_click', methods=['POST'])
def staff_click():
    return increment_click('staff_click')

@app.route('/staff_write', methods=['POST'])
def staff_write():
    return increment_click('staff_write')

@app.route('/clicks', methods=['GET'])
def get_clicks():
    all_clicks = Clicks.query.all()
    clicks_dict = {click.name: click.count for click in all_clicks}
    return jsonify(clicks_dict)

def increment_click(name):
    # Find the row with the corresponding name (route)
    click_data = Clicks.query.filter_by(name=name).first()
    if not click_data:
        click_data = Clicks(name=name, count=0)  # Create a new row if not found
        db.session.add(click_data)

    click_data.count += 1  # Increment the count
    db.session.commit()

    return jsonify({name: click_data.count})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
