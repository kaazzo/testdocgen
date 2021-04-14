import sys
import fire
import pathlib
import shutil
import pandas as pd
import openpyxl
from . import xlformat
from . import mdparser


def main(file_path):

    sf = pathlib.PurePath(file_path).suffix

    if sf != ".md":
        print("invalid file format.")
        sys.exit()

    wb = openpyxl.Workbook()
    md_parser = mdparser.MdParser()
    formatter = xlformat.XlFormat()

    with open(file_path, "r", encoding="UTF-8") as f:

        md_data = f.readlines()

        h1_blocks = md_parser.split_by_symbol(md_data, "# ")

        ex_file_name = pathlib.PurePath(file_path).stem + ".xlsx"

        with pd.ExcelWriter(ex_file_name) as writer:

            for sheet_data in h1_blocks:

                df = md_parser.md_to_dataframe(sheet_data)

                # h1の見出しをシート名に設定
                sheet_data_name = sheet_data[0][2:-1]
                df.to_excel(writer, sheet_name=sheet_data_name, index=False)

                worksheet_data = writer.sheets[sheet_data_name]

                formatter.formatting(worksheet_data)


if __name__ == "__main__":

    fire.Fire(main)