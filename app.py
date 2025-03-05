from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Welcome to My Sample Python App!</h1><p>This is a simple Flask application with build version version 1.1</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
