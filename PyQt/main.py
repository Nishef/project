import cgitb
import time

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox
from persiantools.jdatetime import JalaliDate

from database_connection import Database

cgitb.enable(format='text')

jdate = JalaliDate.today().strftime("%Y/%m/%d")


# it's the first page appears
class Login(QDialog):

    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        uic.loadUi('C:/Datas/PyQt/login_form.ui', self)

        self.show()
        self.login_btn.clicked.connect(
            self.login_check)  # self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)

    @pyqtSlot()
    def login_check(self):
        self.username = self.lineEdit_username.text()
        self.password = self.lineEdit_password.text()

        try:
            db.check_connection(username=self.username, password=self.password)
            # print(db(result))
            # print(hasattr(db, 'result'))
            print(db.result)
            if db.result:
                # self.new_window=QtGui.QMainWindow()
                # Proposal().new_proposal()
                self.pps = Proposal()
                login_window.destroy()  # return self.pps  # self.pps.show_proposal()  # self.show()  # x=uic.loadUi('C:/Datas/PyQt/proposal_form.ui', self)  # pps.show_proposal()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("مشخصات خود را دوباره چک کنید.")
                # msg.setInformativeText('')
                msg.setWindowTitle("خطا")
                msg.exec_()
        except:
            print("check your database is connected and has correct datas!")


class Proposal(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(Proposal, self).__init__(*args, **kwargs)
        # uic.loadUi('C:/Datas/PyQt/proposal_form.ui', self)
        # self.show()
        self.show_proposal()
        # ####why zero in a list?1)cause when user wants to enter new proposal we don't have any edit_result and it's
        # a variable that defined  in edit_data not outside of it #2)list is for result of data cause output is a
        # list type and the first[0] one is id
        self.edit_result = [0]
        self.tlb_pre = None
        self.tlb_nex = None
        # self.plainTextEdit.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        # self.toolBar.toggleViewAction().setChecked(True)

        self.save_btn.clicked.connect(self.save_proposal)
        self.btn_show_my_data.clicked.connect(self.show_user_data)
        self.btn_show_all_data.clicked.connect(self.show_all_data)
        self.btn_page.clicked.connect(self.change_pages)

        self.tableWidget.itemClicked.connect(self.edit_data)
        # self.tableWidget.selectionModel().clearSelection()
        self.tlb_save.triggered.connect(self.save_proposal)
        self.tlb_new.triggered.connect(self.new_proposal)
        # date
        self.lbl_timenow.setText(jdate)
        # if self.plainTextEdit.cursorPositionChanged() and self.tlb_edit.triggered():
        # calling toolbar functions when clicked
        # self.tlb_edit.triggered.connect(self.edit)
        self.tlb_last.triggered.connect(self.last_data)
        self.tlb_first.triggered.connect(self.first_data)
        self.tlb_previous.triggered.connect(self.previous_data)
        self.tlb_next.triggered.connect(self.next_data)
        self.tlb_exit.triggered.connect(lambda: sys.exit())
        self.tlb_print.triggered.connect(self.file_print)
        self.tlb_copy.triggered.connect(self.lineEdit.copy)
        self.tlb_copy.triggered.connect(self.plainTextEdit.copy)
        self.tlb_copy.triggered.connect(self.plainTextEdit_2.copy)
        self.tlb_copy.triggered.connect(self.plainTextEdit_3.copy)
        self.tlb_paste.triggered.connect(self.paste_text)
        self.tlb_copy.triggered.connect(self.plainTextEdit_4.copy)
        # if db.result_edit and db.username == self.edit_result[1]:
        self.tlb_edit.triggered.connect(self.edit_data)
        self.tlb_cut.triggered.connect(self.lineEdit.cut)

        self.tlb_delete.triggered.connect(self.lineEdit.clear)
        self.tlb_cut.triggered.connect(self.plainTextEdit.cut)
        self.tlb_delete.triggered.connect(self.plainTextEdit.clear)
        self.tlb_cut.triggered.connect(self.plainTextEdit_2.cut)
        self.tlb_delete.triggered.connect(self.plainTextEdit_2.clear)
        self.tlb_cut.triggered.connect(self.plainTextEdit_3.cut)
        self.tlb_delete.triggered.connect(self.plainTextEdit_3.clear)
        self.tlb_cut.triggered.connect(self.plainTextEdit_4.cut)
        self.tlb_delete.triggered.connect(self.plainTextEdit_4.clear)
        # self.exit.triggered.connect(self.closeEvent)
        # option = self.plainTextEdit.document().defaultTextOption()
        # option.setTextDirection(Qt.LeftToRight)
        # self.plainTextEdit.document().setDefaultTextOption(option)
        # self.plainTextEdit.setLayoutDirection(Qt.RightToLeft)


    # override default exit button action
    @pyqtSlot()
    def closeEvent(self, *args):
        sys.exit()

    @pyqtSlot()
    def paste_text(self):
        # boolean output where cursor is
        cursor = self.lineEdit.hasFocus()
        cursor1 = self.plainTextEdit.hasFocus()
        cursor2 = self.plainTextEdit_2.hasFocus()
        cursor3 = self.plainTextEdit_3.hasFocus()
        cursor4 = self.plainTextEdit_4.hasFocus()
        # clipboard for save copied values
        clipboard = QApplication.clipboard()
        c_text = clipboard.text()
        # .text() is for current values if exists + adding clipboard to it.
        if cursor and c_text:
            self.lineEdit.setText(self.lineEdit.text() + c_text)
        elif cursor1 and c_text:
            self.plainTextEdit.setPlainText(self.plainTextEdit.toPlainText() + c_text)
            self.plainTextEdit.setAlignment(Qt.AlignCenter)
        elif cursor2 and c_text:
            self.plainTextEdit_2.setPlainText(self.plainTextEdit_2.toPlainText() + c_text)
        elif cursor3 and c_text:
            self.plainTextEdit_3.setPlainText(self.plainTextEdit_3.toPlainText() + c_text)
        elif cursor4 and c_text:

            self.plainTextEdit_4.setPlainText(self.plainTextEdit_4.toPlainText() + c_text)
        else:
            # if clipboard is empty this line prevent app crash
            c_text = None

    @pyqtSlot()
    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    @pyqtSlot()
    def change_pages(self):
        # i=0
        # self.ui.stackedWidget.setCurrentIndex(i+1)
        current_page = self.stackedWidget.currentIndex()
        if current_page == 0:
            current_page = current_page + 1
            self.stackedWidget.setCurrentIndex(current_page)
            self.btn_page.setText('مشاهده سوال')
        else:
            current_page = current_page - 1
            self.stackedWidget.setCurrentIndex(current_page)
            self.btn_page.setText('لیست سوالات')

    # if don't want Login u don't need this function
    @pyqtSlot()
    def show_proposal(self):
        # self.pps=Proposal()
        # if self.ui!=True:
        # uic.loadUi('C:/Datas/PyQt/proposal_form.ui', self)
        # removeToolBar(toolBar)
        # start hidden
        # self.toolBar.toggleViewAction().trigger()
        uic.loadUi('C:/Datas/PyQt/proposal_form.ui', self)
        self.lbl_user.setText(db.username)
        # self.plainTextEdit.setHtml("<p align=\"right\">This paragraph is right aligned")

        self.show()  # if sys.exit():  # self.destroy()  # self.pps.replace(self.pps)  # uic.loadUi('C:/Datas/PyQt/proposal_form.ui', self)  # app._exec()

    @pyqtSlot()
    def new_proposal(self):
        # QtWidgets.QApplication.__init__(self, sys.argv)
        # self.mainWindow = QtWidgets.QMainWindow()
        # self.setupUi(self.MainWindow)
        # # Setup all the slots and other configuration stuff
        # self.mainWindow.show()
        # self.exec_()
        # pps = Proposal(self)
        self.destroy()
        self.pps = Proposal()
        self.show()

    @pyqtSlot()
    def save_proposal(self):

        buttonReply = QMessageBox.question(self, 'توجه', "آیا میخواهید عملیات انجام شود؟",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:

            pps1 = self.plainTextEdit.toPlainText()
            pps2 = self.plainTextEdit_2.toPlainText()
            pps3 = self.plainTextEdit_3.toPlainText()
            pps4 = self.plainTextEdit_4.toPlainText()
            title = self.lineEdit.text()
            combo = self.comboBox.currentText()
            ##############very important part###################### insert & update
            if db.id or self.edit_result[0]:
                db.update_data(pps1, pps2, pps3, pps4, title, self.edit_result[0], combo)
                self.statusBar.setStyleSheet("QStatusBar{background:green;}")
                self.statusBar.showMessage("دیتای شما با موفقیت ثبت شد", 3000)
                time.sleep(3)
                self.statusBar.setStyleSheet("QStatusBar{background:#eeeeee;}")

            else:
                db.insert_data(pps1, pps2, pps3, pps4, title, combo)
                self.statusBar.setStyleSheet("QStatusBar{background:green;}")
                self.statusBar.showMessage("دیتای شما با موفقیت ثبت شد", 3000)
                time.sleep(3)
                self.statusBar.setStyleSheet("QStatusBar{background:#eeeeee;}")
                ################################################################

    # data preview for current user
    @pyqtSlot()
    def show_user_data(self):
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeaderItem(0).setText("شماره")
        self.tableWidget.horizontalHeaderItem(1).setText("شناسه کاربری")
        self.tableWidget.horizontalHeaderItem(2).setText("نام کاربر")
        self.tableWidget.horizontalHeaderItem(3).setText("تاریخ")
        self.tableWidget.horizontalHeaderItem(4).setText("عنوان")
        if self.tableWidget.rowCount() > 0:
            # self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)

        db.show_user_data(db.username)
        x = len(db.result_show_user_data)

        # print(db.result)
        if x > 0:
            for row_number, row_data in enumerate(db.result_show_user_data):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setColumnCount(x)
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("شما دیتایی ثبت نکرده اید!")
            # msg.setInformativeText('')
            msg.setWindowTitle("خطا")
            msg.exec_()

    # data preview for all users
    @pyqtSlot()
    def show_all_data(self):
        # naming header
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeaderItem(0).setText("شماره")
        self.tableWidget.horizontalHeaderItem(1).setText("شناسه کاربری")
        self.tableWidget.horizontalHeaderItem(2).setText("نام کاربر")
        self.tableWidget.horizontalHeaderItem(3).setText("تاریخ")
        self.tableWidget.horizontalHeaderItem(4).setText("عنوان")
        if self.tableWidget.rowCount() > 0:
            # self.tableWidget.clearContents()
            self.tableWidget.setRowCount(0)

        db.show_all_data()
        x = len(db.result_show_all_data)
        for row_number, row_data in enumerate(db.result_show_all_data):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setColumnCount(x)
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

    @pyqtSlot()
    def edit_data(self):
        items = self.tableWidget.selectedItems()
        self.edit_result = []
        self.item = []
        if not self.tlb_pre and not self.tlb_nex:
            # this line gets one row information when clicked(it shows only few columns)
            # iterate through items to get first one which is id
            for i in items:
                self.item.append(i.data(0))

            print(self.item[0])
            # pass id for getting all needed columns
            db.edit_data(self.item[0])

        for i in db.result_edit:
            for j in i:
                self.edit_result.append(j)

        self.tlb_pre, self.tlb_nex = False, False
        print(self.edit_result)
        if db.result_edit and db.username == self.edit_result[1]:
            self.change_pages()
            self.plainTextEdit.setPlainText(self.edit_result[2])
            self.plainTextEdit_2.setPlainText(self.edit_result[3])
            self.plainTextEdit_3.setPlainText(self.edit_result[4])
            self.plainTextEdit_4.setPlainText(self.edit_result[5])
            self.lineEdit.setText(self.edit_result[6])
            self.lbl_qid.setText(str(self.edit_result[0]))
            self.lbl_writer_name.setText(str(self.edit_result[1]))
            self.lbl_data_date.setText(str(self.edit_result[7]))
            self.comboBox.setCurrentText(self.edit_result[8])
            self.plainTextEdit.setReadOnly(False)
            self.plainTextEdit_2.setReadOnly(False)
            self.plainTextEdit_3.setReadOnly(False)
            self.plainTextEdit_4.setReadOnly(False)
            self.lineEdit.setReadOnly(False)
            self.plainTextEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.plainTextEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.plainTextEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.plainTextEdit_4.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.lineEdit.setStyleSheet("QLineEdit { background-color: rgb(255, 255, 255);}")
            self.save_btn.setEnabled(True)
            self.comboBox.setEnabled(True)

        else:
            self.change_pages()
            self.plainTextEdit.setReadOnly(True)
            self.plainTextEdit_2.setReadOnly(True)
            self.plainTextEdit_3.setReadOnly(True)
            self.plainTextEdit_4.setReadOnly(True)
            self.lineEdit.setReadOnly(True)
            self.plainTextEdit.setStyleSheet("background-color: rgb(255, 250, 225);")
            self.plainTextEdit_2.setStyleSheet("background-color: rgb(255, 250, 225);")
            self.plainTextEdit_3.setStyleSheet("background-color: rgb(255, 250, 225);")
            self.plainTextEdit_4.setStyleSheet("background-color: rgb(255, 250, 225);")
            self.lineEdit.setStyleSheet("QLineEdit { background-color: rgb(255, 250, 225);}")
            self.plainTextEdit.setPlainText(self.edit_result[2])
            self.plainTextEdit_2.setPlainText(self.edit_result[3])
            self.plainTextEdit_3.setPlainText(self.edit_result[4])
            self.plainTextEdit_4.setPlainText(self.edit_result[5])
            self.lineEdit.setText(self.edit_result[6])
            self.lbl_qid.setText(str(self.edit_result[0]))
            self.lbl_writer_name.setText(str(self.edit_result[1]))
            self.lbl_data_date.setText(str(self.edit_result[7]))
            self.comboBox.setCurrentText(self.edit_result[8])
            self.save_btn.setEnabled(False)
            self.comboBox.setEnabled(False)

    @pyqtSlot()
    def last_data(self):
        db.last_data()
        # self.t_last=True
        print(db.result_edit)
        if db.result_edit:
            self.tlb_next.setEnabled(False)
            self.tlb_previous.setEnabled(True)
            self.edit_result = []
            for i in db.result_edit:
                for j in i:
                    self.edit_result.append(j)
            if db.result_edit and db.username == self.edit_result[1]:

                self.plainTextEdit.setPlainText(self.edit_result[2])
                self.plainTextEdit_2.setPlainText(self.edit_result[3])
                self.plainTextEdit_3.setPlainText(self.edit_result[4])
                self.plainTextEdit_4.setPlainText(self.edit_result[5])
                self.lineEdit.setText(self.edit_result[6])
                self.lbl_qid.setText(str(self.edit_result[0]))
                self.lbl_writer_name.setText(str(self.edit_result[1]))
                self.lbl_data_date.setText(str(self.edit_result[7]))
                self.comboBox.setCurrentText(self.edit_result[8])
                self.plainTextEdit.setReadOnly(False)
                self.plainTextEdit_2.setReadOnly(False)
                self.plainTextEdit_3.setReadOnly(False)
                self.plainTextEdit_4.setReadOnly(False)
                self.lineEdit.setReadOnly(False)
                self.plainTextEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
                self.plainTextEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
                self.plainTextEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);")
                self.plainTextEdit_4.setStyleSheet("background-color: rgb(255, 255, 255);")
                self.lineEdit.setStyleSheet("QLineEdit { background-color: rgb(255, 255, 255);}")
                self.save_btn.setEnabled(True)
                self.comboBox.setEnabled(True)


            else:
                self.plainTextEdit.setReadOnly(True)
                self.plainTextEdit_2.setReadOnly(True)
                self.plainTextEdit_3.setReadOnly(True)
                self.plainTextEdit_4.setReadOnly(True)
                self.lineEdit.setReadOnly(True)
                self.plainTextEdit.setStyleSheet("background-color: rgb(255, 250, 225);")
                self.plainTextEdit_2.setStyleSheet("background-color: rgb(255, 250, 225);")
                self.plainTextEdit_3.setStyleSheet("background-color: rgb(255, 250, 225);")
                self.plainTextEdit_4.setStyleSheet("background-color: rgb(255, 250, 225);")
                self.lineEdit.setStyleSheet("QLineEdit { background-color: rgb(255, 250, 225);}")
                self.plainTextEdit.setPlainText(self.edit_result[2])
                self.plainTextEdit_2.setPlainText(self.edit_result[3])
                self.plainTextEdit_3.setPlainText(self.edit_result[4])
                self.plainTextEdit_4.setPlainText(self.edit_result[5])
                self.lineEdit.setText(self.edit_result[6])
                self.lbl_qid.setText(str(self.edit_result[0]))
                self.lbl_writer_name.setText(str(self.edit_result[1]))
                self.lbl_data_date.setText(str(self.edit_result[7]))
                self.comboBox.setCurrentText(self.edit_result[8])
                self.save_btn.setEnabled(False)
                self.comboBox.setEnabled(False)


    @pyqtSlot()
    def first_data(self):
        db.first_data()
        self.t_first = True
        print(db.result_edit)
        if db.result_edit:
            self.tlb_previous.setEnabled(False)
            self.tlb_next.setEnabled(True)
            self.edit_result = []
            for i in db.result_edit:
                for j in i:
                    self.edit_result.append(j)
            if db.result_edit and db.username == self.edit_result[1]:

                self.plainTextEdit.setPlainText(self.edit_result[2])
                self.plainTextEdit_2.setPlainText(self.edit_result[3])
                self.plainTextEdit_3.setPlainText(self.edit_result[4])
                self.plainTextEdit_4.setPlainText(self.edit_result[5])
                self.lineEdit.setText(self.edit_result[6])
                self.lbl_qid.setText(str(self.edit_result[0]))
                self.lbl_writer_name.setText(str(self.edit_result[1]))
                self.lbl_data_date.setText(str(self.edit_result[7]))
                self.plainTextEdit.setReadOnly(False)
                self.plainTextEdit_2.setReadOnly(False)
                self.plainTextEdit_3.setReadOnly(False)
                self.plainTextEdit_4.setReadOnly(False)
                self.lineEdit.setReadOnly(False)
                self.plainTextEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
                self.plainTextEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
                self.plainTextEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);")
                self.plainTextEdit_4.setStyleSheet("background-color: rgb(255, 255, 255);")
                self.lineEdit.setStyleSheet("QLineEdit { background-color: rgb(255, 255, 255);}")
                self.save_btn.setEnabled(True)
                self.comboBox.setEnabled(True)


            else:

                self.plainTextEdit.setReadOnly(True)
                self.plainTextEdit_2.setReadOnly(True)
                self.plainTextEdit_3.setReadOnly(True)
                self.plainTextEdit_4.setReadOnly(True)
                self.lineEdit.setReadOnly(True)
                self.plainTextEdit.setStyleSheet("background-color: rgb(255, 250, 225);")
                self.plainTextEdit_2.setStyleSheet("background-color: rgb(255, 250, 225);")
                self.plainTextEdit_3.setStyleSheet("background-color: rgb(255, 250, 225);")
                self.plainTextEdit_4.setStyleSheet("background-color: rgb(255, 250, 225);")
                self.lineEdit.setStyleSheet("QLineEdit { background-color: rgb(255, 250, 225);}")
                self.plainTextEdit.setPlainText(self.edit_result[2])
                self.plainTextEdit_2.setPlainText(self.edit_result[3])
                self.plainTextEdit_3.setPlainText(self.edit_result[4])
                self.plainTextEdit_4.setPlainText(self.edit_result[5])
                self.lineEdit.setText(self.edit_result[6])
                self.lbl_qid.setText(str(self.edit_result[0]))
                self.lbl_writer_name.setText(str(self.edit_result[1]))
                self.lbl_data_date.setText(str(self.edit_result[7]))
                self.save_btn.setEnabled(False)
                self.comboBox.setEnabled(False)


    @pyqtSlot()
    def previous_data(self):

        if self.edit_result[0]:

            db.previous_data(self.edit_result[0])

            if db.result_edit and not db.previous_result:

                # self.tlb_previous.setEnabled(True)
                print(db.result_edit)
                print(db.previous_result)
                self.tlb_next.setEnabled(True)
                self.tlb_pre = True
                self.edit_data()
                self.change_pages()

            else:
                self.statusBar.showMessage("دیتای دیگری وجود ندارد.", 3000)
                self.statusBar.setStyleSheet("QStatusBar{background:red;}")
                self.tlb_previous.setEnabled(False)
                time.sleep(3)
                self.statusBar.setStyleSheet("QStatusBar{background:#eeeeee;}")  # self.timer.stop()





    @pyqtSlot()
    def next_data(self):
        # current_id = self.lbl_qid.text()
        if self.edit_result[0]:
            # current_id=int(current_id)
            db.next_data(self.edit_result[0])

            if db.result_edit and not db.next_reslt:
                print(db.result_edit)

                self.tlb_previous.setEnabled(True)
                self.tlb_nex = True
                self.edit_data()
                self.change_pages()

            else:

                self.statusBar.showMessage("دیتای دیگری وجود ندارد.", 3000)
                self.statusBar.setStyleSheet("QStatusBar{background:red;}")
                self.tlb_next.setEnabled(False)
                time.sleep(3)
                self.statusBar.setStyleSheet("QStatusBar{background:#eeeeee;}")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName("سیستم جامع")
    app.setStyle('Fusion')
    login_window = Login()
    db = Database()

    sys.exit(app.exec_())
