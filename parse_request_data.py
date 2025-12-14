#!/usr/bin/env python3
"""
Parse request_data.md and generate MySQL DDL statements.
"""
import re
import os

# 中文到英文的表名映射（根据内容推断）
TABLE_NAME_MAPPING = {
    "冷凝机": "condenser",
    "电源": "power_supply",
    "压缩机": "compressor",
    "风机": "fan",
    "蒸发器": "evaporator",
    "图片": "image"
}

# 中文到英文的字段名映射（根据内容推断）
FIELD_NAME_MAPPING = {
    "型号编码": "model_code",
    "电源": "power_supply",
    "适用库温": "applicable_temperature",
    "压缩机": "compressor",
    "压缩机数量": "compressor_count",
    "风机": "fan",
    "风机数量": "fan_count",
    "吸气进口": "suction_inlet",
    "液供接口": "liquid_supply_interface",
    "长": "length",
    "宽": "width",
    "高": "height",
    "安装尺寸高": "installation_height",
    "安装尺寸宽": "installation_width",
    "制冷剂": "refrigerant",
    "蒸发器": "evaporator",
    "射程": "range",
    "盘管化霜功率": "coil_defrost_power",
    "水盘化霜功率": "water_pan_defrost_power",
    "制冷量": "refrigeration_capacity",
    "重量": "weight",
    "电压": "voltage",
    "电流": "current",
    "功率": "power",
    "插头类型": "plug_type",
    "类型": "type",
    "压缩比": "compression_ratio",
    "工作压力": "working_pressure",
    "工作流量": "working_flow",
    "工作效率": "working_efficiency",
    "安装尺寸深": "installation_depth",
    "名称": "name",
    "工作电压": "working_voltage",
    "工作功率": "working_power",
    "关联id": "related_id",
    "图片URL": "image_url"
}

# 类型映射
TYPE_MAPPING = {
    "字符串": "VARCHAR",
    "整数": "INT",
    "浮点数": "FLOAT",
    "tinyint": "TINYINT"
}

def parse_request_data(file_path):
    """Parse request_data.md file and generate DDL statements."""
    tables = []
    current_table = None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        return tables
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if it's a table name (Chinese)
        if not line.startswith('-'):
            # New table
            table_name = TABLE_NAME_MAPPING.get(line, line.lower().replace(' ', '_'))
            current_table = {
                'name': table_name,
                'comment': line,
                'fields': []
            }
            tables.append(current_table)
        else:
            # Field definition
            if current_table is None:
                continue
                
            # Parse field line: - 属性名，类型，限制条件1，限制条件2...
            parts = [p.strip() for p in line[1:].split('，')]
            if len(parts) < 2:
                continue
                
            field_name = parts[0]
            field_type = parts[1]
            
            # Determine MySQL field name
            mysql_field_name = FIELD_NAME_MAPPING.get(field_name, field_name.lower().replace(' ', '_'))
            
            # Determine MySQL data type and length
            mysql_type = TYPE_MAPPING.get(field_type, "VARCHAR")
            length = 255  # Default length for strings
            
            # Check for length in parts
            for part in parts[2:]:
                if '长度' in part:
                    match = re.search(r'\d+', part)
                    if match:
                        length = int(match.group())
            
            # Build field definition
            field_def = {
                'name': mysql_field_name,
                'comment': field_name,
                'type': mysql_type,
                'length': length,
                'is_unique': False,
                'is_primary': False
            }
            
            # Check for unique constraint
            for part in parts[2:]:
                if '唯一' in part:
                    field_def['is_unique'] = True
            
            current_table['fields'].append(field_def)
    
    return tables

def generate_ddl(tables):
    """Generate MySQL DDL statements from parsed tables."""
    ddl_statements = []
    ddl_statements.append("-- Database schema generated from request_data.md")
    ddl_statements.append("-- Generated automatically by parse_request_data.py")
    ddl_statements.append("")
    
    for table in tables:
        # Start CREATE TABLE statement
        ddl_statements.append(f"-- Table: {table['name']} ({table['comment']})")
        ddl_statements.append(f"CREATE TABLE `{table['name']}` (")
        
        # Add primary key
        ddl_statements.append(f"  `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键',")
        
        # Add fields
        unique_keys = []
        for field in table['fields']:
            # Skip foreign key references (as requested)
            if '外键' in field['comment']:
                continue
                
            # Build field definition
            if field['type'] == 'VARCHAR':
                field_def = f"  `{field['name']}` {field['type']}({field['length']})"
            else:
                field_def = f"  `{field['name']}` {field['type']}"
            
            # Add NOT NULL constraint if applicable
            if field['type'] != 'VARCHAR':
                field_def += " NOT NULL"
            
            # Add comment
            field_def += f" COMMENT '{field['comment']}',"
            
            ddl_statements.append(field_def)
            
            # Track unique keys
            if field['is_unique']:
                unique_keys.append(field['name'])
        
        # Add default fields
        ddl_statements.append("  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',")
        ddl_statements.append("  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',")
        ddl_statements.append("  `is_deleted` TINYINT DEFAULT 0 COMMENT '是否逻辑删除',")
        ddl_statements.append("  `deleted_at` DATETIME DEFAULT NULL COMMENT '删除时间',")
        
        # Add unique constraints
        if unique_keys:
            for field in unique_keys:
                ddl_statements.append(f"  UNIQUE KEY `uk_{table['name']}_{field}` (`{field}`),")
        
        # Remove trailing comma from last line
        if ddl_statements[-1].endswith(','):
            ddl_statements[-1] = ddl_statements[-1][:-1]
        
        # End CREATE TABLE statement
        ddl_statements.append(f") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='{table['comment']}';")
        ddl_statements.append("")
    
    return "\n".join(ddl_statements)

def main():
    """Main function."""
    file_path = os.path.join(os.path.dirname(__file__), "app", "request_data.md")
    print(f"Reading file: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return
    
    # Parse the file
    tables = parse_request_data(file_path)
    print(f"Parsed {len(tables)} tables")
    
    # Generate DDL
    ddl = generate_ddl(tables)
    print(f"Generated DDL: {len(ddl)} characters")
    
    # Save to SQL file
    sql_dir = os.path.join(os.path.dirname(__file__), "app", "sql")
    os.makedirs(sql_dir, exist_ok=True)
    sql_file = os.path.join(sql_dir, "schema.sql")
    
    try:
        with open(sql_file, "w", encoding="utf-8") as f:
            f.write(ddl)
        print(f"DDL statements generated successfully and saved to {sql_file}")
        print("\nFirst 500 characters of DDL:")
        print(ddl[:500] + "..." if len(ddl) > 500 else ddl)
    except Exception as e:
        print(f"Error saving DDL: {e}")
        print("\nGenerated DDL:")
        print(ddl)

if __name__ == "__main__":
    main()
