# 冷风机智能选型系统 (Cooler Selection System)

基于 FastAPI 的工业冷风机智能选型 API 服务。根据冷库工况参数（蒸发温度、库温、需求冷量、制冷剂类型、供液方式等），自动计算并推荐最合适的冷风机型号。

## 技术栈

- **FastAPI**: 高性能 Python Web 框架，自动生成 OpenAPI 文档
- **SQLAlchemy**: ORM 框架，操作 MySQL 数据库
- **Pydantic / pydantic-settings**: 数据验证与配置管理
- **Uvicorn**: ASGI 服务器
- **PyMySQL**: MySQL 数据库驱动
- **openpyxl / xlrd**: Excel 产品数据读取与处理

## 项目结构

```
product_filter/
├── main.py                          # 应用入口：FastAPI 实例、路由注册、中间件
├── requirements.txt                 # Python 依赖
├── .env.example                     # 环境变量模板
├── DockerFile                       # Docker 镜像构建（注意：第1行有语法错误 FROM FROM）
├── parse_request_data.py            # 从 request_data.md 解析生成 MySQL DDL 的脚本
│
├── app/
│   ├── api/
│   │   ├── __init__.py              # API 路由聚合
│   │   └── v1/
│   │       ├── __init__.py          # v1 路由聚合
│   │       ├── products.py          # 核心 API：冷风机过滤、系列查询、PDF 上传下载
│   │       └── cooler_filter_url_examples.md  # 接口 URL 参数示例
│   │
│   ├── config/
│   │   ├── base.py                  # 基础配置类（Pydantic Settings）
│   │   ├── config.py                # 配置工厂，根据 FASTAPI_ENV 加载不同配置
│   │   ├── production.py            # 生产环境配置
│   │   └── testing.py               # 测试环境配置
│   │
│   ├── models/
│   │   ├── __init__.py              # 导出 Base、engine、get_db，创建所有表
│   │   ├── database.py              # SQLAlchemy 引擎、SessionLocal、事务装饰器
│   │   ├── dao.py                   # 核心数据模型：Cooler、CoolingCapacity、SCQuant
│   │   ├── product.py               # 早期通用模型（未实际使用）
│   │   └── repositories.py          # 仓库模式：BaseRepository 及业务 Repository
│   │
│   ├── schemas/
│   │   ├── equipment.py             # Pydantic 响应模型
│   │   ├── product.py               # 核心过滤请求模型 CoolerFilter
│   │   └── response.py              # 统一 API 响应包装
│   │
│   ├── services/
│   │   └── cooler_service.py        # 核心业务逻辑：冷风机过滤算法、PDF 管理
│   │
│   ├── sql/
│   │   ├── schema.sql               # 早期通用表结构（未使用）
│   │   ├── cooler_schema.sql        # 实际使用的冷风机表结构
│   │   ├── SC_quant.sql             # sc_quant 表结构
│   │   ├── cooler.sql               # 由 Excel 生成的 cooler 表 INSERT 语句
│   │   ├── cooling_capacity.sql     # 由 Excel 生成的 cooling_capacity 表 INSERT 语句
│   │   └── sc_quant_insert.sql      # 由 Excel 生成的 sc_quant 表 INSERT 语句
│   │
│   ├── utils/
│   │   ├── enums.py                 # 核心枚举：SCLevel、Refrigerant、RefrigerantSupplyType
│   │   ├── generate_cooler_sql.py   # Excel → cooler + cooling_capacity SQL
│   │   ├── cooler_excel_to_sql.py   # 早期 Excel→SQL 工具（已废弃）
│   │   ├── excel_to_sql.py          # 转换系数 Excel → sc_quant SQL
│   │   ├── check_excel_structure.py # Excel 结构检查
│   │   ├── range_classifier.py      # 范围分类工具（未使用）
│   │   ├── error_handlers.py        # 全局异常处理器
│   │   └── logger.py                # 日志配置
│   │
│   └── doc/                         # PDF 文档存储目录（运行期生成）
│
└── [18 个 Excel 文件]                # 各系列冷风机原始产品数据
    MJB30, MJB35, MJD35, MJH45, MJH50, MJH63,
    mjl63, MJL80, MJN45, MJN50, MJN63,
    MJQ50, MJQ63, MJW63, MJW80, MJX35, ...
```

## 核心功能

### 1. 冷风机智能过滤

系统根据用户输入的冷库工况参数，通过以下步骤计算并推荐最合适的冷风机型号：

1. **计算温差**: `delta_t = |库温 - 蒸发温度|`
2. **确定工况等级**: 根据蒸发温度确定 SC1~SC5 工况等级
3. **获取修正系数**: 查询 `sc_quant` 表获取工况修正系数 `q`
4. **获取制冷剂系数**: 根据制冷剂和供液方式获取修正系数
5. **计算目标冷量**: `target_cap = 需求冷量 / q / 制冷剂系数`
6. **匹配型号**: 在数据库中找到与目标冷量最接近的冷风机型号
7. **过滤排序**: 按片距、系列进一步过滤，返回 Top 6 推荐结果

### 2. 支持的制冷剂

| 制冷剂 | 说明 |
|--------|------|
| R404A | 常用制冷剂，适用于中低温 |
| R22 | 传统制冷剂（逐步淘汰） |
| R407C | 环保制冷剂 |
| R410A | 环保制冷剂 |
| R507C | 环保制冷剂，替代 R502 |
| R23 | 超低温制冷剂 |

### 3. 供液方式

- **直膨 (direct)**: 适用于小型系统
- **泵供液 (pump)**: 适用于大型系统

## 环境准备

### 1. 克隆项目

```bash
git clone <repository-url>
cd product_filter
```

### 2. 创建并激活虚拟环境

**Windows:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

复制 `.env.example` 为 `.env` 并修改：

```bash
cp .env.example .env
```

编辑 `.env`：

```env
# 应用配置
APP_NAME=CoolerSelection
APP_VERSION=1.0.0
API_PREFIX=/api/v1

# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=product_filter
DB_CHARSET=utf8mb4

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=app.log

# 安全配置（预留）
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. 初始化数据库

```sql
CREATE DATABASE product_filter DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

执行 SQL 脚本：

```bash
# 创建表结构
mysql -u root -p product_filter < app/sql/cooler_schema.sql
mysql -u root -p product_filter < app/sql/SC_quant.sql

# 导入数据（注意：cooling_capacity.sql 中可能含有 Excel 公式，需先处理）
mysql -u root -p product_filter < app/sql/cooler.sql
mysql -u root -p product_filter < app/sql/cooling_capacity.sql
mysql -u root -p product_filter < app/sql/sc_quant_insert.sql
```

### 6. 启动服务

**开发模式（带热重载）:**

```bash
python main.py
# 或
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**生产模式:**

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 7. 访问 API 文档

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API 端点

### 冷风机过滤

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/v1/products/cooler/filter` | 冷风机过滤（JSON Body） |
| GET | `/api/v1/products/cooler/filter/{evaporating_temp}/{repo_temp}/{required_cooling_cap}/{refrigerant}/{refrigerant_supply_type}/{fan_distance}` | 冷风机过滤（路径参数） |

**POST 请求示例：**

```json
{
  "evaporating_temp": -30,
  "repo_temp": -25,
  "required_cooling_cap": 150,
  "refrigerant": "R404A",
  "refrigerant_supply_type": "直膨",
  "fan_distance": 4.5,
  "series": "MJQ"
}
```

**GET 请求示例：**

```
GET /api/v1/products/cooler/filter/-30/-25/150/R404A/直膨/4.5
```

### 其他端点

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/v1/products/cooler/series` | 获取所有冷风机系列列表 |
| POST | `/api/v1/products/cooler/pdf` | 上传冷风机 PDF 文档 |
| GET | `/api/v1/products/cooler/{id}/pdf` | 下载冷风机 PDF 文档 |
| GET | `/health` | 健康检查 |

## 数据导入工具

### 从 Excel 生成冷风机 SQL

```bash
python app/utils/generate_cooler_sql.py
```

读取根目录下以系列命名的 Excel 文件（如 `MJQ50.xlsx`），生成：
- `app/sql/cooler.sql`
- `app/sql/cooling_capacity.sql`

### 从 Excel 生成修正系数 SQL

```bash
python app/utils/excel_to_sql.py
```

读取 `转换系数.xls`，生成：
- `app/sql/sc_quant_insert.sql`

## 参数选择建议

### 片距选择
- **4.5mm**: 适用于低温（-30℃以下）
- **6.0mm**: 适用于中温（-15℃左右）
- **8.0mm**: 适用于高温（-5℃以上）

### 温差建议
- 一般温差（库温 - 蒸发温度）：5-10℃
- 低温冷库：5-7℃
- 中温冷库：7-10℃
- 高温冷库：8-12℃

## 已知问题

1. **DockerFile 语法错误**: 第1行 `FROM FROM` 重复，需修正为 `FROM`
2. **cooling_capacity.sql 含 Excel 公式**: 部分行包含如 `=B3*1.1481` 的公式，导入前需替换为计算后的数值
3. **参数传递 Bug**: `cooler_service.py` 中日志和注释显示存在历史参数错位问题，当前代码已改用 `SCQuantRepository` 查询修正系数

## 开发说明

- 使用 Pydantic 进行数据验证和序列化
- 使用仓库模式封装数据库操作
- 使用装饰器管理数据库事务
- 统一 API 响应格式（`BaseResponse[T]`）
- 支持环境变量配置
- 全局异常处理器覆盖 HTTP、Validation、SQLAlchemy 异常

## 常见问题

### 1. 数据库连接失败

确保：
- MySQL 服务已启动
- `.env` 文件中的数据库配置正确
- 数据库用户有相应的访问权限

### 2. 虚拟环境激活失败（Windows）

PowerShell 可能需要执行：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. 启动服务时出现类型错误

如果出现 `TypeError: BaseResponse cannot be parametrized`，请检查 `app/schemas/response.py` 文件，确保 `BaseResponse` 类继承了 `typing.Generic`。

## 许可证

MIT License
