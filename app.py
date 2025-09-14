from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # This enables CORS globally

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    print("Received:", data)  # Debug log

    rating = data.get('rating')
    message = data.get('message')

    if not rating or not message:
        return jsonify({"success": False, "error": "Rating and message are required."}), 400

    feedback_entry = Feedback(rating=rating, message=message)
    db.session.add(feedback_entry)
    db.session.commit()

    return jsonify({"success": True, "message": "Thank you for your feedback!"})

@app.route('/feedbacks', methods=['GET'])
def get_feedbacks():
    feedbacks = Feedback.query.order_by(Feedback.timestamp.desc()).all()
    result = [
        {
            "id": f.id,
            "rating": f.rating,
            "message": f.message,
            "timestamp": f.timestamp.isoformat()
        } for f in feedbacks
    ]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
# This is a simple Flask application that serves a feedback form and stores feedback in a SQLite database.