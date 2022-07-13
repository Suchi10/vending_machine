import os


def get_database_url(driver, username, password, host, port, name) -> str:
    """
    Creating a database URl.
    """
    return f"{driver}://{username}:{password}@{host}:{port}/{name}"


DATABASE_URL = get_database_url(
    "postgresql", "postgres", "suchi", "localhost", "5432", "vending_machine"
)
