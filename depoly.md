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

## 爬虫

每次运行`main.py`就可以进行一次内容更新的检测爬取与上传

运行环境`requirements.txt`位于仓库根目录，但`playwright`库所需二进制浏览器需要额外执行指令安装

```shell
playwright install
```

程序运行需要对应后端的账密与ip，llm模型的key与地址

需要注意所有本地文件为了便于检查均采用了绝对路径，请按需修改，如有需要请手动创建所需文件夹

运行`main.py`会自动从后端获得最新的网站列表，但对于新加入的网址并不会立即爬取，而是会经历一次初始化，在下次运行时才会开始爬取
