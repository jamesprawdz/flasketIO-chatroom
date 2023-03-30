# Flask-SocketIO Chat Room

A simple chat room application built with Flask and Flask-SocketIO that allows users to create or join chat rooms and communicate in real-time.

## Features

- Real-time messaging
- Create new chat rooms
- Join existing chat rooms
- Unique room codes for easy sharing
- Secure session management with secret key

## Getting Started
---
### Prerequisites

- Python 3.6+
- Flask
- Flask-SocketIO
- python-dotenv

### Installation

**1. Clone the repository or download the source code.**

`git clone https://github.com/yourusername/flask-socketio-chat.git`

**2.  Change directory to the project folder.**

`cd flask-socketio-chat`

**3.  Create a virtual environment.**

`python3 -m venv venv`

**4. Activate the virtual environment.**

`source venv/bin/activate`

**5. Install the required dependencies.**

`pip install -r requirements.txt`

**6. Create a `.env` file to store the secret key for the Flask application.**

`touch .env`

**7. Generate a secure, random key and add it to the `.env` file.**

`FLASK_SECRET_KEY=<your_generated_secret_key>`

_Note: Replace `<your_generated_secret_key>` with the secure key you generated._

### Running the Application

---

**1. Start the Flask application with SocketIO support.**

`python main.py`

**2. To test the chat room application, you have two options:**

##### a.

**Multiple Devices:** You can use multiple devices (either your own or a friend's) that have followed the exact same instructions to set up the chat room application. Ensure that both devices are connected to the same network and use the appropriate IP address and port to access the application.

##### b.

**Single Device:** You can operate the chat room by opening two separate browser windows on the same device. Open a regular browser window with the chat room and another private/incognito window that has it as well. This way, you can test the chat room by yourself, simulating multiple users joining the chat.

## Application Structure
---
The project is organized as follows:
```bash
├── main.py
├── .env
├── templates
│ ├── base.html
│ ├── home.html
│ └── room.html
└── static
└── style.css
```
**-** `main.py`: The main application file that contains the Flask and Flask-SocketIO logic. -`.env`: A file to store environment variables, including the secret key for the Flask application.

**-** `templates`: A folder containing the HTML templates for the application.
- `base.html`: The base template that provides the common structure for other templates.
- `home.html`: The home page template, where users can enter their name and choose to create or join a chat room.
- `room.html`: The chat room template, where users can send and receive messages in real-time.

**-** `static`: A folder containing the CSS file for the application.

- `style.css`: The main stylesheet for the application.

## Security Implications
---
The application uses a secret key to secure sessions, which is essential for protecting user data and maintaining the integrity of the application. The secret key should be kept confidential, and it is recommended to use a strong, randomly generated key. In this project, the secret key is stored in the `.env` file, which should not be committed to version control to prevent unauthorized access.

## Wrapping Up
---
In conclusion, this Flask-SocketIO chat room application provides a simple and efficient way to communicate in real-time with multiple users. By following the setup instructions and implementing the required files, you'll have a fully functional chat room that can be tested across multiple devices or within a single device using different browser windows. Keep in mind the importance of securing your application with a secret key, and make sure to store it safely using environment variables. Enjoy connecting with others and exploring the power of real-time communication in your projects!
