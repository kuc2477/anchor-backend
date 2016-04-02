from app.server import create_app
from config import Prod

app = create_app(Prod, Prod.PROJECT_NAME)
