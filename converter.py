import re
import csv
import sys

def clean_text(text):
    # 清理文本中的多余空格和特殊字符
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_entries(text):
    # 分割文本成多个条目
    entries = []
    
    # 首先按换行分割
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    current_entry = []
    for line in lines:
        # 如果这行看起来像是新条目的开始（包含URL），且当前条目不为空
        if 'http' in line and current_entry:
            entries.append(' '.join(current_entry))
            current_entry = [line]
        else:
            current_entry.append(line)
    
    # 添加最后一个条目
    if current_entry:
        entries.append(' '.join(current_entry))
    
    return entries

def parse_entry(entry):
    # 尝试多种模式匹配网站信息
    patterns = [
        # 模式1: 名称：网址 - 描述
        r'(.*?)[:：]\s*(https?://[^\s]+)(?:\s*[-—]\s*(.*))?',
        # 模式2: 网址 - 名称 - 描述
        r'(https?://[^\s]+)\s*[-—]\s*(.*?)(?:\s*[-—]\s*(.*))?',
        # 模式3: 名称 网址 描述
        r'(.*?)\s+(https?://[^\s]+)(?:\s+(.*))?'
    ]
    
    for pattern in patterns:
        match = re.match(pattern, clean_text(entry))
        if match:
            groups = match.groups()
            if 'http' in groups[0]:  # 如果第一组是URL
                url = groups[0]
                name = groups[1]
                description = groups[2] if len(groups) > 2 else ""
            else:
                name = groups[0]
                url = groups[1]
                description = groups[2] if len(groups) > 2 else ""
            
            return {
                'name': clean_text(name),
                'url': clean_text(url),
                'description': clean_text(description) if description else ""
            }
    
    return None

def clear_csv():
    # 清除文件内容，只保留表头
    with open('sites.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["分类", "子分类", "网站名称", "网站链接", "描述"])
    print("已清除 sites.csv 文件内容，只保留表头")

def get_multiline_input():
    print("\n请粘贴网站信息，输入完成后：")
    print("请输入一个空行（直接按回车键）来结束输入")
    print("\n开始输入：")
    
    lines = []
    while True:
        try:
            line = input()
            if not line and lines:  # 如果输入空行且已经有内容，则结束输入
                break
            if line:  # 只添加非空行
                lines.append(line)
        except KeyboardInterrupt:
            print("\n操作已取消")
            sys.exit(0)
    
    return "\n".join(lines)

def convert_text_to_csv():
    try:
        print("请选择操作：")
        print("1. 添加新内容")
        print("2. 清除所有内容（只保留表头）")
        choice = input("请输入选项（1 或 2）：").strip()
        
        if choice == "2":
            clear_csv()
            return
        elif choice != "1":
            print("无效的选项，程序退出")
            return
        
        # 先获取分类和子分类
        print("\n请输入分类（例如：主线关注、商业、AI工具等）：")
        category = input().strip()
        print("请输入子分类（例如：网站、主页、推特等）：")
        subcategory = input().strip()
        
        # 使用改进的多行输入函数
        text = get_multiline_input()

        # 如果没有输入任何内容就退出
        if not text.strip():
            print("\n没有输入任何内容，程序退出")
            return

        # 提取所有条目
        entries = extract_entries(text)
        
        # 准备CSV数据
        csv_data = []
        
        # 检查sites.csv是否存在并读取现有数据
        try:
            with open('sites.csv', 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                csv_data = list(reader)
        except FileNotFoundError:
            # 如果文件不存在，添加表头
            csv_data = [["分类", "子分类", "网站名称", "网站链接", "描述"]]
        
        # 处理新条目
        for entry in entries:
            parsed = parse_entry(entry)
            if parsed:
                csv_data.append([
                    category,
                    subcategory,
                    parsed['name'],
                    parsed['url'],
                    parsed['description']
                ])
            else:
                print(f"警告：无法解析条目：{entry}")

        # 写入CSV文件
        with open('sites.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)

        print("\n转换完成！数据已保存到 sites.csv")
        print(f"成功处理了 {len(entries)} 个网站条目")

    except KeyboardInterrupt:
        print("\n操作已取消")
        sys.exit(0)

if __name__ == "__main__":
    convert_text_to_csv()