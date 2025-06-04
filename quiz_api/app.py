from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
	x = 'world!\n'
	return f"Hello, {x}"

if __name__ == "__main__":
    app.run()