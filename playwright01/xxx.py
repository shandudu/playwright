from openpyxl import load_workbook
import pandas as pd

def update_cell(file_path, sheet_name, cell_address, new_value):
    """
    更新指定 Excel 文件中的单个单元格值，保持其他单元格格式不变。

    :param file_path: Excel 文件的路径
    :param sheet_name: 要修改的工作表名称
    :param cell_address: 要修改的单元格地址（例如 'A1'）
    :param new_value: 要设置的新值
    """
    try:
        # 加载工作簿
        workbook = load_workbook(file_path)

        # 选择工作表
        sheet = workbook[sheet_name]

        # 更新单元格值
        sheet[cell_address] = new_value

        # 保存工作簿
        workbook.save(file_path)
        print(f"单元格 {cell_address} 在工作表 '{sheet_name}' 中已更新。")

    except Exception as e:
        print(f"更新单元格时发生错误: {str(e)}")


def update_cell_with_pandas(file_path, sheet_name, cell_address, new_value):
    """
    使用 pandas 更新指定 Excel 文件中的单个单元格值，保持其他单元格格式不变。

    :param file_path: Excel 文件的路径
    :param sheet_name: 要修改的工作表名称
    :param cell_address: 要修改的单元格地址（例如 'A1'）
    :param new_value: 要设置的新值
    """
    try:
        # 读取 Excel 文件
        excel_file = pd.ExcelFile(file_path)

        # 将指定工作表加载为 DataFrame
        df = excel_file.parse(sheet_name)

        # 将单元格地址转换为 DataFrame 的行列索引
        row, col = int(cell_address[1:]) - 1, cell_address[0].upper()

        # 更新单元格值
        df.at[row, col] = new_value

        # 使用 ExcelWriter 保存文件，并保持其他格式不变
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"单元格 {cell_address} 在工作表 '{sheet_name}' 中已更新。")

    except Exception as e:
        print(f"更新单元格时发生错误: {str(e)}")

# 使用示例
# file_path = 'path/to/your/excel/file.xlsx'
# sheet_name = 'Sheet1'
# cell_address = 'B2'
# new_value = 'New Data'
#
# update_cell_with_pandas(file_path, sheet_name, cell_address, new_value)





if __name__ == '__main__':

# 使用示例
    file_path = 'D:\pythonProject\playwright\playwright01\\111.xlsx'
    sheet_name = 'Sheet1'
    cell_address = 'C1'
    new_value = 'New Data'

    # update_cell(file_path, sheet_name, cell_address, new_value)
    update_cell_with_pandas(file_path, sheet_name, cell_address, new_value)