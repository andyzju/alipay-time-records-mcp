# Alipay Geo-Memory (支小宝·时空印记)

这是一个基于高德地图 LBS 与 MCP 的"时空印记"服务，允许用户在物理世界进行数字化打卡。

## 核心功能

1. **精准定位**：调用高德地图 API，将用户的经纬度转化为具体的场所名称，确保打卡信息的准确性。
2. **AI 赋能**：利用多模态大模型识别照片内容，结合高德返回的场所信息，自动生成高质量的打卡文案。
3. **空间存储**：将图片、文案、精确坐标、POI 信息存入支持 GIS 的数据库。
4. **智能推荐**：基于地理位置和语义（Tag），回答"附近有什么好玩的"。

## 技术栈

- **MCP Server**: Python (使用 mcp SDK, fastapi, uvicorn)
- **地理信息服务 (LBS)**: 高德地图 Web 服务 API (用于逆地理编码/POI 搜索)
- **数据库**: Supabase (PostgreSQL + PostGIS 扩展)
- **AI 模型**: OpenAI (GPT-4o) 或 DashScope (Qwen-VL)
- **HTTP 客户端**: httpx (用于请求高德 API)

## 安装和配置

1. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

2. 复制 `.env.example` 到 `.env` 并填写相应配置：
   ```
   cp .env.example .env
   ```

3. 配置数据库：
   执行 `schema.sql` 中的 SQL 脚本初始化数据库表结构和 PostGIS 扩展。

## 使用方法

启动服务：
```bash
python server.py
```

服务提供两个主要工具：

### publish_checkin
完成完整的"定位-识图-发布"链路。

参数：
- `image_base64` (string): 图片数据
- `latitude` (float): 纬度
- `longitude` (float): 经度
- `user_comment` (string, optional): 用户随口说的话

### explore_nearby
基于高德 POI 和用户数据进行语义推荐。

参数：
- `latitude` (float): 纬度
- `longitude` (float): 经度
- `radius` (int, optional): 搜索半径，默认为500米

## 开发指南

项目结构：
```
├── amap_service.py          # 高德地图服务封装
├── server.py                # MCP服务器主文件
├── schema.sql               # 数据库结构定义
├── requirements.txt         # 项目依赖
└── .env.example             # 环境变量示例
```
# Alipay Geo-Memory Service

This is the core service implementation for the Alipay Geo-Memory project. It provides geolocation-based check-in functionality with AI-powered content generation.

For detailed information about this project, please refer to [README_ZH.md](README_ZH.md) (Chinese documentation).

## Core Components

- `server.py` - Main FastMCP service implementation
- `tcp_server.py` - TCP server wrapper for SEE connections
- `amap_service.py` - AMap API integration service
- `schema.sql` - Database schema definition

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment variables by copying `.env.example` to `.env` and filling in your keys

3. Run the service:
   - Standard mode: `python server.py`
   - TCP mode: `python tcp_server.py`

Or use the provided scripts:
- Standard mode: `./start.sh`
- TCP mode: `./start-tcp.sh`