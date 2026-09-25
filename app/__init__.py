"""
=============================================================================
Capa de Presentación Web: app/__init__.py
Fábrica de la Aplicación Flask (Application Factory Pattern)
=============================================================================
"""

import os
from flask import Flask


def create_app() -> Flask:
    """Crea y configura la instancia de la aplicación web Flask."""
    app_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(app_dir, "templates")
    static_dir = os.path.join(app_dir, "static")

    app = Flask(
        __name__,
        template_folder=templates_dir,
        static_folder=static_dir
    )

    # Registrar rutas y controladores
    from app.routes import bp_main
    app.register_blueprint(bp_main)

    return app
