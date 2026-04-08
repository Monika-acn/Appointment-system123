from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

appointments = []

@app.route('/')
def home():
    return render_template('index.html')

# Book Appointment
@app.route('/book', methods=['POST'])
def book():
    data = request.json

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

    return jsonify({"message": "Appointment booked successfully"})

# View All
@app.route('/all', methods=['GET'])
def view_all():
    return jsonify(appointments)

# 🔥 NEW: Search Appointment
@app.route('/search', methods=['GET'])
def search():
    name = request.args.get('name')

    result = [a for a in appointments if name.lower() in a["name"].lower()]
    return jsonify(result)

# 🔥 NEW: Delete Appointment
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    global appointments
    appointments = [a for a in appointments if a["id"] != id]
    return jsonify({"message": "Deleted successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
