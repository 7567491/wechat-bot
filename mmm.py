import os

def merge_py_files():
    # 打开输出文件
    with open('mmm.txt', 'w', encoding='utf-8') as output_file:
        # 遍历当前目录及子目录
        for root, dirs, files in os.walk('.'):
            # 筛选出.py文件
            py_files = [f for f in files if f.endswith('.py')]
            
            for py_file in py_files:
                # 构建完整的文件路径
                file_path = os.path.join(root, py_file)
                
                # 写入分隔线和文件名
                output_file.write('\n' + '='*50 + '\n')
                output_file.write(f'File: {file_path}\n')
                output_file.write('='*50 + '\n\n')
                
                # 读取并写入Python文件内容
                try:
                    with open(file_path, 'r', encoding='utf-8') as input_file:
                        content = input_file.read()
                        output_file.write(content)
                        output_file.write('\n')
                except Exception as e:
                    output_file.write(f'Error reading file: {str(e)}\n')

if __name__ == '__main__':
    merge_py_files()
    print('合并完成！所有.py文件内容已保存到 mmm.txt')