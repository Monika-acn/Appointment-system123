from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# In-memory storage
appointments = []

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Book Appointment
@app.route('/book', methods=['POST'])
def book():
    data = request.json

    # Validation
    if not data.get("name") or not data.get("date") or not data.get("time"):
        return jsonify({"message": "All fields are required"}), 400

    appointment = {
        "id": len(appointments) + 1,
        "name": data["name"],
        "date": data["date"],
        "time": data["time"],
        "doctor": data.get("doctor", "General")
    }

    appointments.append(appointment)

    return jsonify({
        "message": "Appointment booked successfully",
        "data": appointment
    })

# (Extra feature even in v1 → shows project quality)
@app.route('/all', methods=['GET'])
def view_all():
    return jsonify(appointments)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
