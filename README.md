# Custom HashMap-Based Student Record System

A jury-ready web application demonstrating a Student Record System implemented with a custom hash table.

## Key requirement

The student records are stored in a custom `HashMap` implemented in `hashmap.py`.

The implementation does **not** use Python's built-in `dict` as the data structure for records.

### Data structure concepts demonstrated

- Custom hash function
- Hash buckets
- Separate chaining for collision handling
- Linked-list nodes
- Insert / update
- Search
- Delete
- Contains
- Load factor
- Automatic resizing / rehashing
- Bucket visualization
- Step-by-step hash calculation

## Run on Windows

1. Install Python 3.10+.
2. Open Command Prompt inside this project folder.
3. Run:

```text
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

4. Open:

```text
http://127.0.0.1:5000
```

If `python` does not work, try `py`:

```text
py -m venv venv
venv\Scripts\activate
py -m pip install -r requirements.txt
py app.py
```

## Jury demo flow

1. Open the dashboard.
2. Show the preloaded student records.
3. Add a new student.
4. Search for the student by ID.
5. Delete the student.
6. Open the Hash Table Visualization.
7. Use "Hash Demo" to show how an ID maps to a bucket.
8. Explain that collisions are handled through linked-list chaining.
9. Add records until the load factor crosses 0.75 and explain automatic resizing.

## Project files

- `app.py` - Flask web server and API
- `hashmap.py` - custom hash table implementation
- `student.py` - student model
- `templates/index.html` - web UI
- `static/style.css` - styling
- `static/app.js` - frontend behavior
- `requirements.txt` - dependency
