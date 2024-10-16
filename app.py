from flask import Flask, request, redirect, url_for

app = Flask(__name__)
app.config.from_pyfile("config.py")

@app.route('/')
def main():
    return 'Hello, World!', 200

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/homepage') 
def home():
    """View for the Home page of your website."""
    agent = request.user_agent
    return f"This is your homepage :) - {agent} "

@app.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", 0, int)
    year = 2024 - age

    return f"Welcome, {name} - {year}"

@app.route("/admin")
def admin():
    to_url = url_for("greetings", name="administrator", age=45, _external=True)
    print(to_url)
    return redirect(to_url)