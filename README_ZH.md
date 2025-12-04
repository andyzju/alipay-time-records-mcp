# 支付宝时空印记服务

这是一个基于高德地图 LBS 与 MCP 协议的"时空印记"服务，实现了用户在物理世界的数字化打卡功能。通过结合 AI 生成内容和地理信息数据存储，打造智能空间记忆系统。

## 功能特点

- **publish_checkin**: 完成定位 → 图像识别 → 文案生成 → 数据存储的完整链路
- **explore_nearby**: 基于当前位置搜索周边 POI 并结合语义进行智能推荐

## 技术架构

- **MCP框架**: 基于 FastMCP 框架实现
- **地理信息服务**: 高德地图 Web 服务 API
- **数据库**: Supabase (PostgreSQL + PostGIS 扩展)
- **AI模型**: 阿里云 DashScope Qwen-VL（多模态）

## 安装依赖

首先建议创建并激活虚拟环境：

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或者在Windows上使用 venv\Scripts\activate
```

然后安装依赖：

```bash
pip install -r requirements.txt
```

## 环境配置

复制 `.env.example` 文件为 `.env` 并填写相应配置：

```bash
cp .env.example .env
```

需要配置以下环境变量：
- `AMAP_API_KEY`: 高德地图API密钥
- `SUPABASE_URL`: Supabase项目URL
- `SUPABASE_KEY`: Supabase anon key
- `DASHSCOPE_API_KEY`: 阿里云DashScope API密钥

## 启动服务

### 方法一：使用启动脚本（推荐）

_stdio模式_：
```bash
./start.sh
```

_TCP模式_：
```bash
./start-tcp.sh
```

### 方法二：直接运行Python脚本

_stdio模式_：
```bash
python server.py
```

_TCP模式_：
```bash
python tcp_server.py
```

## 使用方式

服务提供了两个主要工具：

1. `publish_checkin` - 发布打卡信息
   - 参数:
     - `image_base64`: Base64编码的图片
     - `latitude`: 纬度
     - `longitude`: 经度
     - `user_comment`: 用户评论（可选）

2. `explore_nearby` - 探索附近地点
   - 参数:
     - `latitude`: 纬度
     - `longitude`: 经度
     - `radius`: 搜索半径（默认500米）

## 项目结构

```
.
├── server.py              # 主服务文件，基于FastMCP框架实现
├── tcp_server.py          # TCP服务支持文件
├── amap_service.py        # 高德地图API封装
├── schema.sql             # 数据库结构定义
├── requirements.txt       # Python依赖
├── .env.example           # 环境变量示例配置
├── start.sh               # stdio模式启动脚本
├── start-tcp.sh           # TCP模式启动脚本
└── ...
```

## 部署说明

服务支持多种部署方式：

1. **Stdio模式**: 适用于本地运行的MCP服务，通过标准输入/输出通信
2. **TCP模式**: 通过TCP连接，监听指定端口

## 测试

可以通过以下脚本测试服务功能：

```bash
python test_fastmcp_service.py
```