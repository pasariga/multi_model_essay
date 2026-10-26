# 文衡生产部署

生产部署沿用 GitHub 仓库作为代码源，由原 Ubuntu 服务器通过 Docker Compose 构建。本仓库当前为公开仓库；本轮没有改变可见性。

GitHub 协作与发布已分离：PR 和 main 推送仅执行 CI，不触发生产部署。正式发布由所有者手动选择已通过 CI 的完整 main SHA，并经过 production 环境审批；当前生产执行开关关闭，等待 ECS 身份及最小权限核验。详见 [发布安全说明](docs/RELEASE_SECURITY.zh-CN.md) 和 [GitHub Actions 说明](deploy/GITHUB_ACTIONS.md)。

下列服务器命令是管理员操作参考，不是本轮已执行的步骤。不要把包含迁移、容器更新的部署脚本作为只读验证运行。

## 数据安全边界

- `compose.production.yaml` 不创建、删除或重建 PostgreSQL 服务，只连接 `DATABASE_URL` 指向的现有数据库。
- 上传图片和头像保存在 Docker 卷 `wenheng_storage`。
- PaddleX/OCR 下载缓存保存在 `wenheng_paddlex_cache`，重建容器不会重复下载。
- 不要运行 `docker compose down -v`，也不要手工删除上述数据卷。
- Alembic 迁移前脚本必须检测到 `DATABASE_MIGRATION_BACKUP_CONFIRMED=yes`。

## 服务器前置条件

- Ubuntu x86_64，建议使用 Python 3.12 对应的容器镜像。
- Git、Docker Engine 和 Docker Compose plugin。
- 服务器具有 GitHub 私有仓库的只读权限，优先使用 GitHub Deploy Key。
- 可连通的 PostgreSQL 16 或兼容版本，并在修改 schema 前完成备份/快照。

## 首次部署参考（已有生产网站不要重复执行）

```bash
sudo mkdir -p /opt/wenheng
sudo chown "$USER":"$USER" /opt/wenheng
git clone git@github.com:pasariga/multi_model_essay.git /opt/wenheng
cd /opt/wenheng
cp deploy/production.env.example deploy/production.env
chmod 600 deploy/production.env
```

编辑 `deploy/production.env`：

- 将 `DATABASE_URL` 设为现有生产数据库，密码中的特殊字符需要 URL 编码。
- 填入 DeepSeek、Qwen、Ark 以及可选的百度 OCR 密钥。
- 设置正式域名对应的 `CORS_ORIGINS`。
- 确认数据库已有备份或云数据库快照后，将 `DATABASE_MIGRATION_BACKUP_CONFIRMED` 设为 `yes`。

执行：

```bash
./deploy/deploy.sh
```

默认只在服务器 `127.0.0.1:18080` 监听，避免抢占现有 80/443 端口。将 `deploy/nginx-host.conf.example` 中的域名替换为正式域名，放入主机 Nginx 配置后再申请 TLS 证书。

## 管理员手动更新参考

常规更新应使用上述授权发布流程。仅当管理员已核对目标版本并明确批准手动发布时，才在服务器执行：

```bash
cd /opt/wenheng
./deploy/deploy.sh
```

脚本只允许 fast-forward 更新，当服务器工作区存在未提交修改时会停止，不会覆盖服务器文件。
