import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    """
    Entry Point của ứng dụng NetGraph Sentinel.
    """
    # 1. Khởi tạo ứng dụng Qt
    app = QApplication(sys.argv)

    # 2. Khởi tạo cửa sổ chính
    window = MainWindow()
    window.show()

    # 3. Chạy vòng lặp sự kiện (Event Loop)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()