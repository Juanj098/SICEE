from flask import Flask
from sqlalchemy import text
from app.config import Config
from app.extensions import db, migrate



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.modules.investigadores import ibp as investigadores_bp
    app.register_blueprint(investigadores_bp, url_prefix="/api/investigadores")

    from app.modules.catalogos import bp as catalogos_bp
    app.register_blueprint(catalogos_bp, url_prefix="/api/catalogos")
    
    # endpoint health
    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    # endpoint health_db
    @app.get("/api/health/db")
    def health_db():
        try:
            db.session.execute(text("SELECT 1"))
            return {"status":"ok", "database":"ok"}
        except Exception as e:
             return {"status": "error", "database": "unreachable", "detail": str(e)}, 503

    return app