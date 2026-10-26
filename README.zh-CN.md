[English](README.md) | [简体中文](README.zh-CN.md)

# 文衡 · WenHeng

面向中文写作练习的评测与提升应用，将图片导入、OCR 校对、多模型独立评审和原文证据反馈连接起来。仓库名保留为 `multi_model_essay`，当前前端的产品名称为**文衡**。

这是应用源码快照，不代表目前存在可用的公开在线服务。它与历史写作助手[妙笔智改（简称智笔，英文标识 ZhiBi）](https://github.com/pasariga/ProjectZhiBi) 分开管理；[OpenEssayScore](https://github.com/pasariga/OpenEssayScore) 则是独立打包的评分研究工具，分数尺度和证据范围不同，不是本应用的三路模型评审引擎。

## 使用流程

1. 注册或登录，提交正文或有序的多页图片，并补充写作信息。
2. 检查图片质量，识别文字，对照原图区域完成 OCR 校对。
3. 按统一结构化量规请求 DeepSeek、Qwen、豆包独立评审。
4. 比较评分和证据、查看分歧，按需交叉复核，阅读或导出已保存的报告。
5. 从个人历史重新打开作文，录入教师参考评分，使用修改和训练功能继续练习。

这些路径有代码实现，但外部服务仍需要有效账号、配置和模型访问权限。报告用于辅助学习，不是经过验证的教师评价替代品。

## 技术实现与已完成改进

| 范围 | 仓库中的实现依据 |
| --- | --- |
| 账号隔离 | `backend/app/api/` 与 `backend/app/modules/auth/` 中的 Bearer 会话、作文归属和访问校验。 |
| 图片／OCR | OpenCV 预处理保留原图和几何映射；默认百度手写 OCR，PaddleOCR 作为明确启用的本地备选；校对记录不覆盖原识别结果。 |
| 评审编排 | `backend/app/modules/reviews/` 中的提供方适配、结构化协议、并行尝试、重试／错误记录和最低完成数量／宽限策略，达到条件的批次不必无限等待慢服务。 |
| 评分解释 | 100 分归一化量规，四维各 25 分；分歧分析、证据偏移和独立复核记录。仅当教师样本达到配置阈值时启用历史可靠性权重。 |
| 写作提升 | 独立训练、润色和深度分析模块，以及 Vue 中的报告和历史界面。 |
| 验证边界 | `backend/TESTING.md` 区分离线测试与主动启用的真实服务 Smoke Test；模拟测试通过不能证明付费 API 或 OCR 账号可用。 |

历史提交包含素材、模拟考试流程和批注反馈的完善，属于实现改进，不代表已经量化验证了教学效果。较长的旧配置及接口资料保留在[原实现指南](docs/IMPLEMENTATION.zh-CN.md)；其中部分章节描述较早阶段，当前行为以源码为准。

## 架构

- **前端：**Vue 3、TypeScript、Vite，主要产品流程位于 `frontend/src/App.vue`。
- **后端：**FastAPI、SQLAlchemy／asyncpg、Alembic 和 PostgreSQL。
- **外部服务：**百度 OCR 与独立配置的评审提供方，API 凭据保留在服务端。
- **运行资料：**本地／生产 Compose、部署文档和服务就绪检查。

本应用并非完全离线：启用的 OCR 和评审服务会接收提交内容。部署前应确认材料使用授权及外部服务的数据处理要求。

## 本地启动

项目资料要求 Python 3.11+、Node.js 20+ 和 PostgreSQL 16+。使用自己的凭据，不要将真实 `.env`、数据库或上传内容提交到 Git。

```powershell
git clone https://github.com/pasariga/multi_model_essay.git
cd multi_model_essay
Copy-Item .env.example .env
docker compose up -d postgres
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
# 先将 DATABASE_URL 设置为本机 PostgreSQL 数据库，再执行迁移。
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe app.py
```

另开终端进入 `frontend/`，执行 `npm install`，复制 `.env.example` 为 `.env` 后执行 `npm run dev`。开发前端为 `http://localhost:5173`，后端 8000 端口提供 `/api/health`。在 `backend/.env` 配置对应服务的 Key 和模型标识后才能使用在线能力；PaddleOCR 需要明确配置 Worker，不会作为静默回退自动启动。

[部署说明](DEPLOYMENT.md) · [离线与真实服务测试](backend/TESTING.md) · [历史实现资料](docs/IMPLEMENTATION.zh-CN.md)

[多人协作与 PR 检查](docs/COLLABORATION.zh-CN.md) · [发布授权与 ECS 待确认项](docs/RELEASE_SECURITY.zh-CN.md)。合并 PR 不会自动部署生产网站。

## 状态、来源与许可

本轮文档整理没有部署应用、运行付费服务或新增性能／准确率结论。恢复源码本身不能证明在线服务可用或项目持续维护。

当前版本没有仓库级许可证文件，本 README 不新增授权；依赖和外部服务遵循各自条款。历史项目正式全称为妙笔智改，简称智笔，英文标识 ZhiBi；文衡是后续独立发展的应用，功能和成果仍按各自仓库归属。
