from flask import Flask, render_template, request, jsonify
from hashmap import HashMap
from student import Student

app = Flask(__name__)
students = HashMap(8)

# Demo records for jury presentation
demo_students = [
    ("STU1001", "Aarav Sharma", 20, "Computer Science", 88.5),
    ("STU1002", "Priya Reddy", 21, "Information Technology", 92.0),
    ("STU1003", "Rahul Verma", 20, "Data Science", 84.0),
    ("STU1004", "Sneha Rao", 22, "Computer Science", 90.5),
    ("STU1005", "Kiran Kumar", 21, "Electronics", 79.5),
]
for sid, name, age, course, marks in demo_students:
    students.put(sid, Student(sid, name, age, course, marks))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/students", methods=["GET"])
def get_students():
    records = []
    for student in students.values():
        records.append(student.to_dict())
    return jsonify({
        "students": records,
        "size": students.size,
        "capacity": students.capacity,
        "load_factor": round(students.load_factor(), 3),
        "buckets": students.bucket_snapshot()
    })

@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.get_json()
    sid = str(data.get("student_id", "")).strip()
    name = str(data.get("name", "")).strip()
    course = str(data.get("course", "")).strip()

    if not sid or not name or not course:
        return jsonify({"error": "Student ID, name and course are required."}), 400

    try:
        age = int(data.get("age"))
        marks = float(data.get("marks"))
    except (TypeError, ValueError):
        return jsonify({"error": "Age must be an integer and marks must be numeric."}), 400

    if age < 1 or marks < 0 or marks > 100:
        return jsonify({"error": "Enter a valid age and marks between 0 and 100."}), 400

    is_update = students.contains(sid)
    student = Student(sid, name, age, course, marks)
    students.put(sid, student)

    return jsonify({
        "message": "Student updated successfully." if is_update else "Student added successfully.",
        "student": student.to_dict(),
        "capacity": students.capacity,
        "load_factor": round(students.load_factor(), 3),
        "buckets": students.bucket_snapshot()
    })

@app.route("/api/students/<student_id>", methods=["GET"])
def find_student(student_id):
    student = students.get(student_id)
    if student is None:
        return jsonify({"error": "Student not found."}), 404
    return jsonify({"student": student.to_dict()})

@app.route("/api/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = students.remove(student_id)
    if student is None:
        return jsonify({"error": "Student not found."}), 404
    return jsonify({
        "message": "Student deleted successfully.",
        "student": student.to_dict()
    })

@app.route("/api/hash-demo", methods=["POST"])
def hash_demo():
    data = request.get_json()
    sid = str(data.get("student_id", "")).strip()
    if not sid:
        return jsonify({"error": "Enter a student ID."}), 400
    return jsonify(students.hash_explanation(sid))

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5001)
