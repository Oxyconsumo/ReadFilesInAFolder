import os

def read_files_to_txt(root_dir, output_file):
    """
    读取目录下所有文件内容并输出到txt文件
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            # 遍历根目录下的所有文件和子目录
            for root, dirs, files in os.walk(root_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    try:
                        # 读取文件内容
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                        
                        # 写入分隔符和文件路径
                        outfile.write("=" * 50 + "\n")
                        outfile.write(f"文件位置: {file_path}\n")
                        outfile.write("=" * 50 + "\n")
                        
                        # 写入文件内容
                        outfile.write(content)
                        outfile.write("\n\n")  # 文件之间添加空行
                        
                        print(f"已处理文件: {file_path}")
                    
                    except UnicodeDecodeError:
                        # 如果遇到编码问题，尝试其他编码
                        try:
                            with open(file_path, 'r', encoding='gbk') as infile:
                                content = infile.read()
                            
                            outfile.write("=" * 50 + "\n")
                            outfile.write(f"文件位置: {file_path}\n")
                            outfile.write("=" * 50 + "\n")
                            outfile.write(content)
                            outfile.write("\n\n")
                            
                            print(f"已处理文件(GBK编码): {file_path}")
                        
                        except Exception as e:
                            outfile.write("=" * 50 + "\n")
                            outfile.write(f"文件位置: {file_path}\n")
                            outfile.write("=" * 50 + "\n")
                            outfile.write(f"无法读取文件: {str(e)}\n\n")
                            print(f"无法读取文件 {file_path}: {str(e)}")
                    
                    except Exception as e:
                        outfile.write("=" * 50 + "\n")
                        outfile.write(f"文件位置: {file_path}\n")
                        outfile.write("=" * 50 + "\n")
                        outfile.write(f"无法读取文件: {str(e)}\n\n")
                        print(f"无法读取文件 {file_path}: {str(e)}")
        
        print(f"\n所有文件内容已成功输出到: {output_file}")
    
    except Exception as e:
        print(f"程序执行出错: {str(e)}")

if __name__ == "__main__":
    # 设置要读取的目录路径
    directory_to_scan = input("请输入要扫描的目录路径: ").strip()
    
    # 检查目录是否存在
    if not os.path.exists(directory_to_scan):
        print("指定的目录不存在！")
    else:
        # 输出文件路径
        output_path = "D:/reading.txt"
        read_files_to_txt(directory_to_scan, output_path)