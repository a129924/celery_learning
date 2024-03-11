from celery_app.utils._utils import load_toml_file

print(load_toml_file("./config/config.toml"))