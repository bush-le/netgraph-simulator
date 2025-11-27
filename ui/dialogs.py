from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PyQt6.QtGui import QFont

class AuditReportDialog(QDialog):
    """
    Cửa sổ Pop-up hiển thị báo cáo kiểm toán mạng chi tiết.
    """
    def __init__(self, report_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Báo Cáo Kiểm Toán Mạng - BẢO MẬT")
        self.resize(500, 400)
        self.setStyleSheet("""
            QDialog { background-color: #0A0A0A; border: 1px solid #00FF00; }
            QLabel { color: #00FF00; font-weight: bold; font-size: 16px; }
            QTextEdit { background-color: #111; color: #00FF00; font-family: 'Consolas'; font-size: 12px; border: none; }
            QPushButton { background-color: #003300; color: #00FF00; border: 1px solid #00FF00; padding: 10px; }
            QPushButton:hover { background-color: #00FF00; color: #000000; }
        """)

        layout = QVBoxLayout(self)

        # Header
        lbl_title = QLabel("/// NHẬT KÝ KIỂM TOÁN HỆ THỐNG ///")
        layout.addWidget(lbl_title)

        # Content
        self.txt_content = QTextEdit()
        self.txt_content.setReadOnly(True)
        layout.addWidget(self.txt_content)

        # Format nội dung báo cáo
        content = self._format_report(report_data)
        self.txt_content.setText(content)

        # Close Button
        btn_close = QPushButton("ĐÃ HIỂU")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)

    def _format_report(self, data):
        """Chuyển đổi dữ liệu dict thành text định dạng kiểu Hacker."""
        status = "AN TOÀN" if data["is_connected"] and not data["critical_links"] else "CÓ LỖ HỔNG"
        
        bridges_text = ""
        if data["critical_links"]:
            bridges_text = "\n[CẢNH BÁO NGHIÊM TRỌNG] PHÁT HIỆN CÁC ĐIỂM YẾU CHÍ MẠNG (CẦU):\n"
            for u, v in data["critical_links"]:
                bridges_text += f"  (!) LIÊN KẾT {u} <--> {v}\n"
        else:
            bridges_text = "\n[OK] Không phát hiện điểm yếu đơn lẻ (cầu) nào.\n"

        return (
            f"========================================\n"
            f"TRẠNG THÁI AN TOÀN MẠNG: [{status}]\n"
            f"========================================\n\n"
            f"[-] KIỂM TRA TÍNH LIÊN THÔNG:\n"
            f"    Liên thông hoàn toàn: {str(data['is_connected']).upper()}\n"
            f"    Số phân mảnh mạng:    {data['connected_components']}\n"
            f"\n[-] CHỈ SỐ PHỤC HỒI (RESILIENCE):\n"
            f"    Kết nối trung bình: {data['average_redundancy']:.2f} liên kết/thiết bị\n"
            f"{bridges_text}\n"
            f"========================================\n"
            f"KHUYẾN NGHỊ:\n"
            f"{'Cần thêm các liên kết dự phòng để tăng độ tin cậy.' if not data['is_connected'] or data['critical_links'] else 'Mạng đang hoạt động ổn định.'}"
        )