from flask import Flask, request, jsonify
import pyodbc
from flask_cors import CORS

app = Flask(__name__)

# CORS configuration
cors = CORS(app, resources={
    r"/add_user": {
        "origins": ["https://ccsem5app-eeahfff0bwg3a2ez.scm.westindia-01.azurewebsites.net"],
        "methods": ["POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    },
    r"/users": {
        "origins": ["*"],  # Allow all origins for this endpoint
        "methods": ["GET"],
        "allow_headers": ["Content-Type"]
    }
})

# Database connection string (replace with your Azure SQL Database connection info)
driver = '{ODBC Driver 18 for SQL Server}'
server = 'tcp:ccsem5server.database.windows.net,1433'
database = 'ccsem5db'
username = 'CloudSAc995b7fa'
authentication = 'ActiveDirectoryIntegrated'
encrypt = 'yes'
trust_certificate = 'no'
timeout = 30

connection_string = (
    f'DRIVER={driver};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'Encrypt={encrypt};'
    f'TrustServerCertificate={trust_certificate};'
    f'Connection Timeout={timeout};'
    f'Authentication={authentication}'
)

# Home route
@app.route('/')
def index():
    return 'Welcome to my Azure web app with a database!'

# Route to add a user
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    name = data['name']
    email = data['email']
    
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (Name, Email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "User added successfully!"})

# Route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    rows = cursor.fetchall()
    conn.close()

    users = []
    for row in rows:
        users.append({"ID": row[0], "Name": row[1], "Email": row[2]})

    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)
