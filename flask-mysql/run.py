from app import create_app
import app

app = create_app()

@app.route('/')
def home():
    return 'Hello, I am an building API!!'

if __name__ == '__main__':
    app.run(port=5006)