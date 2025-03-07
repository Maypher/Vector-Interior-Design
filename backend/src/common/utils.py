def read_secret(name: str) -> str | None:
    """
    Reads a docker secret mounted at /run/secrets/<name>
    """
    secrets_path = "/run/secrets/"
    secret = None

    with open(f"{secrets_path}{name}", "r") as secret_file:
        secret = secret_file.read().strip()

    return secret
