from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PyQt6.QtGui import QFont

class AuditReportDialog(QDialog):
    """
    Cửa sổ Pop-up hiển thị báo cáo kiểm toán mạng chi tiết.
    """
    def __init__(self, report_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Network Audit Report - TOP SECRET")
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
        lbl_title = QLabel("/// SYSTEM AUDIT LOG ///")
        layout.addWidget(lbl_title)

        # Content
        self.txt_content = QTextEdit()
        self.txt_content.setReadOnly(True)
        layout.addWidget(self.txt_content)

        # Format nội dung báo cáo
        content = self._format_report(report_data)
        self.txt_content.setText(content)

        # Close Button
        btn_close = QPushButton("ACKNOWLEDGE")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)

    def _format_report(self, data):
        """Chuyển đổi dữ liệu dict thành text định dạng kiểu Hacker."""
        status = "SECURE" if data["is_connected"] and not data["critical_links"] else "VULNERABLE"
        
        bridges_text = ""
        if data["critical_links"]:
            bridges_text = "\n[CRITICAL WARNING] SINGLE POINTS OF FAILURE DETECTED:\n"
            for u, v in data["critical_links"]:
                bridges_text += f"  (!) LINK {u} <--> {v}\n"
        else:
            bridges_text = "\n[OK] No critical single points of failure detected.\n"

        return (
            f"========================================\n"
            f"NETWORK HEALTH STATUS: [{status}]\n"
            f"========================================\n\n"
            f"[-] CONNECTIVITY CHECK:\n"
            f"    Fully Connected: {str(data['is_connected']).upper()}\n"
            f"    Partitions:      {data['connected_components']}\n"
            f"\n[-] RESILIENCE METRICS:\n"
            f"    Avg Connections: {data['average_redundancy']:.2f} links/device\n"
            f"{bridges_text}\n"
            f"========================================\n"
            f"RECOMMENDATION:\n"
            f"{'Add redundant links.' if not data['is_connected'] or data['critical_links'] else 'Network is stable.'}"
        )