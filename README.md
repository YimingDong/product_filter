# 产品过滤系统 (Product Filter System)

一个基于FastAPI的RESTful API服务，用于管理和查询产品信息，支持MySQL数据库集成。

## 技术栈

- **FastAPI**: 现代化的Python Web框架，用于构建高性能API
- **SQLAlchemy**: Python SQL工具包和ORM，用于数据库操作
- **MySQL**: 关系型数据库
- **Pydantic**: 数据验证和设置管理
- **Uvicorn**: ASGI服务器，用于运行FastAPI应用

## 项目结构

```
product_filter/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── equipment.py      # 设备相关API端点
│   ├── models/
│   │   ├── dao.py              # SQLAlchemy数据模型
│   │   └── repositories.py     # 仓库模式实现
│   ├── schemas/
│   │   └── response.py         # 标准API响应模型
│   ├── services/
│   │   └── equipment_service.py # 设备服务层
│   ├── database.py             # 数据库连接和会话管理
│   ├── main.py                 # 应用入口
│   └── settings.py             # 配置管理
├── sql/
│   └── schema.sql              # 数据库表结构SQL
├── .gitignore                  # Git忽略文件
├── README.md                   # 项目说明文档
├── requirements.txt            # 依赖列表
└── .env                        # 环境变量配置
```

## 如何启动项目

### 1. 克隆项目

```bash
git clone <repository-url>
cd product_filter
```

### 2. 创建并激活虚拟环境

**Windows (PowerShell):**

```powershell
python3.11 -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
python3.11 -m venv venv
.\venv\Scripts\activate.bat
```

**Linux/macOS:**

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

创建并编辑 `.env` 文件：

```bash
# 数据库连接配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=product_filter

# 应用配置
APP_NAME=ProductFilter
APP_VERSION=1.0.0
DEBUG=True
```

### 5. 初始化数据库

1. 确保MySQL服务已启动
2. 创建数据库：
   ```sql
   CREATE DATABASE product_filter DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. 执行SQL脚本创建表结构：
   ```bash
   mysql -u your_username -p product_filter < app/sql/schema.sql
   ```

### 6. 启动服务

**开发模式（带热重载）：**

```bash
uvicorn app.main:app --reload
```

**生产模式：**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 7. 访问API文档

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API端点

### 设备相关

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/v1/condensers | 获取所有冷凝器 |
| GET | /api/v1/condensers/{condenser_id} | 获取单个冷凝器 |
| POST | /api/v1/condensers | 创建冷凝器 |
| PUT | /api/v1/condensers/{condenser_id} | 更新冷凝器 |
| DELETE | /api/v1/condensers/{condenser_id} | 删除冷凝器 |
| GET | /api/v1/power-supplies | 获取所有电源 |
| GET | /api/v1/power-supplies/{power_supply_id} | 获取单个电源 |
| POST | /api/v1/power-supplies | 创建电源 |
| PUT | /api/v1/power-supplies/{power_supply_id} | 更新电源 |
| DELETE | /api/v1/power-supplies/{power_supply_id} | 删除电源 |

## 开发说明

- 使用Pydantic进行数据验证和序列化
- 使用仓库模式封装数据库操作
- 使用装饰器管理数据库事务
- 统一API响应格式
- 支持环境变量配置

## 常见问题

### 1. 数据库连接失败

确保：
- MySQL服务已启动
- `.env` 文件中的数据库配置正确
- 数据库用户有相应的访问权限

### 2. 启动服务时出现类型错误

如果出现 `TypeError: BaseResponse cannot be parametrized`，请检查 `app/schemas/response.py` 文件，确保 `BaseResponse` 类继承了 `typing.Generic`。

### 3. 虚拟环境激活失败

- Windows PowerShell可能需要执行 `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` 来允许运行脚本
- 确保使用正确版本的Python创建虚拟环境（要求Python 3.11+）

## 许可证

MIT License
