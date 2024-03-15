import socket


class Settings:
    hostname: str = socket.gethostname()
    port: int = 5555


settings = Settings()
