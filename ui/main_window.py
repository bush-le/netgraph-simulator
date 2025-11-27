from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame, QMessageBox, QComboBox, 
                             QGroupBox, QFileDialog, QMenuBar, QMenu, QTextEdit, QScrollArea)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QTimer

# Import Views
from ui.network_canvas import NetworkCanvas
from ui.dialogs import AuditReportDialog

# Import Models & Utils
from utils.network_data import NetworkGenerator
from utils.file_io import FileManager
from utils.report_gen import ReportGenerator

# Import Algorithms (Core & Academic)
from algorithms.routing import RoutingManager
from algorithms.traversal import VirusSimulator
from algorithms.throughput import BandwidthAnalyzer
from algorithms.auditing import NetworkAuditor
from algorithms.stp import STPManager
from algorithms.graph_theory import GraphTheoryManager # <--- NEW IMPORT

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- 1. CONFIGURATION ---
        self.setWindowTitle("NetGraph Sentinel - Phiên Bản Tối Thượng (Đa Cấu Trúc)") # Đã Việt hóa
        self.resize(1366, 768)
        
        # Cyberpunk Stylesheet (Full Fix)
        self.setStyleSheet("""
            QMainWindow { background-color: #050505; }
            QLabel { color: #00FF00; font-family: 'Consolas'; font-size: 12px; font-weight: bold; }
            QGroupBox { 
                border: 1px solid #333; margin-top: 10px; color: #00FFFF; font-weight: bold; padding-top: 15px;
            }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; background-color: #050505; }
            QPushButton {
                background-color: #1a1a1a; color: #E0E0E0; border: 1px solid #555;
                padding: 6px; font-weight: bold; border-radius: 4px;
            }
            QPushButton:hover { background-color: #333; color: #FFF; border-color: #FFF; }
            
            QComboBox { 
                background-color: #111; color: #00FF00; border: 1px solid #555; padding: 5px; 
            }
            QComboBox::drop-down { border: 0px; }
            QComboBox QAbstractItemView {
                background-color: #050505; color: #FFFFFF; border: 1px solid #333;
                selection-background-color: #003300; selection-color: #00FF00;
            }
            QFrame { border: none; }
        """)

        # --- 2. LOGIC INITIALIZATION ---
        self.generator = NetworkGenerator()
        
        # Core Algorithms
        self.router_logic = RoutingManager()
        self.virus_logic = VirusSimulator()
        self.bandwidth_logic = BandwidthAnalyzer()
        self.auditor_logic = NetworkAuditor()
        self.stp_logic = STPManager()
        
        # Academic Algorithms (NEW)
        self.acad_logic = GraphTheoryManager()

        self.current_graph = None 
        
        # Animation State
        self.simulation_timer = QTimer()
        self.simulation_timer.timeout.connect(self.run_simulation_step)
        self.infection_steps = []
        self.current_step_index = 0
        self.infected_history = set() # <--- THÊM DÒNG NÀY

        # --- 3. UI INITIALIZATION ---
        self._create_menu_bar()
        self._init_layout()
        
        # Start
        self.on_generate_network()

    def _create_menu_bar(self):
        """Tạo thanh Menu phía trên."""
        menu_bar = self.menuBar()
        # Style cho MenuBar để đồng bộ Cyberpunk
        menu_bar.setStyleSheet("""
            QMenuBar { background-color: #111; color: #FFF; border-bottom: 1px solid #333; font-weight: bold; }
            QMenuBar::item { padding: 8px 15px; background-color: transparent; }
            QMenuBar::item:selected { background-color: #00FF00; color: #000; }
            QMenu { background-color: #111; color: #FFF; border: 1px solid #555; }
            QMenu::item { padding: 8px 20px; }
            QMenu::item:selected { background-color: #333; color: #00FF00; border-left: 2px solid #00FF00; }
        """)

        # === 1. File Menu ===
        file_menu = menu_bar.addMenu("TỆP TIN") # Đã Việt hóa
        
        action_open = QAction("Mở Sơ Đồ (.json)", self) # Đã Việt hóa
        action_open.setShortcut("Ctrl+O")
        action_open.triggered.connect(self.on_open_file)
        file_menu.addAction(action_open)

        action_save = QAction("Lưu Sơ Đồ (.json)", self) # Đã Việt hóa
        action_save.setShortcut("Ctrl+S")
        action_save.triggered.connect(self.on_save_file)
        file_menu.addAction(action_save)
        
        file_menu.addSeparator()

        action_export = QAction("Xuất Báo Cáo (.txt)", self) # Đã Việt hóa
        action_export.setShortcut("Ctrl+E")
        action_export.triggered.connect(self.on_export_report)
        file_menu.addAction(action_export)
        
        file_menu.addSeparator()
        
        action_exit = QAction("Thoát", self) # Đã Việt hóa
        action_exit.triggered.connect(self.close)
        file_menu.addAction(action_exit)

        # === 2. Academic Menu (NEW - Đáp ứng yêu cầu còn thiếu) ===
        acad_menu = menu_bar.addMenu("CÔNG CỤ HỌC THUẬT") # Đã Việt hóa

        # 4. Duyệt DFS
        action_dfs = QAction("Chạy Duyệt DFS", self) # Đã Việt hóa
        action_dfs.triggered.connect(self.on_run_dfs)
        acad_menu.addAction(action_dfs)

        # 5. Kiểm tra 2 phía
        action_bipartite = QAction("Kiểm tra Đồ thị 2 Phía", self) # Đã Việt hóa
        action_bipartite.triggered.connect(self.on_check_bipartite)
        acad_menu.addAction(action_bipartite)

        # 6. Biểu diễn đồ thị
        action_reps = QAction("Xem Biểu diễn Đồ thị (Ma trận/Danh sách)", self) # Đã Việt hóa
        action_reps.triggered.connect(self.on_view_representations)
        acad_menu.addAction(action_reps)

        acad_menu.addSeparator()

        # 7.4 & 7.5 Euler
        action_euler = QAction("Phân tích Đường đi/Chu trình Euler", self) # Đã Việt hóa
        action_euler.triggered.connect(self.on_find_euler)
        acad_menu.addAction(action_euler)

    def _init_layout(self):
        """Khởi tạo bố cục chính (Đã thêm Thanh Cuộn)."""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        # === TẠO VÙNG CUỘN (SCROLL AREA) CHO CỘT TRÁI ===
        # Giúp giao diện không bị vỡ khi có quá nhiều nút
        scroll_area = QScrollArea()
        scroll_area.setFixedWidth(320) # Tăng nhẹ độ rộng để chứa thanh cuộn
        scroll_area.setWidgetResizable(True)
        # Style cho thanh cuộn để hợp với nền đen
        scroll_area.setStyleSheet("""
            QScrollArea { border: none; background-color: #0A0A0A; }
            QScrollBar:vertical { border: none; background: #111; width: 8px; margin: 0px; }
            QScrollBar::handle:vertical { background: #444; min-height: 20px; border-radius: 4px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

        # Widget chứa nội dung thực sự bên trong vùng cuộn
        control_content_widget = QWidget()
        control_content_widget.setStyleSheet("background-color: #0A0A0A;") 
        
        # Layout dọc cho các nút bấm, sẽ được đặt vào control_content_widget
        panel_layout = QVBoxLayout(control_content_widget)
        panel_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        panel_layout.setContentsMargins(10, 10, 10, 10)

        # Gắn widget chứa nội dung vào vùng cuộn
        scroll_area.setWidget(control_content_widget)

        # --- BẮT ĐẦU THÊM CÁC NÚT VÀO `panel_layout` ---

        # Header
        lbl_title = QLabel("NETGRAPH\nSENTINEL")
        lbl_title.setStyleSheet("font-size: 24px; color: #FF00FF; font-weight: bold; margin-bottom: 5px;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        panel_layout.addWidget(lbl_title)

        # Group 1: Topology
        g_topo = QGroupBox("1. ĐIỀU KHIỂN CẤU TRÚC") # Đã Việt hóa
        l_topo = QVBoxLayout()
        l_topo.setSpacing(10)

        # --- THÊM ĐOẠN NÀY ---
        l_topo.addWidget(QLabel("Loại Cấu Trúc:")) # Đã Việt hóa
        self.combo_topology = QComboBox()
        self.combo_topology.addItems([
            "Phân Cấp (Tree)", # Đã Việt hóa
            "Lưới (Random)",   # Đã Việt hóa
            "Hình Sao (Hub-Spoke)", # Đã Việt hóa
            "Vòng Tròn (Loop)" # Đã Việt hóa
        ])
        l_topo.addWidget(self.combo_topology)
        # ---------------------

        self.btn_gen = QPushButton("Khởi Tạo Mạng") # Đã Việt hóa
        self.btn_gen.setStyleSheet("color: #00FFFF; border: 1px solid #00FFFF;")
        self.btn_gen.clicked.connect(self.on_generate_network)
        l_topo.addWidget(self.btn_gen)
        
        self.btn_stp = QPushButton("Kích hoạt STP (Chống Vòng Lặp)") # Đã Việt hóa
        self.btn_stp.setStyleSheet("color: #ADFF2F; border: 1px solid #ADFF2F;")
        self.btn_stp.clicked.connect(self.on_run_stp)
        l_topo.addWidget(self.btn_stp)
        
        self.btn_audit = QPushButton("Chạy Kiểm Toán Hệ Thống") # Đã Việt hóa
        self.btn_audit.setStyleSheet("color: #00FF00; border: 1px dashed #00FF00;")
        self.btn_audit.clicked.connect(self.on_run_audit)
        l_topo.addWidget(self.btn_audit)
        
        g_topo.setLayout(l_topo)
        panel_layout.addWidget(g_topo)

        # Group 2: Traffic & Analysis
        g_ops = QGroupBox("2. PHÂN TÍCH LƯU LƯỢNG") # Đã Việt hóa
        l_ops = QVBoxLayout()
        l_ops.setSpacing(10)
        
        l_ops.addWidget(QLabel("Nút Nguồn:")) # Đã Việt hóa
        self.combo_source = QComboBox()
        l_ops.addWidget(self.combo_source)
        
        l_ops.addWidget(QLabel("Nút Đích:")) # Đã Việt hóa
        self.combo_target = QComboBox()
        l_ops.addWidget(self.combo_target)
        
        h_btn_layout = QHBoxLayout()
        self.btn_trace = QPushButton("Dò Đường") # Đã Việt hóa
        self.btn_trace.clicked.connect(self.on_trace_route)
        self.btn_bw = QPushButton("Băng Thông Tối Đa") # Đã Việt hóa
        self.btn_bw.setStyleSheet("color: #FFA500; border: 1px solid #FFA500;")
        self.btn_bw.clicked.connect(self.on_analyze_bandwidth)
        h_btn_layout.addWidget(self.btn_trace)
        h_btn_layout.addWidget(self.btn_bw)
        l_ops.addLayout(h_btn_layout)
        
        g_ops.setLayout(l_ops)
        panel_layout.addWidget(g_ops)

        # Group 3: Security
        g_sec = QGroupBox("3. MÔ PHỎNG MỐI ĐE DỌA") # Đã Việt hóa
        l_sec = QVBoxLayout()
        l_sec.setSpacing(10)
        l_sec.addWidget(QLabel("Bệnh Nhân Số 0:")) # Đã Việt hóa
        self.combo_virus = QComboBox()
        l_sec.addWidget(self.combo_virus)
        
        self.btn_virus = QPushButton("⚠️ THỰC THI TẤN CÔNG VIRUS") # Đã Việt hóa
        self.btn_virus.setStyleSheet("background-color: #330000; color: #FF0000; border: 1px solid #FF0000; font-weight: bold;")
        self.btn_virus.clicked.connect(self.on_simulate_virus)
        l_sec.addWidget(self.btn_virus)
        g_sec.setLayout(l_sec)
        panel_layout.addWidget(g_sec)

        # Status Log
        # Status Log (Dùng QTextEdit để không bị tràn chữ)
        self.lbl_stats = QTextEdit()
        self.lbl_stats.setReadOnly(True) # Chỉ đọc
        self.lbl_stats.setText("Hệ thống sẵn sàng...")
        self.lbl_stats.setFixedHeight(100) # Chiều cao cố định
        # Style cho khung Log
        self.lbl_stats.setStyleSheet("""
            background-color: #0A0A0A; 
            color: #888; 
            font-family: 'Consolas'; 
            font-size: 11px;
            border: 1px solid #333;
            border-radius: 4px;
        """)
        panel_layout.addWidget(self.lbl_stats)

        # === RIGHT PANEL (CANVAS) ===
        self.canvas = NetworkCanvas()
        
        # Thêm Scroll Area (chứa panel trái) và Canvas (panel phải) vào layout chính
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(self.canvas, stretch=1)

    # --- EVENT HANDLERS (CORE) ---

    def on_generate_network(self):
        """Sinh mạng mới dựa trên kiểu được chọn."""
        # Dọn dẹp giao diện trước
        self.reset_visual_state()
        
        # Lấy kiểu tô pô từ ComboBox
        topo_type_text = self.combo_topology.currentText()
        
        # Ánh xạ tên hiển thị sang từ khóa (key) nội bộ
        topo_map = {
            "Phân Cấp (Tree)": "hierarchical", # Đã Việt hóa key map
            "Lưới (Random)": "mesh",           # Đã Việt hóa key map
            "Hình Sao (Hub-Spoke)": "star",    # Đã Việt hóa key map
            "Vòng Tròn (Loop)": "ring"         # Đã Việt hóa key map
        }
        # Lấy key, mặc định là hierarchical nếu không tìm thấy
        topo_key = topo_map.get(topo_type_text, "hierarchical")
        
        # Gọi hàm sinh mạng mới trong NetworkGenerator
        # (Đảm bảo bạn đã cập nhật file utils/network_data.py trước đó)
        self.current_graph = self.generator.generate_network(topo_key)
        
        # Cập nhật giao diện
        self._refresh_ui_data()
        self.lbl_stats.setText(f"Đã khởi tạo mạng ({topo_type_text}). Sẵn sàng chờ lệnh.") # Đã Việt hóa

    def _refresh_ui_data(self):
        """Vẽ lại đồ thị và cập nhật ComboBox."""
        if self.current_graph:
            self.canvas.draw_network(self.current_graph)
            nodes = sorted(list(self.current_graph.nodes()))
            
            # Update Combos without triggering events
            for c in [self.combo_source, self.combo_target, self.combo_virus]:
                c.blockSignals(True)
                c.clear()
                c.addItems(nodes)
                c.blockSignals(False)

    def reset_visual_state(self):
        """Hàm trung tâm để dọn dẹp giao diện về trạng thái mặc định."""
        # Dừng animation virus nếu đang chạy
        if self.simulation_timer.isActive():
            self.simulation_timer.stop()
        
        # Reset trạng thái virus
        self.infection_steps = []
        self.current_step_index = 0
        self.infected_history.clear()
        
        if self.current_graph:
            # Khôi phục màu sắc và kích thước mặc định cho NODE
            for node, data in self.current_graph.nodes(data=True):
                n_type = data.get('type', 'PC')
                # Màu mặc định theo loại
                if n_type == 'PC': color = '#D3D3D3'; size = 250
                elif n_type == 'Switch': color = '#00BFFF'; size = 350
                elif n_type == 'Router': color = '#FF4500'; size = 450
                elif n_type == 'Server': color = '#32CD32'; size = 300 # Thêm Server
                else: color = '#FFFFFF'; size = 300
                
                self.current_graph.nodes[node]['color'] = color
                self.current_graph.nodes[node]['size'] = size
            
            # Khôi phục mặc định cho CẠNH (Edge)
            for u, v, data in self.current_graph.edges(data=True):
                # Xóa màu đặc biệt (virus/highlight)
                if 'color' in data:
                    del data['color'] 
                # Xóa trạng thái STP
                if 'stp_state' in data:
                    del data['stp_state']

            # Vẽ lại đồ thị sạch sẽ (giữ nguyên vị trí)
            self.canvas.draw_network(self.current_graph, keep_layout=True)
            self.lbl_stats.setText("Đã đặt lại trạng thái hiển thị. Sẵn sàng.") # Đã Việt hóa

    def on_trace_route(self):
        self.reset_visual_state() # <--- THÊM DÒNG NÀY
        src, dst = self.combo_source.currentText(), self.combo_target.currentText()
        if src == dst or not src: return
        
        path, lat = self.router_logic.find_shortest_path(self.current_graph, src, dst)
        if path:
            self.canvas.highlight_path(path)
            self.lbl_stats.setText(f"[KẾT QUẢ ĐỊNH TUYẾN]\nĐường đi: {' -> '.join(path)}\nTổng độ trễ: {lat} ms") # Đã Việt hóa
        else:
            QMessageBox.warning(self, "Không thể tới", "Không tìm thấy đường đi giữa các nút đã chọn.") # Đã Việt hóa

    def on_analyze_bandwidth(self):
        self.reset_visual_state() # Dọn dẹp giao diện
        
        src, dst = self.combo_source.currentText(), self.combo_target.currentText()
        
        # Kiểm tra dữ liệu đầu vào
        if src == dst or not src or not dst: 
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn Nút Nguồn và Nút Đích khác nhau.")
            return

        # 1. Tính toán Băng thông tối đa (Logic Toán học)
        max_flow, _ = self.bandwidth_logic.analyze_max_bandwidth(self.current_graph, src, dst)

        # 2. Tìm đường đi ngắn nhất để làm minh họa (Visual)
        # (Chúng ta cần một đường dẫn hợp lệ để vẽ lên bản đồ, tránh lỗi vẽ cạnh không tồn tại)
        path, _ = self.router_logic.find_shortest_path(self.current_graph, src, dst)

        # 3. Vẽ đường minh họa lên Canvas
        if path:
            self.canvas.highlight_path(path)
        
        # 4. Hiển thị kết quả tính toán
        self.lbl_stats.setText(f"[KIỂM TRA BĂNG THÔNG]\nTừ: {src}\nĐến: {dst}\nDung lượng tối đa: {max_flow} Mbps")

    def on_run_stp(self):
        self.reset_visual_state() # <--- THÊM DÒNG NÀY
        active, blocked = self.stp_logic.compute_spanning_tree(self.current_graph)
        
        # Xóa trạng thái STP cũ (nếu có)
        for u, v, d in self.current_graph.edges(data=True):
            d.pop('stp_state', None)

        # Gán trạng thái STP mới vào thuộc tính của cạnh
        for u, v in active:
            self.current_graph[u][v]['stp_state'] = 'forwarding'
        for u, v in blocked:
            self.current_graph[u][v]['stp_state'] = 'blocking'
        
        # Yêu cầu canvas vẽ lại với dữ liệu đồ thị đã được cập nhật
        self.canvas.draw_network(self.current_graph, keep_layout=True)
        self.lbl_stats.setText(f"[CHẾ ĐỘ STP]\nLiên kết Hoạt động: {len(active)}\nLiên kết Bị chặn: {len(blocked)}\nĐã thực thi cấu trúc không vòng lặp.") # Đã Việt hóa

    def on_run_audit(self):
        report = self.auditor_logic.perform_full_audit(self.current_graph)
        dialog = AuditReportDialog(report, self)
        dialog.exec()

    def on_simulate_virus(self):
        self.reset_visual_state() # <--- THÊM DÒNG NÀY
        start_node = self.combo_virus.currentText()
        if not start_node: return
        
        self.infection_steps = self.virus_logic.simulate_spread(self.current_graph, start_node)
        if self.infection_steps:
            self.canvas.draw_network(self.current_graph) # Reset visual
            self.current_step_index = 0
            self.infected_history.clear() # <--- THÊM DÒNG NÀY (Reset lịch sử)
            self.lbl_stats.setText(f"⚠️ PHÁT HIỆN VIRUS TẠI {start_node}!") # Đã Việt hóa
            self.simulation_timer.start(500)

    def run_simulation_step(self):
        """Thực hiện một bước mô phỏng lây lan virus."""
        if self.current_step_index >= len(self.infection_steps):
            self.simulation_timer.stop()
            self.lbl_stats.setText("MẠNG ĐÃ BỊ XÂM NHẬP HOÀN TOÀN. Mô phỏng kết thúc.") # Đã Việt hóa
            return

        newly_infected_nodes = self.infection_steps[self.current_step_index]
        
        # Xử lý cho bước > 0 (Không phải Patient Zero)
        if self.current_step_index > 0:
            # Với mỗi node mới bị nhiễm, tìm xem nó bị lây từ node hàng xóm nào
            for new_node in newly_infected_nodes:
                # Lấy danh sách hàng xóm của node mới nhiễm
                neighbors = list(self.current_graph.neighbors(new_node))
                for neighbor in neighbors:
                    # Nếu hàng xóm này đã nằm trong lịch sử nhiễm trước đó -> Đây là nguồn lây
                    if neighbor in self.infected_history:
                        # Đánh dấu cạnh nối giữa chúng là màu ĐỎ
                        if self.current_graph.has_edge(neighbor, new_node):
                            self.current_graph[neighbor][new_node]['color'] = '#FF0000'

        # Tô màu ĐỎ cho các node mới nhiễm và thêm vào lịch sử
        for node in newly_infected_nodes:
            self.current_graph.nodes[node]['color'] = '#FF0000' # Red
            self.current_graph.nodes[node]['size'] = 600 # Phình to ra
            self.infected_history.add(node) # Ghi nhận đã nhiễm
            
        # Vẽ lại đồ thị với màu sắc mới (cả node và edge)
        self.canvas.draw_network(self.current_graph, keep_layout=True)
        
        nodes_str = ", ".join(newly_infected_nodes)
        self.lbl_stats.setText(f"Bước {self.current_step_index + 1}: Virus đang lây lan sang {nodes_str}...") # Đã Việt hóa
        self.current_step_index += 1

    # --- EVENT HANDLERS (ACADEMIC TOOLS) ---

    def _show_academic_result(self, title, content):
        """Hàm hỗ trợ hiển thị kết quả học thuật bằng Dialog."""
        # Tận dụng AuditReportDialog nhưng thay đổi dữ liệu đầu vào một chút
        # Vì AuditReportDialog mong đợi một dict, ta "hack" nhẹ để nó hiển thị text raw
        dummy_report = {
            "is_connected": False, "connected_components": 0, "critical_links": [], "average_redundancy": 0
        }
        dialog = AuditReportDialog(dummy_report, self)
        dialog.setWindowTitle(title)
        # Ghi đè nội dung text trực tiếp
        dialog.txt_content.setText(content)
        dialog.exec()

    def on_run_dfs(self):
        """Xử lý yêu cầu duyệt DFS."""
        # Lấy nút đang chọn ở Source làm nút bắt đầu DFS
        start_node = self.combo_source.currentText()
        result = self.acad_logic.run_dfs(self.current_graph, start_node)
        self._show_academic_result("Kết quả duyệt DFS", result) # Đã Việt hóa

    def on_check_bipartite(self):
        """Xử lý kiểm tra đồ thị 2 phía."""
        result = self.acad_logic.check_bipartite(self.current_graph)
        self._show_academic_result("Kiểm tra Đồ thị 2 Phía", result) # Đã Việt hóa

    def on_view_representations(self):
        """Xử lý xem các biểu diễn đồ thị."""
        result = self.acad_logic.get_representations(self.current_graph)
        self._show_academic_result("Biểu diễn Đồ thị", result) # Đã Việt hóa

    def on_find_euler(self):
        """Xử lý tìm chu trình Euler."""
        result = self.acad_logic.find_eulerian(self.current_graph)
        self._show_academic_result("Phân tích Đường đi/Chu trình Euler", result) # Đã Việt hóa

    # --- FILE OPERATIONS ---

    def on_save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Lưu Sơ Đồ", "network_config.json", "JSON (*.json)") # Đã Việt hóa
        if file_path:
            ok, msg = FileManager.save_network_to_json(self.current_graph, file_path)
            if ok: self.lbl_stats.setText(f"Đã lưu: {file_path}") # Đã Việt hóa
            else: QMessageBox.critical(self, "Lỗi", msg) # Đã Việt hóa

    def on_open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Mở Sơ Đồ", "", "JSON (*.json)") # Đã Việt hóa
        if file_path:
            G, msg = FileManager.load_network_from_json(file_path)
            if G:
                self.reset_visual_state() # <--- THÊM DÒNG NÀY
                self.current_graph = G
                self._refresh_ui_data()
                self.lbl_stats.setText(f"Đã tải: {file_path}") # Đã Việt hóa
            else:
                QMessageBox.critical(self, "Lỗi", msg) # Đã Việt hóa

    def on_export_report(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Xuất Báo Cáo", "audit_log.txt", "Text (*.txt)") # Đã Việt hóa
        if file_path:
            # Truyền self.current_graph vào hàm get_topology_stats
            stats = self.generator.get_topology_stats(self.current_graph) # <--- SỬA DÒNG NÀY
            audit = self.auditor_logic.perform_full_audit(self.current_graph)
            ok, msg = ReportGenerator.export_summary(self.current_graph, stats, audit, file_path)
            if ok: QMessageBox.information(self, "Thành công", f"Đã xuất báo cáo ra {file_path}") # Đã Việt hóa