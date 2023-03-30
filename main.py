# Import necessary libraries
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Flask app and SocketIO
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY")

socketio = SocketIO(app)

# Global variable to store rooms and their data
rooms = {}
ROOM_CODE_LENGTH = 4

# Function to generate a unique room code
def generate_unique_code(length):
    while True:
        code = "".join(random.choice(ascii_uppercase) for _ in range(length))
        if code not in rooms:
            return code

# Route for the home page
@app.route("/", methods=["POST", "GET"])
def home():
    # If the user is already in a room, redirect them to the room page
    if session.get("room") is not None and session.get("name") is not None:
        room = session["room"]
        if room in rooms:
            return redirect(url_for("room"))

    # If the user is not in a room, process their form submission
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join") is not None
        create = request.form.get("create") is not None

        # Validate user input
        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)
        if join and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)

        # Create or join a room
        room = code
        if create:
            room = generate_unique_code(ROOM_CODE_LENGTH)
            rooms[room] = {"members": 0, "usernames": [], "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)

        # Store room and name in session
        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    # Render the home page template
    return render_template("home.html")

# Route for the chat room page
@app.route("/room")
def room():
    # Check if the user is authorized to access the room page
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    # Render the room page template
    return render_template("room.html", code=room, messages=rooms[room]["messages"])

# SocketIO event handler for receiving messages
@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return

    # Create message content and add it to the room's message list
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

# SocketIO event handler for handling connections
@socketio.on("connect")
def connect(auth):
    # Get the current user's room and name from the session
    room = session.get("room")
    name = session.get("name")

    # If either the room or name are missing, do nothing and return
    if not room or not name:
        return

    # If the room doesn't exist, leave the current room and return
    if room not in rooms:
        leave_room(room)
        return

    # Join the current room
    join_room(room)

    # If the current room doesn't have a list of usernames yet, create one
    if "usernames" not in rooms[room]:
        rooms[room]["usernames"] = []

    # Send a message to all other unique users in the room that the current user has entered
    for username in set(rooms[room]["usernames"]):
        if username != name:
            send({"name": username, "message": "has entered the room"}, to=room)

    # Add the current user's name to the room's list of usernames
    rooms[room]["usernames"].append(name)

    # Send the list of unique usernames to the current client
    socketio.emit("user_list", {"users": list(
        set(rooms[room]["usernames"]))}, to=request.sid)

    # Increment the number of members in the current room
    rooms[room]["members"] += 1

    # Print a message to the console indicating that the user has joined the room
    print(f"{name} joined room {room}")

# SocketIO event handler for handling disconnections
@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    # If room still exists
    if room in rooms:
        # Decrease the members count
        rooms[room]["members"] -= 1
        # Delete room if no members left
        if rooms[room]["members"] <= 0:
            del rooms[room]
        else:
            # Send "has left the room" message to all other users in the room
            for username in rooms[room]["usernames"]:
                if username != name:
                    send({"name": username, "message": "has left the room"}, to=room)

    print(f"{name} has left the room {room}")


# Start the Flask App with SocketIO
if __name__ == "__main__":
    socketio.run(app, debug=True)
