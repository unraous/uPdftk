import os
import sys
import time
import itertools
import string

from pypdf import PdfReader, PdfWriter


def is_pdf_file(path):
    if not os.path.isfile(path):
        return False
    if not path.lower().endswith(".pdf"):
        return False
    with open(path, "rb") as f:
        header = f.read(4)
    return header == b"%PDF"


def remove_pdf_password(input_path, output_path, password):
    try:
        reader = PdfReader(input_path)
        if reader.is_encrypted:
            try:
                reader.decrypt(password)
            except Exception as e:
                print(f"密码错误或无法解密：{e}")
                return False
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        with open(output_path, "wb") as f:
            writer.write(f)
        print(f"已去除密码，输出文件：{output_path}")
        return True
    except Exception as e:
        print(f"处理失败：{e}")
        return False

def encrypt_pdf_file(input_path, output_path, password):
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(password)
        with open(output_path, "wb") as f:
            writer.write(f)
        print(f"已加密，输出文件：{output_path}")
        return True
    except Exception as e:
        print(f"加密失败：{e}")
        return False
    
def batch_process(exe, inp, key, mode="encrypt"):
    input_path = input("请输入PDF文件或目录路径：").strip() if exe else inp
    input_path = input_path.strip('"').strip("'")
    is_dir = os.path.isdir(input_path)
    list_pdf = []
    if is_dir:
        for filename in os.listdir(input_path):
            file_path = os.path.join(input_path, filename)
            if is_pdf_file(file_path):
                list_pdf.append(file_path)
                print(filename)
        if not list_pdf:
            print("[ERROR] 目录下没有有效的PDF文件。")
            sys.exit(1)
        if exe:
            print(f"确认{'加密' if mode=='encrypt' else '解密'}以上全部pdf文件？(y/n)")
            if input().strip().lower() == "n":
                print("已取消操作。")
                sys.exit(0)
    elif not is_pdf_file(input_path):
        print("[ERROR] 文件或目录不存在或不是有效的PDF文件。")
        sys.exit(1)

    output_dir = os.path.join(input_path if is_dir else os.path.dirname(input_path), "Encrypted" if mode == "encrypt" else "Decrypted")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    password = input("请输入要设置的PDF密码：").strip() if exe else key

    handler = encrypt_pdf_file if mode == "encrypt" else remove_pdf_password
    targets = list_pdf if is_dir else [input_path]
    for pdf_file in targets:
        filename = os.path.basename(pdf_file)
        output_file = os.path.join(output_dir, filename)
        handler(pdf_file, output_file, password)
    if exe:
        print(f"所有文件已存入：{output_dir}，程序将在三秒后自动关闭。")
        time.sleep(3)

# 替换原有 encry 和 depry
def encry(exe, inp, key):
    batch_process(exe, inp, key, mode="encrypt")

def depry(exe, inp, key):
    batch_process(exe, inp, key, mode="decrypt")


def print_to_txt(input_path, output_path):
    if not os.path.isfile(input_path):
        print("文件不存在或不是有效的PDF文件。")
        exit(1)
    pdf_path = input_path
    with open(pdf_path, "rb") as f:
        data = f.read()

    text = data.decode("ascii", errors="ignore")

    with open(
        output_path if output_path else os.path.join(
            os.path.dirname(input_path),
            os.path.splitext(os.path.basename(input_path))[0] + ".txt"
        ),
        "w",
        encoding="ascii"
    ) as f:
        f.write(text)
    print(f"所有对象内容已保存到：{output_path}")

    
def dump_pdf_objects(input_path, output_path=None):
    if not os.path.isfile(input_path):
        print("文件不存在或不是有效的PDF文件。")
        return
    reader = PdfReader(input_path)
    lines = []
    # 遍历所有对象号和代号
    for obj_id in reader.xref:
        try:
            obj = reader.xref[obj_id]
            lines.append(f"OBJ {obj_id}:\n{repr(obj)}\n{'-'*40}\n")
        except Exception as e:
            lines.append(f"OBJ {obj_id} ERROR: {e}\n{'-'*40}\n")
    if not output_path:
        output_path = os.path.splitext(input_path)[0] + "_objects.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"所有对象内容已保存到：{output_path}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("选择操作：")
        print("1. 加密PDF文件")
        print("2. 解密PDF文件")
        if input("请输入操作编号：").strip() == "1":
            encry(True, 0, 0)
        else:
            depry(True, 0, 0)


    elif len(sys.argv) == 2:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print("用法：")
            print("python main.py [选项] [输入文件/目录] [输出文件/目录]")
            print("选项：")
            print("  -h, --help        显示帮助信息")
            print("  -v, --version     显示版本信息")
            print("  -p, --print       生成PDF文件纯对象流txt")
            print("  -a, --analyse     生成PDF文件对象txt")
            print("  -d, --depry       解密PDF文件")
            print("  -e, --encry       加密PDF文件")
            exit(0)
        elif sys.argv[1] == "-v" or sys.argv[1] == "--version":
            print("版本：1.0.0")
            exit(0)
    elif len(sys.argv) == 3:
        if sys.argv[1] == "-p" or sys.argv[1] == "--print":
            print_to_txt(sys.argv[2], None)
        elif sys.argv[1] == "-a" or sys.argv[1] == "--analyse":
            dump_pdf_objects(sys.argv[2], None)
    elif len(sys.argv) == 4:
        if sys.argv[1] == "-d" or sys.argv[1] == "--depry":
            depry(False, sys.argv[2], sys.argv[3])
        elif sys.argv[1] == "-e" or sys.argv[1] == "--encry":
            encry(False, sys.argv[2], sys.argv[3])
        elif sys.argv[1] == "-a" or sys.argv[1] == "--analyse":
            dump_pdf_objects(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == "-p" or sys.argv[1] == "--print":
            print_to_txt(sys.argv[2], sys.argv[3])
