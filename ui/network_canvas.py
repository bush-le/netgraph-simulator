import sys
import networkx as nx
import matplotlib.pyplot as plt
# THÊM IMPORT NÀY ĐỂ TẠO VIỀN CHỮ
import matplotlib.patheffects as path_effects
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QWidget, QVBoxLayout

# --- CẤU HÌNH HÌNH DÁNG (MATPLOTLIB MARKERS) ---
SHAPE_MAP = {
    'Router': 'D', 
    'Switch': 's',  
    'Server': '^',  
    'PC': 'o',      
}

class NetworkCanvas(QWidget):
    """
    Widget vẽ đồ thị sử dụng Matplotlib Shapes với chữ được tối ưu hiển thị.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 1. Matplotlib Init (Cyberpunk Style)
        self.figure = Figure(figsize=(8, 6), dpi=100, facecolor='#050505')
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#050505')
        self.ax.axis('off')

        # 2. Canvas Widget
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.current_G = None
        self.current_pos = None

    def draw_network(self, G):
        """Vẽ mạng và phân loại hình dáng theo thiết bị."""
        try:
            self.ax.clear()
            self.ax.axis('off')
            self.current_G = G

            if G is None or G.number_of_nodes() == 0:
                self.canvas.draw()
                return

            # 1. Layout
            self.current_pos = nx.spring_layout(G, seed=42, k=0.5, iterations=50)
            pos = self.current_pos

            # --- LAYER 1: DÂY CÁP (EDGES) - ZORDER=1 ---
            edge_colors = []
            edge_widths = []
            for u, v, d in G.edges(data=True):
                # Ưu tiên 1: Nếu cạnh có thuộc tính 'color' đặc biệt (ví dụ: bị nhiễm virus)
                if d.get('color'):
                    edge_colors.append(d.get('color'))
                    # Nếu là màu đỏ virus, vẽ dày hơn
                    edge_widths.append(3.0 if d.get('color') == '#FF0000' else 1.5)
                # Ưu tiên 2: Cáp quang (Fiber)
                elif d.get('type') == 'Fiber':
                    edge_colors.append('#00FFFF') # Cyan Neon
                    edge_widths.append(2.0)
                # Mặc định: Cáp thường
                else:
                    edge_colors.append('#555555') # Xám tối
                    edge_widths.append(1.0)

            edge_styles = [d.get('style', 'solid') for u,v,d in G.edges(data=True)]

            nx.draw_networkx_edges(G, pos, ax=self.ax, 
                                   edge_color=edge_colors, 
                                   width=edge_widths,
                                   style=edge_styles,
                                   alpha=0.8)

            # --- LAYER 2: THIẾT BỊ (NODES) - ZORDER=2 ---
            node_groups = {}
            for node, data in G.nodes(data=True):
                n_type = data.get('type', 'PC')
                if n_type not in node_groups: node_groups[n_type] = []
                node_groups[n_type].append(node)
            
            for n_type, nodes_in_group in node_groups.items():
                shape = SHAPE_MAP.get(n_type, 'o')
                colors = [G.nodes[n].get('color', '#FFFFFF') for n in nodes_in_group]
                sizes = [G.nodes[n].get('size', 300) for n in nodes_in_group]
                
                nx.draw_networkx_nodes(G, pos, ax=self.ax,
                                       nodelist=nodes_in_group,
                                       node_shape=shape,
                                       node_color=colors,
                                       node_size=sizes,
                                       edgecolors='#FFFFFF',
                                       linewidths=1.5)

            # --- LAYER 3: NHÃN (LABELS) - ZORDER=3 ---
            # Dịch nhãn xuống một chút nữa (từ 0.08 thành 0.1) để tách khỏi node
            label_pos = {k: (v[0], v[1] - 0.1) for k, v in pos.items()}
            
            # Vẽ nhãn và lấy lại đối tượng text
            text_items = nx.draw_networkx_labels(G, label_pos, ax=self.ax,
                                                 font_size=9,         # Tăng size chữ lên xíu
                                                 font_color='white', 
                                                 font_weight='bold',  # Chữ đậm hơn
                                                 font_family='sans-serif')
            
            # TẠO HIỆU ỨNG VIỀN ĐEN (HALO) CHO CHỮ
            for _, text_obj in text_items.items():
                text_obj.set_path_effects([path_effects.withStroke(linewidth=2, foreground='black')])

            self.canvas.draw()
            
        except Exception as e:
            print(f"Drawing Error: {e}")
            import traceback
            traceback.print_exc()

    def highlight_path(self, path_nodes):
        """Highlight đường đi."""
        if not self.current_G or not path_nodes or not self.current_pos: return
        pos = self.current_pos

        # Highlight Edges
        path_edges = list(zip(path_nodes, path_nodes[1:]))
        nx.draw_networkx_edges(self.current_G, pos, ax=self.ax,
                               edgelist=path_edges, edge_color='#FF00FF', width=3.0, alpha=1.0)
        
        # Highlight Nodes
        for node in path_nodes:
            node_data = self.current_G.nodes[node]
            n_type = node_data.get('type', 'PC')
            shape = SHAPE_MAP.get(n_type, 'o')
            size = node_data.get('size', 300)

            nx.draw_networkx_nodes(self.current_G, pos, ax=self.ax,
                                   nodelist=[node],
                                   node_shape=shape,
                                   node_color='#FF00FF',
                                   node_size=size + 150,
                                   edgecolors='#FFFFFF',
                                   linewidths=2.0)
        self.canvas.draw()