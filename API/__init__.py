from app import app
from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from API.blueprints.users.views import users_api_blueprint
from API.blueprints.blogs.views import blogs_api_blueprint

app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(blogs_api_blueprint, url_prefix='/api/v1/blogs')