import json
import os
import pathlib
import sys

def process_json_files(input_dir, output_dir):
    """
    处理指定目录中的所有JSON文件，提取processed_response字段，保存为{id}.py
    
    Args:
        input_dir: 输入目录路径，包含JSON文件
        output_dir: 输出目录路径，保存处理后的Python文件
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"创建目录: {output_dir}")
    
    # 获取输入目录中的所有JSON文件
    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
    print(f"发现{len(json_files)}个JSON文件")
    
    processed_count = 0
    skipped_count = 0
    
    # 处理每个JSON文件
    for json_file in json_files:
        try:
            file_path = os.path.join(input_dir, json_file)
            
            # 读取JSON文件
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 获取id和processed_response内容
            item_id = data.get('id')
            processed_code = data.get('processed_response')
            
            if item_id is None:
                print(f"警告: 文件{json_file}中没有id字段，跳过")
                skipped_count += 1
                continue
                
            if not processed_code:
                print(f"警告: 文件{json_file}中id={item_id}没有processed_response内容，跳过")
                skipped_count += 1
                continue
            
            # 创建输出文件
            output_file = os.path.join(output_dir, f"{item_id}.py")
            
            # 写入Python文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(processed_code)
            
            print(f"已保存: {item_id}.py")
            processed_count += 1
            
        except Exception as e:
            print(f"处理文件{json_file}时出错: {e}")
            skipped_count += 1
    
    print(f"处理完成! 成功处理{processed_count}个文件，跳过{skipped_count}个文件")

if __name__ == "__main__":
    # 默认目录
    default_input_dir = 'baseline/sql7b'
    default_output_dir = 'sql7b'
    
    # 从命令行参数获取目录（如果提供）
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
    else:
        input_dir = default_input_dir
        
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    else:
        output_dir = default_output_dir
    
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    
    process_json_files(input_dir, output_dir)
