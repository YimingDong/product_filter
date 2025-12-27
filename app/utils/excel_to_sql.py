import xlrd
from typing import List, Tuple
from datetime import datetime


def read_excel_to_sql_insert(
    excel_file_path: str,
    output_file_path: str,
    sheet_names: List[str] = None
) -> None:
    """
    读取Excel文件并生成MySQL INSERT语句
    
    Args:
        excel_file_path: Excel文件路径
        output_file_path: 输出SQL文件路径
        sheet_names: 要处理的工作簿名称列表，如果为None则处理所有工作簿
    """
    workbook = xlrd.open_workbook(excel_file_path)
    
    if sheet_names is None:
        sheet_names = workbook.sheet_names()
    
    insert_statements = []
    
    for sheet_name in sheet_names:
        sheet = workbook.sheet_by_name(sheet_name)
        
        if sheet.nrows < 2 or sheet.ncols < 2:
            print(f"工作簿 {sheet_name} 数据不足，跳过")
            continue
        
        print(f"处理工作簿: {sheet_name}")
        
        for row_idx in range(1, sheet.nrows):
            delta_t = sheet.cell_value(row_idx, 0)
            
            if delta_t == '' or delta_t is None:
                continue
            
            try:
                delta_t = float(delta_t)
            except (ValueError, TypeError):
                print(f"第 {row_idx + 1} 行，第 1 列的delta_t值无效: {delta_t}，跳过")
                continue
            
            for col_idx in range(1, sheet.ncols):
                evaporating_temp = sheet.cell_value(0, col_idx)
                quant = sheet.cell_value(row_idx, col_idx)
                
                if evaporating_temp == '' or evaporating_temp is None:
                    continue
                
                try:
                    evaporating_temp = float(evaporating_temp)
                except (ValueError, TypeError):
                    print(f"第 1 行，第 {col_idx + 1} 列的evaporating_temp值无效: {evaporating_temp}，跳过")
                    continue
                
                if quant == '' or quant is None:
                    continue
                
                try:
                    quant = float(quant)
                except (ValueError, TypeError):
                    print(f"第 {row_idx + 1} 行，第 {col_idx + 1} 列的quant值无效: {quant}，跳过")
                    continue
                
                insert_statement = (
                    f"INSERT INTO SC_quant (evaporating_temp, delta_t, quant, create_time, update_time, is_deleted) "
                    f"VALUES ({evaporating_temp}, {delta_t}, {quant}, NOW(), NOW(), 0);"
                )
                insert_statements.append(insert_statement)
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(f"-- SC_quant 表数据插入语句\n")
        f.write(f"-- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"-- 数据来源: {excel_file_path}\n\n")
        
        for statement in insert_statements:
            f.write(statement + '\n')
    
    print(f"\n成功生成 {len(insert_statements)} 条INSERT语句")
    print(f"输出文件: {output_file_path}")


def parse_sheet_names(sheet_name_str: str) -> List[str]:
    """
    解析工作簿名称字符串，支持/分隔符
    
    Args:
        sheet_name_str: 工作簿名称字符串，如"SC1/SC2/SC3/SC4"
    
    Returns:
        工作簿名称列表
    """
    return [name.strip() for name in sheet_name_str.split('/') if name.strip()]


def main():
    excel_file = "转换系数.xls"
    output_file = "app/sql/sc_quant_insert.sql"
    
    try:
        workbook = xlrd.open_workbook(excel_file)
        sheet_names = workbook.sheet_names()
        
        print(f"Excel文件: {excel_file}")
        print(f"所有工作簿列表: {sheet_names}")
        
        target_sheets = ['SC1', 'SC2', 'SC3', 'SC4']
        available_sheets = [s for s in target_sheets if s in sheet_names]
        
        print(f"要处理的工作簿: {available_sheets}")
        print(f"开始转换...\n")
        
        read_excel_to_sql_insert(excel_file, output_file, available_sheets)
        
        print("\n转换完成！")
        
    except FileNotFoundError:
        print(f"错误: 找不到文件 {excel_file}")
        print("请确保Excel文件在项目根目录下")
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
