# 文衡网页版发布授权与 ECS 待确认项

本次配置保留原仓库、原服务器部署约定和 `deploy/deploy.sh`，没有连接 ECS、发布
网站、重启服务、执行数据库迁移，或变更生产数据。服务器身份和实际权限尚未核验。

## GitHub 侧的安全边界

仓库当前为公开仓库。`main` 受 PR、Code Owner、状态检查及禁止强推/删除的规则保护。
仓库级 Secrets 没有生产凭据；已有五个 `ALIYUN_*` Secrets 保留在 `production`
环境。本次只检查它们的名称，不读取或打印任何秘密值。

`production` 只接受 `main` 分支，必须由 `pasariga` 批准。批准自己的部署请求是
允许的，因为目前只有该所有者负责发布；这不允许普通协作者批准。普通协作者
不能修改环境审批规则，也不能通过创建开发分支工作流绕过该分支限制。
所有者具有管理员权限，因此仍需审查具体提交和工作流后再批准。

生产环境变量 `WENHENG_PRODUCTION_DEPLOY_ENABLED=false`。该开关在服务器身份、
受限 SSH 账号和命令包装器核验完成前必须保持关闭。缺失或任何非 `true` 值都会阻止
SSH 阶段。它是补充关闭开关，不能替代环境审批和分支保护。

CI 只使用 GitHub 托管的临时 Runner，令牌默认只读，不持有生产凭据。生产作业不
检出仓库、不安装依赖、不执行仓库中的脚本，也不使用第三方 Actions；只在审批后
传递经过验证的 SHA 给已有 SSH 命令包装器。应用代码是在后续正式发布时交由服务器
构建，因此仍必须审查业务代码、Dockerfile、Compose 和部署脚本。

## 以后如何发布

1. 同学提交 PR，经检查和所有者审核后合并到 `main`。
2. 等该提交的 `Web CI` **main push** 运行成功。记录完整 40 位提交 SHA。
3. 所有者在 **Actions → Deploy production → Run workflow** 选择 `main`，输入该
   SHA，先选 **validate-only**。此模式只核对 main、工作流提交和对应 CI，不使用
   `production` 环境、不读取部署秘密，也不连接 ECS。
4. 服务器核验完成并另行获准后，管理员才能将生产环境开关改为 `true`。
5. 对同一个仍为 main 最新版本的 SHA 选择 **deploy**；所有者再次审查待发布提交，
   在 **Review deployments** 中批准，作业才会取用受保护的 SSH 凭据并发送
   `deploy:<SHA>`。等待审批时 main 若已改变，作业停止，必须重新验证新版本。
6. 后续检查部署日志的 `DEPLOYMENT_OK`、网站和健康接口；本轮没有执行这一步。

普通分支推送、PR、合并、打标签和 GitHub Release 均不会自动连接生产。
手动请求发布后的构建、更新与健康检查由现有服务器部署流程自动完成；不是每次
开发提交后自动上线。不要仅凭 CI 成功就认为生产迁移安全或软件已上线。

## 原有服务器约定：仅文档证据，待实际核验

`deploy/GITHUB_ACTIONS.md` 的历史资料记载：

- 代码目录 `/opt/wenheng-production`；
- 私密配置 `/opt/wenheng-secrets/production.env`；
- 服务器专用覆盖文件 `/opt/wenheng-secrets/compose.server.yaml`；
- 最近部署标记 `/opt/wenheng-secrets/last-deployed-commit`；
- SSH 接受 `deploy:<40位SHA>`，通过服务器受限包装器调用原部署脚本。

这些资料不能证明当前 ECS 的实际状态。现有脚本涉及备份、Alembic 迁移、容器更新
和健康检查，绝不能作为“无副作用测试”直接运行。

以后连接已确认的 ECS 时，先只读确认：

1. 当前主机确实是文衡生产机，确认主机公钥，不猜测 IP；继续排除已停用的
   `8.133.234.29`，不连接 DSW 或其他项目服务器。
2. Git remote、部署分支和已部署 SHA；检查工作区是否干净，不自动 reset/stash。
3. Actions SSH 账号不是 root；密钥只允许固定的、root 所有且普通部署用户不可修改的
   forced-command 包装器；拒绝交互 shell、端口/代理/X11 转发与任意命令。
4. sudo 仅允许包装器所需的固定操作；不能给予通用 sudo，也不能把同学加入 Docker
   组。Docker 控制权通常等同主机高权限，不能当作无害的普通用户权限。
5. 包装器校验仓库、分支、完整 SHA、更新策略和并发锁；生产 env/主机覆盖配置不在
   Git 中，不能由同学的普通开发分支改写。
6. 数据备份、恢复演练和向后兼容迁移策略具备后，再单独批准首次正式发布。

若现有 SSH 密钥实际具有宽泛权限，应先在服务器侧收紧或更换专用部署身份，不能
因为名字叫“deploy”就认定它安全。本轮没有声称这些服务器条件已满足。

## 若以后转为私有且套餐不支持强制保护

不要直接改变可见性并继续沿用本流程。GitHub Free 的私有仓库不能依赖这些保护
能力；仅靠 `if: github.actor == ...`、CODEOWNERS 文件或 `workflow_dispatch` 不能
防止写入者改写工作流获取凭据。

在变更可见性或邀请不受信任写入者前，先暂停生产工作流，移出共享仓库中的部署
Secrets，并在服务器侧撤销或轮换相应密钥。生产授权改为共享仓库之外的所有者控制
通道：所有者在可信本地环境审查并固定 SHA 后，使用仅所有者持有的受限身份批准
已有服务器部署入口；或者在独立、已有且仅发布管理员可写的发布控制仓库执行。
不要新建重复的应用仓库，不自动执行共享仓库里的本地发布脚本，也不要给共享仓库
Runner 生产访问权。需要进一步配置独立授权边界后才可重新启用自动化。

这项备用方案是切换条件与实施要求，尚未部署；当前公开仓库的保护规则已实际启用。

官方依据：[分支保护](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)、
[环境与套餐限制](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)、
[Actions 秘密与不受信任代码](https://docs.github.com/en/actions/reference/security/secure-use)。
