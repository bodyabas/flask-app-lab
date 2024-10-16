from flask import Flask
app = Flask(__name__)

@app.route('/')
def main():
    return 'Hello, World!', 200

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/homepage') 
def home():
    """View for the Home page of your website."""

    return "This is your homepage :) "