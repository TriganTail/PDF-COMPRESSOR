 # PDF HELPER (сжатие)

 ## Русский

 ### Инструкция по установке
 
 1. Установите необходимые библиотеки:
    ```sh
    pip install PyQt5 PyPDF2 Pillow img2pdf pymupdf
    ```

 2. Скачайте и сохраните файл `PDF HELPER (сжатие).py` на ваш компьютер.

 3. Запустите файл с помощью Python:
    ```sh
    python PDF\ HELPER\ \(сжатие\).py
    ```

 ### Принцип работы кода и про разные режимы работы

 Программа предоставляет графический интерфейс для сжатия PDF файлов. Вы можете добавить один PDF файл или все PDF файлы из папки для сжатия. 

 Существует два режима работы:
 1. **Обычное сжатие PDF** - Используется метод сжатия содержимого потоков страниц PDF.
 2. **Сжатие PDF как изображения** - Конвертирует страницы PDF в изображения, сжимает их, а затем создаёт новый PDF из сжатых изображений. Этот режим включается галочкой "Сжимать PDF как изображения".

 ### Где можно менять качество изображения в коде

 В коде, в функции `compress_pdf_as_images`, вы можете изменить значение параметра `quality` в строке:
 ```python
 img.save(img_byte_array, format='JPEG', quality=60)  # Качество 60, можно настроить
 ```
 Значение `quality` можно установить от 1 до 100, где 100 - наилучшее качество изображения.

 ### Полезная информация

 - Программа использует библиотеку `PyMuPDF` (fitz) для конвертации страниц PDF в изображения, что исключает необходимость установки дополнительных системных приложений.
 - Для корректной работы программы убедитесь, что пути к файлам и папкам указаны правильно.
 - Если у вас возникли проблемы или ошибки при работе программы, проверьте консоль для получения дополнительной информации о проблеме.

 ## English

 ### Installation Instructions

 1. Install the required libraries:
    ```sh
    pip install PyQt5 PyPDF2 Pillow img2pdf pymupdf
    ```

 2. Download and save the `PDF HELPER (compression).py` file to your computer.

 3. Run the file using Python:
    ```sh
    python PDF\ HELPER\ \(compression\).py
    ```

 ### How the Code Works and Modes of Operation

 The program provides a graphical interface for compressing PDF files. You can add a single PDF file or all PDF files from a folder for compression.

 There are two modes of operation:
 1. **Regular PDF Compression** - Uses the method of compressing the content streams of PDF pages.
 2. **Compress PDF as Images** - Converts PDF pages to images, compresses them, and then creates a new PDF from the compressed images. This mode is enabled by checking the "Compress PDF as images" checkbox.

 ### Where to Change Image Quality in the Code

 In the code, in the `compress_pdf_as_images` function, you can change the value of the `quality` parameter in the line:
 ```python
 img.save(img_byte_array, format='JPEG', quality=60)  # Quality 60, can be adjusted
 ```
 The `quality` value can be set from 1 to 100, where 100 is the best image quality.

 ### Useful Information

 - The program uses the `PyMuPDF` (fitz) library to convert PDF pages to images, eliminating the need for additional system applications.
 - Ensure that file and folder paths are correctly specified for the program to work properly.
 - If you encounter problems or errors while running the program, check the console for additional information about the issue.
