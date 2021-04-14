import re
import pandas as pd


class MdParser:
    def __init__(self):
        self.PRIMARY_COLUMN_NAME = "大項目"
        self.SECONDARY_COLUMN_NAME = "中項目"
        self.TERTIARY_COLUMN_NAME = "小項目"
        self.PROCESS_COLUMN_NAME = "手順"
        self.CHECK_COLUMN_NAME = "確認項目"

        self.OTHER_COLUMNS = ["実施日", "実施者", "結果", "確認者"]

    def split_by_symbol(self, rows, symbol):
        target_row = [index for index, line in enumerate(rows) if line.startswith(symbol)]

        if len(target_row) == 0:
            print("not found")
            return None

        sheets = [
            rows[target_row[index] : target_row[index + 1]]
            for index, number in enumerate(target_row)
            if index + 1 != len(target_row)
        ]

        sheets.append(rows[target_row[len(target_row) - 1] :])

        return sheets

    def md_to_dataframe(self, sheet_data):

        df_header = [
            self.PRIMARY_COLUMN_NAME,
            self.SECONDARY_COLUMN_NAME,
            self.TERTIARY_COLUMN_NAME,
            self.PROCESS_COLUMN_NAME,
            self.CHECK_COLUMN_NAME,
        ]
        df_header.extend(self.OTHER_COLUMNS)

        df = pd.DataFrame(index=[], columns=df_header)

        row_items = {
            self.PRIMARY_COLUMN_NAME: "",
            self.SECONDARY_COLUMN_NAME: "",
            self.TERTIARY_COLUMN_NAME: "",
            self.PROCESS_COLUMN_NAME: "",
            self.CHECK_COLUMN_NAME: "",
        }

        process_index = 1
        for line in sheet_data:

            if line.startswith("## "):
                row_items[self.PRIMARY_COLUMN_NAME] = line[3:-1]
            elif line.startswith("### "):
                row_items[self.SECONDARY_COLUMN_NAME] = line[4:-1]
            elif line.startswith("#### "):
                row_items[self.TERTIARY_COLUMN_NAME] = line[5:-1]
            elif re.match("^[0-9]+[.].*$", line):
                row_items[self.PROCESS_COLUMN_NAME] += re.sub("[0-9]+[. ]", str(process_index) + ".", line, 1)
                process_index += 1
            elif re.match("^- \[.\].*$", line):
                row_items[self.CHECK_COLUMN_NAME] += re.sub("- \[.\]", "・", line, 1)
            # 手順と確認項目が両方設定されたら初期化
            elif row_items[self.PROCESS_COLUMN_NAME] and row_items[self.CHECK_COLUMN_NAME]:
                # 最後の改行コードを削除
                row_items[self.PROCESS_COLUMN_NAME] = row_items[self.PROCESS_COLUMN_NAME][:-1]
                row_items[self.CHECK_COLUMN_NAME] = row_items[self.CHECK_COLUMN_NAME][:-1]

                process_index = 1
                df = df.append(row_items, ignore_index=True)
                # 行データ初期化
                row_items = {
                    self.PRIMARY_COLUMN_NAME: "",
                    self.SECONDARY_COLUMN_NAME: "",
                    self.TERTIARY_COLUMN_NAME: "",
                    self.PROCESS_COLUMN_NAME: "",
                    self.CHECK_COLUMN_NAME: "",
                }

        return df