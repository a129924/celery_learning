def load_toml_file(path: str):
    from pytomlpp import load

    return load(path)
