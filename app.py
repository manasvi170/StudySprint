import os
from dotenv import load_dotenv

load_dotenv()
from flask import Flask, request, redirect, render_template_string
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Home page
@app.route("/")
def home():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tasks ORDER BY task_id DESC")
    tasks = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>StudySprint</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    </head>
    <body>
        <header class="hero">
    <div>
        <p class="eyebrow">YOUR PERSONAL STUDY SPACE ✨</p>
        <h1>🌷 Welcome to StudySprint</h1>
        <p>Your little space to plan, focus, and grow.</p>
       </div>
        </header>

        <button type="button" onclick="enableReminders()">
            Enable Reminders 🔔
        </button>
        <form action="/add" method="POST">
        

    <input type="text" name="title"
           placeholder="What do you need to do?" required>

    <textarea name="description"
              placeholder="Add a task description..."></textarea>

    <label>Due Date:</label>
    <input type="date" name="due_date">

    <label>Due Time:</label>
    <input type="time" name="due_time">

    <button type="submit">Add task</button>

</form>


        <h2>My Study Tasks</h2>
        {% for task in tasks %}
    <div class="task"
     data-task-id="{{ task.task_id }}"
     data-title="{{ task.title }}"
     data-due-date="{{ task.due_date or '' }}"
     data-due-time="{{ task.due_time or '' }}"
     data-status="{{ task.status }}">
        <h3>{{ task.title }}</h3>

<p>{{ task.description or "No description added" }}</p>

<p>
    <strong>Due Date:</strong>
    {{ task.due_date or "Not set" }}
</p>

<p>
    <strong>Due Time:</strong>
    {{ task.due_time or "Not set" }}
</p>

<p>
    <strong>Status:</strong> {{ task.status }}
</p>

        {% if task.status == 'Pending' %}
        <form action="/complete/{{ task.task_id }}" method="POST">
            <button type="submit">Complete</button>
        </form>
        {% endif %}
    </div>
{% else %}
    <p>No tasks yet. Add your first task!</p>
{% endfor %}
<script>
    const notifiedTasks = new Set();

    function enableReminders() {
        if ("Notification" in window) {
            Notification.requestPermission().then(permission => {
                if (permission === "granted") {
                    alert("StudySprint reminders enabled!");
                    checkReminders();
                } else {
                    alert("Please allow notifications in your browser settings.");
                }
            });
        } else {
            alert("Your browser does not support notifications.");
        }
    }

    function checkReminders() {
        if (Notification.permission !== "granted") {
            return;
        }

        const tasks = document.querySelectorAll(".task");

        tasks.forEach(task => {
            const id = task.dataset.taskId;
            const title = task.dataset.title;
            const date = task.dataset.dueDate;
            const time = task.dataset.dueTime;
            const status = task.dataset.status;

            if (!date || !time || status !== "Pending") {
                return;
            }

            const deadline = new Date(date + "T" + time);
            const remaining = deadline.getTime() - Date.now();

            if (remaining > 0 && remaining <= 5 * 60 * 1000
                && !notifiedTasks.has(id)) {

                new Notification("StudySprint Reminder 🔔", {
                    body: title + " is due in 5 minutes!"
                });

                notifiedTasks.add(id);
            }
        });
    }

    setInterval(checkReminders, 15000);
    checkReminders();
</script>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">    
    </body>
    </html>
    """, tasks=tasks)


# Add a new task

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    due_date = request.form.get("due_date") or None
    due_time = request.form.get("due_time") or None

    if title:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO tasks (title, description, due_date, due_time)
            VALUES (%s, %s, %s, %s)
            """,
            (title, description, due_date, due_time)
        )



        connection.commit()
        cursor.close()
        connection.close()

    return redirect("/")

#Complete task
@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE tasks SET status = %s WHERE task_id = %s",
        ("Completed", task_id)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
