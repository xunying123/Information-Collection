class DatabaseConfig:
    url = "postgresql://username:password@127.0.0.1/database"
    connection_pool_recycle = 3600


class JAccountAuth:
    client_id = "client_id of OAuth2"
    secretkey = "secretkey of OAuth2"


class AppConfig:
    secret_key = "secret_key"
