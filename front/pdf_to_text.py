from io import StringIO
import re
#from pdfminer.high_level import extract_text_to_fp

from pdfminer.converter import TextConverter
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def _can_delete_line(_line) -> bool:
    PATTERNS = (
        # ヘッダーとフッター
        r"^テクニカルレポート$",
        r"^CDSL Technical Report$",
        r"^.*\d+ Cloud and Distributed Systems Laboratory$",
        # 脚注
        r"^\*\d+ .*$",
        # 参考文献の参照
        r"\[(\d+)(,\d+)*\]",
        # 数字だけ
        r"^\d+$",
        # 図表のキャプション
        r"^(図|表|ソースコード) \d+ .{,60}",
        # 見出し
        r"\d+(\.\d+)*\.? .{,20}",
        # 箇条書き
        r"^\( \d \) .*$",
        # 著者名
        r".*串田 高幸.*"
    )
    for p in PATTERNS:
        if re.fullmatch(pattern=p, string=_line):
            # print("match", line)
            return True
    return False


def pdf_to_text(file_body) -> str:
    output_string = StringIO()
    # extract_text_to_fp(file_body, output_string)
    # print(output_string.getvalue().strip())
    # return output_string.getvalue().strip()

    parser = PDFParser(file_body)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for i,page in enumerate(PDFPage.create_pages(doc)):
        interpreter.process_page(page)

    lines = output_string.getvalue().splitlines()
    for line in lines:
        if line == "":
            lines.remove(line)
            continue
        if line == "参考文献":
            break
        if _can_delete_line(line):
            lines.remove(line)
            continue
        # print(line)
    
    return ''.join(lines)