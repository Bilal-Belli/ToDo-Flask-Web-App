from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
app.config['MYSQL_HOST'] = 'localhost'       # Set to your MySQL host
app.config['MYSQL_USER'] = 'root'    # Set to your MySQL username
app.config['MYSQL_PASSWORD'] = '1234' # Set to your MySQL password
app.config['MYSQL_DB'] = 'todoflaskapp'      # Set to your MySQL database name

def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.json.get('task')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task, done) VALUES (%s, %s)", (task, False))
    conn.commit()
    id = cursor.lastrowid  # Get the ID of the newly added task
    cursor.close()
    conn.close()
    return jsonify({'message': 'Task added successfully', 'id': id})

@app.route('/update_task/<int:id>', methods=['POST'])
def update_task(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET done = NOT done WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Task updated successfully'})

@app.route('/delete_task/<int:id>', methods=['DELETE'])
def delete_task(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)