from src.celery_app.utils import load_toml_file

print(load_toml_file("./config/config.toml"))
