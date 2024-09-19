# 部署方法

## 数据库

使用 postgresql，自行创建用户和数据库，并grant权限。

于是可以获得一个地址
```
postgresql://user:password@host:port/database
```

修改 alembic.ini 中 sqlalchemy.url 为该地址，然后在项目根目录执行
```
alembic upgrade head
```

## 后端

创建 `config.py`：
```shell
cp server/config.template.py server/config.py
```

编辑该文件，修改 `DatabaseConfig.url`, `JAccountAuth` 为需要的值，随意修改 `AppConfig.secret_key`（建议为随机字符串）。

使用 systemd service 配置 uwsgi 启动。参考 [uwsgi-dic.service](uwsgi-dic.service) 文件。

```
sudo cp uwsgi-dic.service /usr/lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable uwsgi-dic
```

## 前端

首先进入 `web` 目录, 创建并修改配置文件
```shell
cd web
cp const.template.ts const.ts
vim const.ts
```

然后下载依赖并构建

```shell
pnpm install
pnpm build
```

使用 nginx 等进行部署，使得

- `^/api/*` 转发到后端, 默认地址为 127.0.0.1:8000, 需要保持路径 `/api/`，默认需要使用 uwsgi_pass
- `^/*` 访问 dist 目录中的静态文件

特别注意，对于不存在的文件，也需要解析到 index.html。

参考 [nginx-dic.conf](nginx-dic.conf)

```shell
sudo cp nginx-dic.conf /etc/nginx/site-enabled/
```
