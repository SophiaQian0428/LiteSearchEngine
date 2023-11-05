import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pandas as pd


class MyWindow(QMainWindow):
    resulta_rank_count = 0
    resultb_rank_count = 0
    results = []
    entry_idx = 0
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Audit App")
        self.setGeometry(100, 100, 800, 600)

        self.csv_path_layout = QHBoxLayout()
        self.csv_path_layout.addWidget(QLabel('打开素材csv'))
        self.csv_path_edit = QLineEdit(self)
        self.csv_path_layout.addWidget(self.csv_path_edit)
        self.csv_path_choose = QPushButton('打开文件')
        self.csv_path_layout.addWidget(self.csv_path_choose)
        self.csv_path_choose.clicked.connect(self.csv_path_showFileDialog)

        self.top_label = QLabel("", self)
        self.top_label.setAlignment(Qt.AlignCenter)
        top_layout = QVBoxLayout()
        top_layout.addLayout(self.csv_path_layout)
        top_layout.addWidget(self.top_label)

        self.left_panel = QTextEdit(self)
        self.left_panel.setReadOnly(True)

        self.right_panel = QTextEdit(self)
        self.right_panel.setReadOnly(True)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.left_panel)
        bottom_layout.addWidget(self.right_panel)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

        self.left_panel.mousePressEvent = self.on_click_left
        self.right_panel.mousePressEvent = self.on_click_right

        self.left_panel.mouseDoubleClickEvent = self.on_double_click_left
        self.right_panel.mouseDoubleClickEvent = self.on_double_click_right


    def on_click_left(self, event):
        self.reset_panel(self.right_panel)
        self.highlight_panel(self.left_panel)

    def on_click_right(self, event):
        self.reset_panel(self.left_panel)
        self.highlight_panel(self.right_panel)

    def on_double_click_left(self, event):
        self.results.append("a")
        self.resulta_rank_count += 1
        self.next_entry()

    def on_double_click_right(self, event):
        self.results.append("b")
        self.resultb_rank_count += 1
        self.next_entry()

    def highlight_panel(self, panel):
        panel.setStyleSheet("border: 3px solid yellow;")

    def reset_panel(self, panel):
        panel.setStyleSheet("border: 1px solid gray;")

    def next_entry(self):
        self.reset_panel(self.left_panel)
        self.reset_panel(self.right_panel)
        question_column, resulta_column, resultb_column = self.df.columns.values[:3]

        if self.entry_idx >= len(self.df):
            self.df["audit_result"] = self.results
            new_csv_path = f"{os.path.splitext(os.path.basename(self.csv_path))[0]}_" \
                           f"a={self.resulta_rank_count/(self.resulta_rank_count+self.resultb_rank_count):.2f}_" \
                           f"b={self.resultb_rank_count/(self.resulta_rank_count+self.resultb_rank_count):.2f}.csv"
            self.df.to_csv(new_csv_path, encoding="ANSI")
            app = QApplication.instance()
            app.quit()
        question = self.df.loc[self.entry_idx][question_column]
        resulta = self.df.loc[self.entry_idx][resulta_column]
        resultb = self.df.loc[self.entry_idx][resultb_column]
        self.top_label.setText(question)
        self.left_panel.setText(resulta)
        self.right_panel.setText(resultb)
        self.entry_idx += 1

    def csv_path_showFileDialog(self):
        # 获取文件路径
        filename = QFileDialog.getOpenFileName(self, '选择文件', filter="CSV Files (*.csv);;All Files (*)")
        if filename[0]:
            # 将文件路径显示在QLineEdit中
            self.csv_path_edit.setText(filename[0])
            self.csv_path = self.csv_path_edit.text()
            self.df = pd.read_csv(self.csv_path, encoding='ANSI')
            self.resulta_rank_count = 0
            self.resultb_rank_count = 0
            self.entry_idx = 0
            self.next_entry()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
