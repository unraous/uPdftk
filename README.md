# uPDFpwr

一个基于 [pypdf](https://pypdf.readthedocs.io/) 的简单 PDF 加密、解密与对象分析工具。

## 功能

- **PDF加密**：批量或单个文件加密，支持自定义密码。
- **PDF解密**：批量或单个文件解密，支持输入密码。
- **对象分析**：导出 PDF 所有对象内容到 TXT 文件。
- **对象流导出**：将 PDF 文件的原始内容以 ASCII 形式导出为 TXT。

## 使用方法

### 1. 交互模式

直接运行：

```bash
python main.py
```

根据提示选择加密或解密，并输入文件/目录路径和密码。

### 2. 命令行参数模式

```bash
python main.py [选项] [输入文件/目录] [密码/输出文件]
```

#### 常用选项

- `-h, --help`      显示帮助信息
- `-v, --version`   显示版本信息
- `-e, --encry`     加密PDF文件例：`python main.py -e input.pdf yourpassword`
- `-d, --depry`     解密PDF文件例：`python main.py -d input.pdf yourpassword`
- `-a, --analyse`   导出PDF对象内容到TXT例：`python main.py -a input.pdf [output.txt]`
- `-p, --print`     导出PDF原始对象流到TXT
  例：`python main.py -p input.pdf [output.txt]`

### 3. 批量处理

输入目录路径时，会自动处理目录下所有 PDF 文件，并输出到 `Encrypted` 或 `Decrypted` 子目录。

## 依赖

- Python 3.7+
- [pypdf](https://pypdf.readthedocs.io/)

安装依赖：

```bash
pip install pypdf
```

## 代码结构说明

- `main.py`：主程序，包含加密、解密、对象导出等所有功能。
- `is_pdf_file`：判断文件是否为有效 PDF。
- `encrypt_pdf_file`：加密单个 PDF 文件。
- `remove_pdf_password`：解密单个 PDF 文件。
- `batch_process`：加解密公用模块
- `print_to_txt`：导出 PDF 纯对象流内容为 TXT。
- `dump_pdf_objects`：导出 PDF 对象内容为 TXT。

## 注意事项

- 若加密/解密操作的输入路径为目录，则会将该目录下 `Encrypted` 或 `Decrypted` 文件夹。
- 解密时需输入正确的密码，否则会提示失败。
- 对象导出功能仅用于分析 PDF 结构，不保证内容可直接阅读。

---

如有问题欢迎反馈！
