from mark_read import readfile
from markui import Ui_FormMark
import html
import pickle
import os
import csv

HTML_1 = r"""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><style type="text/css">
p, li { white-space: pre-wrap; }
</style></head><body style=" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Ubuntu';">
"""

HTML_2 = r"""</span></p></body></html>"""

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
        self.ui.btn_yes.clicked.connect(self.btnyes)
        self.ui.btn_no.clicked.connect(self.btnno)
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

        writer.writerow(("", "uid", "word", "title", "cat"))

        for i in range(len(self.items)):
            yesno, word, title, cat = self.results[i]
            uid, *_ = self.items[i]

            if yesno is not True:
                continue

            if cat is None:
                catt = ""
            elif cat == 1:
                catt = "社会防疫动态"
            elif cat == 2:
                catt = "大众防护指南"
            elif cat == 3:
                catt = "专业知识科普"
            elif cat == 4:
                catt = "抗击疫情故事"

            writer.writerow(("", uid, word, title, catt))

        csvfile.close()

    def openfile(self):
        filename, x = QFileDialog.getOpenFileName(self.widget, "Open File")
        if not filename:
            return
        
        try:
            items = list(readfile(filename))
        except Exception as ex:
            QMessageBox.about(self.widget, "Error", "Cannot open file.")
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
        self.results = results or [[None, "", "", None] for _ in range(len(items))]
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

    def btnyes(self):
        if self.items is None:
            return
        
        yesno = True
        self.results[self.index][0] = yesno
        self.ui.btn_yes.setStyleSheet("background: green;" if yesno is True else "")
        self.ui.btn_no.setStyleSheet("background: red;" if yesno is False else "")
        self.saveinfo()

    def btnno(self):
        if self.items is None:
            return
        
        yesno = False
        self.results[self.index][0] = yesno
        self.ui.btn_yes.setStyleSheet("background: green;" if yesno is True else "")
        self.ui.btn_no.setStyleSheet("background: red;" if yesno is False else "")
        self.saveinfo()


    def saveinfo(self):
        if self.items is None:
            return

        title = self.ui.text_title.text()
        word = self.ui.text_word.text()
        cat = None
        if self.ui.radio_1.isChecked():
            cat = 1
        if self.ui.radio_2.isChecked():
            cat = 2
        if self.ui.radio_3.isChecked():
            cat = 3
        if self.ui.radio_4.isChecked():
            cat = 4
        self.results[self.index][1] = word
        self.results[self.index][2] = title
        self.results[self.index][3] = cat

        self.savefile()

    def updateinfo(self):
        if self.items is not None:
            yesno, word, title, cat = self.results[self.index]
            uid, freq, words, title1, detail1, title2, detail2, title3, detail3 = self.items[self.index]
            self.ui.btn_yes.setStyleSheet("background: green;" if yesno is True else "")
            self.ui.btn_no.setStyleSheet("background: red;" if yesno is False else "")
            self.ui.text_title.setText(title)
            self.ui.text_word.setText(word)
            self.ui.radio_1.setAutoExclusive(False)
            self.ui.radio_2.setAutoExclusive(False)
            self.ui.radio_3.setAutoExclusive(False)
            self.ui.radio_4.setAutoExclusive(False)
            self.ui.radio_1.setChecked(cat == 1)
            self.ui.radio_2.setChecked(cat == 2)
            self.ui.radio_3.setChecked(cat == 3)
            self.ui.radio_4.setChecked(cat == 4)
            self.ui.radio_1.setAutoExclusive(True)
            self.ui.radio_2.setAutoExclusive(True)
            self.ui.radio_3.setAutoExclusive(True)
            self.ui.radio_4.setAutoExclusive(True)
            self.ui.text_uid.setText(uid)
            self.ui.text_freq.setText(str(freq))
            self.ui.text_words.setText(words)
            self.ui.text_title_1.setText(title1)
            self.ui.text_title_2.setText(title2)
            self.ui.text_title_3.setText(title3)
            self.ui.text_detail_1.setHtml(HTML_1 + html.escape(detail1) + HTML_2)
            self.ui.text_detail_2.setHtml(HTML_1 + html.escape(detail2) + HTML_2)
            self.ui.text_detail_3.setHtml(HTML_1 + html.escape(detail3) + HTML_2)
            self.ui.lab_info.setText(f"{self.index+1} / {len(self.items)}")
        else:
            self.ui.btn_yes.setStyleSheet("")
            self.ui.btn_no.setStyleSheet("")
            self.ui.text_title.setText("")
            self.ui.text_word.setText("")
            self.ui.radio_1.setChecked(False)
            self.ui.radio_2.setChecked(False)
            self.ui.radio_3.setChecked(False)
            self.ui.radio_4.setChecked(False)
            self.ui.text_uid.setText("")
            self.ui.text_freq.setText("")
            self.ui.text_words.setText("")
            self.ui.text_title_1.setText("")
            self.ui.text_title_2.setText("")
            self.ui.text_title_3.setText("")
            self.ui.text_detail_1.setHtml(HTML_1 + HTML_2)
            self.ui.text_detail_2.setHtml(HTML_1 + HTML_2)
            self.ui.text_detail_3.setHtml(HTML_1 + HTML_2)
            self.ui.lab_info.setText("0 / 0")

def main():
    app = QApplication([])
    myapp = MarkApp()
    app.exec_()

if __name__ == "__main__":
    main()
