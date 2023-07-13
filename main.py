from flask import Flask
from flasgger import Swagger
from routes import predict

app = Flask(__name__)
predict.predict_routes(app)
Swagger(app)
app.config['SECRET_KEY'] = 'your-secret-key'

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
