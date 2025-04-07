from flask import Flask
from routes.render import bp as render_bp

app = Flask(__name__)
app.register_blueprint(render_bp)

if __name__ == "__main__":
    app.run(debug=True)
