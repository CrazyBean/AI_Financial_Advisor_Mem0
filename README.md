# 基于 Mem0 记忆层的大模型个性化金融理财顾问系统 (AI Financial Advisor)

![Version](https://img.shields.io/badge/version-v1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.9%2B-green)
![LLM](https://img.shields.io/badge/LLM-Zhipu_GLM--4-orange)
![Memory](https://img.shields.io/badge/Memory-Mem0%20%7C%20Qdrant-red)

## 📖 项目简介
本项目基于智能体记忆框架 **Mem0** 构建，旨在实现一个具备“持久且动态演进记忆”能力的私人财富管理顾问。
为解决国内网络限制与数据合规问题，本项目底层引擎全面接入**纯国产大模型方案（智谱AI清言 GLM-4）**，实现本土化、高速、安全的记忆召回与个性化投资策略生成。

相比于传统的 RAG（检索增强生成），本系统的核心优势在于**长效记忆的提纯与衰减机制**，它能够记住用户的风险偏好、财务状况和历史决策，并在后续的多轮对话中“像真正的私人顾问一样”基于历史特征为您量身定制建议。

---

## 🏗️ 核心架构

系统主要分为三个核心层：
1. **记忆存储层 (Vector Store)**：使用 **Qdrant**（本地 SQLite 模式，已适配 MacOS 并发补丁），存储 Mem0 提取的高密度“用户特征/偏好”向量（1024维）。
2. **大脑模型层 (LLM & Embedder)**：全面接入 **智谱大模型 (`glm-4-flash`)** 与向量化模型 (`embedding-2`)。
3. **业务逻辑层**：
   - **记忆摄入**：用户输入 → 语义提纯特征 → 存入 Qdrant。
   - **策略生成**：用户提问 → 专属记忆检索 → 强上下文融合 → GLM-4 输出深度定制的私人理财建议。

---

## 🚀 快速运行指南

### 1. 克隆代码仓库
```bash
git clone https://github.com/CrazyBean/AI_Financial_Advisor_Mem0.git
cd AI_Financial_Advisor_Mem0
```

### 2. 安装环境依赖
强烈建议使用虚拟环境（venv 或 conda）。
```bash
pip3 install -r requirements.txt
```

### 3. 获取并配置 API Key
由于本项目使用智谱大模型，国内用户可前往 [智谱大模型开放平台](https://open.bigmodel.cn/) 注册并获取免费的 API Key。

在终端中设置环境变量：
```bash
# Mac / Linux
export ZHIPU_API_KEY="您的智谱API_KEY"

# Windows (CMD)
set ZHIPU_API_KEY="您的智谱API_KEY"
```
*(注：如果未设置环境变量，程序运行时也会友善地提示您输入 Key)*

### 4. 运行演示程序
```bash
python3 src/demo_run.py
```
启动后，直接在终端中进行交互，感受秒级的智能金融记忆与个性化策略推演！

---

## 📂 项目结构

```text
.
├── README.md               # 项目快速指南
├── requirements.txt        # Python 依赖清单
├── src/                    # 核心源代码库
│   ├── advisor.py          # 系统大脑：Mem0 初始化、记忆读写与 GLM-4 调用
│   └── demo_run.py         # 运行入口：终端交互界面与工作流组装
└── report/                 # 学术与汇报产出库 (文档/论文)
    └── 项目报告_基于Mem0的大模型个性化金融理财顾问系统.pdf (等相关材料)
```

## 🛠️ 已知问题与补丁说明
*   **MacOS SQLite 多线程报错**：`src/advisor.py` 中已包含 `Monkey Patch` 补丁（`check_same_thread=False`），彻底解决 Mem0 底层 Qdrant 在 Mac 环境下因并发导致的 SQLite 线程安全异常。开发者无需额外配置即可在 Mac 环境流畅运行。

## 📜 许可证 (License)
本项目为学术与研究用途构建，遵循 MIT 许可证。