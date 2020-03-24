from mark_read import readfile
from markui import Ui_FormMark
import html
import pickle
import os
import csv
import traceback
import sys

HTML_1 = r"""<!doctype html>
<html><body>
<pre>
"""

HTML_2 = r"""
</pre></body></html>"""

from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QMessageBox

class MarkApp:
    def __init__(self):
        self.widget = QWidget()
        self.ui = Ui_FormMark()
        self.ui.setupUi(self.widget)

        self.ui.btn_open.clicked.connect(self.openfile)
        self.ui.btn_save.clicked.connect(self.saveinfo)
        self.ui.btn_back.clicked.connect(self.btnprev)
        self.ui.btn_next.clicked.connect(self.btnnext)
        self.ui.btn_1_yes.clicked.connect(self.btnyes_1)
        self.ui.btn_1_no.clicked.connect(self.btnno_1)
        self.ui.btn_2_yes.clicked.connect(self.btnyes_2)
        self.ui.btn_2_no.clicked.connect(self.btnno_2)
        self.ui.btn_3_yes.clicked.connect(self.btnyes_3)
        self.ui.btn_3_no.clicked.connect(self.btnno_3)
        self.ui.btn_gencsv.clicked.connect(self.gencsv)

        self.filename = None
        self.items = None
        self.results = None
        self.index = None

        self.updateinfo()
        self.widget.show()

    def gencsv(self):
        if self.items is None:
            return

        self.saveinfo()
        
        csvfile = self.filename + ".csv"
        csvfile = open(csvfile, "w", newline="")
        writer = csv.writer(csvfile)

        writer.writerow(("id", "gencomment", "gencode", "problem"))

        for i in range(len(self.items)):
            yesno1, yesno2, yesno3 = self.results[i]
            writer.writerow((i, yesno1, yesno2, yesno3))
        csvfile.close()

    def openfile(self):
        self.savefile()

        filename, x = QFileDialog.getOpenFileName(self.widget, "Open File")
        if not filename:
            return
        
        try:
            items = list(readfile(filename))
            assert len(items) > 0
        except Exception as ex:
            exc = traceback.format_exc()
            print(exc, file=sys.stderr)
            QMessageBox.about(self.widget, "Error", "Cannot open file.\n" + exc)
            return

        pklfile = filename + ".pkl"
        results = None
        if os.path.exists(pklfile):
            try:
                results = pickle.load(open(pklfile, "rb"))
            except Exception as ex:
                pass

        self.filename = filename
        self.items = items
        self.results = results or [[None, None, None] for _ in range(len(items))]
        self.index = 0

        self.updateinfo()

    def savefile(self):
        if self.items is None:
            return

        pklfile = self.filename + ".pkl"
        pickle.dump(self.results, open(pklfile, "wb"))

    def btnprev(self):
        if self.items is None:
            return

        self.saveinfo()

        if self.index == 0:
            return

        self.index -= 1
        self.updateinfo()

    def btnnext(self):
        if self.items is None:
            return

        self.saveinfo()

        if self.index == len(self.items) - 1:
            return

        self.index += 1
        self.updateinfo()

    def btnyes_1(self):
        if self.items is None:
            return

        yesno = True
        self.results[self.index][0] = yesno
        self.ui.btn_1_yes.setStyleSheet("background: green;" if yesno is True else "")
        self.ui.btn_1_no.setStyleSheet("background: red;" if yesno is False else "")
        self.saveinfo()

    def btnyes_2(self):
        if self.items is None:
            return

        yesno = True
        self.results[self.index][1] = yesno
        self.ui.btn_2_yes.setStyleSheet("background: green;" if yesno is True else "")
        self.ui.btn_2_no.setStyleSheet("background: red;" if yesno is False else "")
        self.saveinfo()
    
    def btnyes_3(self):
        if self.items is None:
            return

        yesno = True
        self.results[self.index][2] = yesno
        self.ui.btn_3_yes.setStyleSheet("background: green;" if yesno is True else "")
        self.ui.btn_3_no.setStyleSheet("background: red;" if yesno is False else "")
        self.saveinfo()

    def btnno_1(self):
        if self.items is None:
            return

        yesno = False
        self.results[self.index][0] = yesno
        self.ui.btn_1_yes.setStyleSheet("background: green;" if yesno is True else "")
        self.ui.btn_1_no.setStyleSheet("background: red;" if yesno is False else "")
        self.saveinfo()

    def btnno_2(self):
        if self.items is None:
            return

        yesno = False
        self.results[self.index][1] = yesno
        self.ui.btn_2_yes.setStyleSheet("background: green;" if yesno is True else "")
        self.ui.btn_2_no.setStyleSheet("background: red;" if yesno is False else "")
        self.saveinfo()
    
    def btnno_3(self):
        if self.items is None:
            return

        yesno = False
        self.results[self.index][2] = yesno
        self.ui.btn_3_yes.setStyleSheet("background: green;" if yesno is True else "")
        self.ui.btn_3_no.setStyleSheet("background: red;" if yesno is False else "")
        self.saveinfo()


    def saveinfo(self):
        if self.items is None:
            return

        self.savefile()

    def updateinfo(self):
        if self.items is not None:
            yesno1, yesno2, yesno3 = self.results[self.index]
            comment, code = self.items[self.index]
            self.ui.btn_1_yes.setStyleSheet("background: green;" if yesno1 is True else "")
            self.ui.btn_1_no.setStyleSheet("background: red;" if yesno1 is False else "")
            self.ui.btn_2_yes.setStyleSheet("background: green;" if yesno2 is True else "")
            self.ui.btn_2_no.setStyleSheet("background: red;" if yesno2 is False else "")
            self.ui.btn_3_yes.setStyleSheet("background: green;" if yesno3 is True else "")
            self.ui.btn_3_no.setStyleSheet("background: red;" if yesno3 is False else "")

            self.ui.text_detail_1.setHtml(HTML_1 + html.escape(comment) + HTML_2)
            self.ui.text_detail_2.setHtml(HTML_1 + html.escape(code) + HTML_2)
            self.ui.lab_info.setText(f"{self.index+1} / {len(self.items)}")
        else:
            self.ui.btn_1_yes.setStyleSheet("")
            self.ui.btn_1_no.setStyleSheet("")
            self.ui.btn_2_yes.setStyleSheet("")
            self.ui.btn_2_no.setStyleSheet("")
            self.ui.btn_3_yes.setStyleSheet("")
            self.ui.btn_3_no.setStyleSheet("")
            self.ui.text_detail_1.setHtml(HTML_1 + HTML_2)
            self.ui.text_detail_2.setHtml(HTML_1 + HTML_2)
            self.ui.lab_info.setText("0 / 0")

def main():
    app = QApplication([])
    myapp = MarkApp()
    app.exec_()

if __name__ == "__main__":
    main()
