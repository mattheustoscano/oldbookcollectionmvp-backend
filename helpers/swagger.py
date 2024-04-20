from flask import Blueprint
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL="/swagger"
API_URL="/src/static/swagger.json"

def swagger_config(name, app):
        swagger_ui_blueprint = get_swaggerui_blueprint(
            SWAGGER_URL,
            API_URL,
            config={
                name: 'BookStore API Rest for MVP - PUC RJ'
            })
        app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
    