import sys
from PyQt5.QtWidgets import * #QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QMessageBox, QHBoxLayout, QScrollArea
from PyQt5.QtGui import QIcon

from PyPDF2 import PdfMerger

class SelectedFileWidget(QWidget):
    def __init__(self, parent_app, file_path):
        super().__init__(parent_app)
        self.file_path = file_path
        self.parent_app = parent_app
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        file_label = QLabel(self.file_path)
        layout.addWidget(file_label)
        self.setLayout(layout)

class PdfMergerApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PDF Merger")

        icon_path = "icon.ico" # 아이콘 설정
        self.setWindowIcon(QIcon(icon_path))

        self.selected_files = []  # 선택된 PDF 파일 위젯을 저장하는 리스트
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.btn_save_folder = QPushButton("Select Save Folder")
        self.btn_save_folder.clicked.connect(self.select_save_folder)
        layout.addWidget(self.btn_save_folder)

        self.save_folder_label = QLabel()  # 폴더 선택한 경로를 표시할 레이블
        layout.addWidget(self.save_folder_label)

        self.file_list_label = QLabel()
        self.file_list_label.hide()  # 초기에는 파일 목록 숨김
        layout.addWidget(self.file_list_label)

        self.btn_select_files = QPushButton("Select PDF Files")
        self.btn_select_files.clicked.connect(self.select_files)
        layout.addWidget(self.btn_select_files)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        layout.addWidget(self.scrollArea)

        self.btn_merge = QPushButton("Merge PDFs")
        self.btn_merge.setEnabled(False)  # 초기에 비활성화 상태로 설정
        self.btn_merge.clicked.connect(self.merge_pdfs)
        layout.addWidget(self.btn_merge)

        self.setLayout(layout)

    def select_save_folder(self):
        self.save_folder = QFileDialog.getExistingDirectory(self, "Select Save Folder")
        if self.save_folder:
            self.save_folder_label.setText("Save folder: " + self.save_folder)  # 선택한 폴더 경로를 표시
            self.btn_select_files.setEnabled(True)  # 저장 폴더 선택 후에는 파일 선택 버튼 활성화

    def select_files(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        files = file_dialog.getOpenFileNames(self, "Select PDF Files", "", "PDF Files (*.pdf)")[0]
        if files:
        # 선택한 파일들을 위젯으로 만들어서 스크롤 영역에 추가
            for file_path in files:
                file_widget = SelectedFileWidget(parent_app=self, file_path=file_path)  # 부모 위젯으로 self를 전달
                self.selected_files.append(file_widget)
                self.scrollAreaLayout.addWidget(file_widget)
            self.file_list_label.show()  # 파일 목록 표시
            self.btn_merge.setEnabled(True)  # 파일 선택 후에는 병합 버튼을 활성화
        else:
            self.btn_merge.setEnabled(False)  # 파일이 선택되지 않은 경우에는 병합 버튼 비활성화

    def merge_pdfs(self):
        if self.selected_files and self.save_folder:
            output_file = self.save_folder + "/merged.pdf"
            merger = PdfMerger()
            try:
                for file_widget in self.selected_files:
                    merger.append(file_widget.file_path)
                merger.write(output_file)
                merger.close()
                self.show_success_message()
            except Exception as e:
                QMessageBox.critical(self, "Error", "An error occurred during merging: " + str(e))

    def show_success_message(self):
        QMessageBox.information(self, "Merge Complete", "병합이 완료되었습니다!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon_path = "icon.ico"
    app.setWindowIcon(QIcon(icon_path))
    window = PdfMergerApp()
    window.show()
    sys.exit(app.exec_())
