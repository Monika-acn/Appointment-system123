from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

appointments = []
id_counter = [1]

@app.route('/')
def home():
    return render_template('index.html')

# V1: Book Appointment
@app.route('/book', methods=['POST'])
def book():
    data = request.json
    if not data.get("name") or not data.get("date") or not data.get("time"):
        return jsonify({"success": False, "message": "Name, date and time are required."}), 400

    appointment = {
        "id": id_counter[0],
        "name": data["name"],
        "date": data["date"],
        "time": data["time"],
        "doctor": data.get("doctor", "General"),
        "reason": data.get("reason", ""),
        "status": "Confirmed"
    }
    id_counter[0] += 1
    appointments.append(appointment)
    return jsonify({"success": True, "message": f"Appointment booked successfully! ID: {appointment['id']}"})

# V2: View All / Search
@app.route('/all', methods=['GET'])
def view_all():
    return jsonify(appointments)

@app.route('/search', methods=['GET'])
def search():
    name = request.args.get('name', '').lower()
    result = [a for a in appointments if name in a["name"].lower()]
    return jsonify(result)

# V3: Cancel Appointment (mark as cancelled, don't remove)
@app.route('/cancel/<int:appt_id>', methods=['PUT'])
def cancel(appt_id):
    for a in appointments:
        if a["id"] == appt_id:
            if a["status"] == "Cancelled":
                return jsonify({"success": False, "message": "Already cancelled."})
            a["status"] = "Cancelled"
            return jsonify({"success": True, "message": f"Appointment #{appt_id} cancelled successfully."})
    return jsonify({"success": False, "message": "Appointment not found."}), 404

# V3: Delete Appointment (hard delete)
@app.route('/delete/<int:appt_id>', methods=['DELETE'])
def delete(appt_id):
    global appointments
    before = len(appointments)
    appointments = [a for a in appointments if a["id"] != appt_id]
    if len(appointments) < before:
        return jsonify({"success": True, "message": "Appointment deleted."})
    return jsonify({"success": False, "message": "Appointment not found."}), 404

# Stats endpoint for dashboard
@app.route('/stats', methods=['GET'])
def stats():
    total = len(appointments)
    confirmed = sum(1 for a in appointments if a["status"] == "Confirmed")
    cancelled = sum(1 for a in appointments if a["status"] == "Cancelled")
    return jsonify({"total": total, "confirmed": confirmed, "cancelled": cancelled})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
