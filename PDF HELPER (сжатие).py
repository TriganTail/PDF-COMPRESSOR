import os
import sys
import threading
from PyQt5 import QtWidgets, QtCore
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import io
import img2pdf
from pdf2image import convert_from_path
import fitz

class PDFCompressor(QtWidgets.QWidget):
    showDialog = QtCore.pyqtSignal(str)
    logSignal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.showDialog.connect(self.handleDialog)
        self.logSignal.connect(self.log)

    def initUI(self):
        vbox = QtWidgets.QVBoxLayout()
        hbox1 = QtWidgets.QHBoxLayout()
        hbox2 = QtWidgets.QHBoxLayout()
        hbox4 = QtWidgets.QHBoxLayout()

        self.btn_add_file = QtWidgets.QPushButton('Добавить 1 файл PDF')
        self.btn_add_folder = QtWidgets.QPushButton('Добавить все файлы из папки')
        self.path_box = QtWidgets.QLineEdit()
        self.path_box.setPlaceholderText('Путь к сохранению...')
        self.btn_change_path = QtWidgets.QPushButton('Изменить путь сохранения')
        self.table = QtWidgets.QTableWidget(0, 1)
        self.table.setHorizontalHeaderLabels(['Файлы для сжатия'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.console = QtWidgets.QTextEdit()
        self.console.setReadOnly(True)
        self.btn_start = QtWidgets.QPushButton('Начать сжатие')
        self.checkbox_images = QtWidgets.QCheckBox('Сжимать PDF как изображения')

        hbox1.addWidget(self.btn_add_file)
        hbox1.addWidget(self.btn_add_folder)
        hbox2.addWidget(self.path_box)
        hbox2.addWidget(self.btn_change_path)
        hbox4.addWidget(self.checkbox_images)
        hbox4.addWidget(self.btn_start)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.table)
        vbox.addWidget(self.console)
        vbox.addLayout(hbox4)

        self.setLayout(vbox)

        self.btn_add_file.clicked.connect(self.addFile)
        self.btn_add_folder.clicked.connect(self.addFolder)
        self.btn_change_path.clicked.connect(self.changeSavePath)
        self.btn_start.clicked.connect(self.startCompression)

        self.files_to_compress = []

        self.setWindowTitle('PDF HELPER (сжатие)')
        self.setGeometry(300, 300, 800, 600)

    def addFile(self):
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите PDF файл", "", "PDF Files (*.pdf)", options=options)
        if file_path:
            self.files_to_compress.append(file_path)
            self.updateTable()

    def addFolder(self):
        options = QtWidgets.QFileDialog.Options()
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку", "", options=options)
        if folder_path:
            for filename in os.listdir(folder_path):
                if filename.endswith('.pdf'):
                    self.files_to_compress.append(os.path.join(folder_path, filename))
            self.updateTable()

    def changeSavePath(self):
        options = QtWidgets.QFileDialog.Options()
        save_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения", "", options=options)
        if save_path:
            self.path_box.setText(save_path)

    def updateTable(self):
        self.table.setRowCount(0)
        for file in self.files_to_compress:
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)
            self.table.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(file))

    def log(self, message):
        self.console.append(message)

    def startCompression(self):
        self.console.clear()
        save_path = self.path_box.text()
        if not save_path:
            self.log("Ошибка: Пожалуйста, укажите путь для сохранения.")
            return

        self.compression_thread = threading.Thread(target=self.compressFiles, args=(save_path,))
        self.compression_thread.start()

    def compressFiles(self, save_path):
        for file_path in self.files_to_compress:
            try:
                filename = os.path.basename(file_path)
                new_file_path = os.path.join(save_path, f"{filename}")
                self.logSignal.emit(f"Начало сжатия: {file_path}")

                if self.checkbox_images.isChecked():
                    self.compress_pdf_as_images(file_path, new_file_path)
                else:
                    self.compress_pdf(file_path, new_file_path)
            except Exception as e:
                self.logSignal.emit(f"Ошибка при сжатии {file_path}: {str(e)}")

        self.showDialog.emit(save_path)

    def compress_pdf_as_images(self, input_path, output_path):
        try:
            pdf_document = fitz.open(input_path)

            compressed_images = []
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                pix = page.get_pixmap(dpi=200)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                img_byte_array = io.BytesIO()
                img.save(img_byte_array, format='JPEG', quality=80)
                compressed_images.append(img_byte_array.getvalue())

            with open(output_path, "wb") as f:
                f.write(img2pdf.convert(compressed_images))

            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            compression_ratio = (1 - compressed_size / original_size) * 100

            self.logSignal.emit(f"Исходный размер: {original_size / 1024:.2f} КБ")
            self.logSignal.emit(f"Сжатый размер: {compressed_size / 1024:.2f} КБ")
            self.logSignal.emit(f"Степень сжатия: {compression_ratio:.2f}%")

        except Exception as e:
            self.logSignal.emit(f"Ошибка при сжатии PDF как изображения: {str(e)}")

    def compress_pdf(self, input_path, output_path):
        try:
            reader = PdfReader(input_path)
            writer = PdfWriter()

            for page in reader.pages:
                page.compress_content_streams()
                writer.add_page(page)

            with open(output_path, 'wb') as f:
                writer.write(f)

            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            compression_ratio = (1 - compressed_size / original_size) * 100

            self.logSignal.emit(f"Исходный размер: {original_size / 1024:.2f} КБ")
            self.logSignal.emit(f"Сжатый размер: {compressed_size / 1024:.2f} КБ")
            self.logSignal.emit(f"Степень сжатия: {compression_ratio:.2f}%")

        except Exception as e:
            self.logSignal.emit(f"Ошибка при сжатии PDF: {str(e)}")

    @QtCore.pyqtSlot(str)
    def handleDialog(self, save_path):
        reply = QtWidgets.QMessageBox.question(self, 'Сообщение', "Хотите открыть папку с сжатыми файлами?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            os.startfile(save_path)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = PDFCompressor()
    ex.show()
    sys.exit(app.exec_())
