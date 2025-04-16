from dataclasses import dataclass


class DatabaseConfig:
    url = "postgresql://username:password@127.0.0.1/database"
    connection_pool_recycle = 3600


@dataclass
class OauthConfig:
    name: str
    client_id: str
    secret_key: str
    auth_url: str
    token_url: str
    profile_url: str


JAccountAuth = OauthConfig(
    name="jaccount",
    client_id="",
    secret_key="",
    auth_url="https://jaccount.sjtu.edu.cn/oauth2/authorize",
    token_url="https://jaccount.sjtu.edu.cn/oauth2/token",
)

AuthCNAES = OauthConfig(
    name="cnaes",
    client_id="",
    secret_key="",
    auth_url="https://passport.cnaes.edu.cn/sso/oauth2/authorize",
    token_url="https://passport.cnaes.edu.cn/sso/oauth2/token",
)

OAUTH_MAP: dict[str, OauthConfig] = {
    JAccountAuth.name: JAccountAuth,
    AuthCNAES.name: AuthCNAES,
}


class AppConfig:
    secret_key = "secret_key"
    default_paging_size = 50
