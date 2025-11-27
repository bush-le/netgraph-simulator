import sys
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
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
    Widget vẽ đồ thị với Cyberpunk style clean và tối ưu hiển thị.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # 1. Matplotlib Init (Clean Cyberpunk Style)
        self.figure = Figure(figsize=(8, 6), dpi=100, facecolor='#0a0a0a')
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor('#0a0a0a')
        self.ax.axis('off')
        
        # Tắt margins để tối đa không gian
        self.figure.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)

        # 2. Canvas Widget
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.current_G = None
        self.current_pos = None
        self.highlight_artists = []

    def draw_network(self, G, keep_layout=False):
        """Vẽ mạng với Cyberpunk style clean và tối giản."""
        try:
            self.clear_highlights()
            self.ax.clear()
            self.ax.axis('off')
            self.current_G = G

            if G is None or G.number_of_nodes() == 0:
                self.canvas.draw()
                return

            # 1. Layout Logic - Tối ưu độ giãn
            if not keep_layout or self.current_pos is None:
                num_nodes = G.number_of_nodes()
                if num_nodes > 0:
                    k_val = 2.8 / np.sqrt(num_nodes)  # Tăng độ giãn
                else:
                    k_val = 0.5
                
                self.current_pos = nx.spring_layout(
                    G, seed=42, k=k_val, iterations=150, scale=2.8
                )
            else:
                unplaced = [n for n in G.nodes() if n not in self.current_pos]
                if unplaced:
                    new_pos = nx.spring_layout(
                        G, pos=self.current_pos, 
                        fixed=list(self.current_pos.keys())
                    )
                    self.current_pos.update(new_pos)
            
            pos = self.current_pos

            # --- LAYER 1: DÂY CÁP (EDGES) - ZORDER=1 ---
            edge_colors = []
            edge_widths = []
            edge_styles = []
            for u, v, d in G.edges(data=True):
                # Ưu tiên 1: Màu đặc biệt (giữ nguyên)
                if d.get('color'):
                    edge_colors.append(d.get('color'))
                    edge_widths.append(3.0 if d.get('color') == '#FF0000' else 1.5)
                elif d.get('stp_state') == 'forwarding':
                    edge_colors.append('#00FF00')
                    edge_widths.append(2.0)
                elif d.get('stp_state') == 'blocking':
                    edge_colors.append('#FF0000')
                    edge_widths.append(1.0)
                # Ưu tiên 2: Cáp quang (Fiber) - Giữ nguyên Cyan
                elif d.get('type') == 'Fiber':
                    edge_colors.append('#00FFFF')
                    edge_widths.append(2.0)
                # Mặc định: Cáp Ethernet (Cải tiến màu và độ dày)
                else:
                    # Thay #555555 (xám tối) bằng #AAAAAA (xám sáng hơn nhiều)
                    edge_colors.append('#AAAAAA')
                    # Tăng độ dày lên chút
                    edge_widths.append(1.5)
                edge_styles.append(
                    'dashed' if d.get('stp_state') == 'blocking'
                    else d.get('style', 'solid')
                )
            nx.draw_networkx_edges(
                G, pos, ax=self.ax,
                edge_color=edge_colors,
                width=edge_widths,
                style=edge_styles,
                # Tăng độ trong suốt chung lên 0.9 (từ 0.8)
                alpha=0.9
            )

            # --- LAYER 2: NODES (Thiết bị) - Neon colors ---
            node_groups = {}
            for node, data in G.nodes(data=True):
                n_type = data.get('type', 'PC')
                if n_type not in node_groups:
                    node_groups[n_type] = []
                node_groups[n_type].append(node)

            # Màu Cyberpunk neon cho từng loại thiết bị
            DEFAULT_COLORS = {
                'Router': '#FF00FF',   # Magenta neon
                'Switch': '#00D9FF',   # Cyan neon
                'Server': '#FF0055',   # Pink neon
                'PC': '#00FF41',       # Matrix green
            }

            for n_type, nodes_in_group in node_groups.items():
                shape = SHAPE_MAP.get(n_type, 'o')
                default_color = DEFAULT_COLORS.get(n_type, '#FFFFFF')
                
                colors = [
                    G.nodes[n].get('color', default_color) 
                    for n in nodes_in_group
                ]
                sizes = [
                    G.nodes[n].get('size', 450)  # Tăng size một chút
                    for n in nodes_in_group
                ]

                nx.draw_networkx_nodes(
                    G, pos, ax=self.ax,
                    nodelist=nodes_in_group,
                    node_shape=shape,
                    node_color=colors,
                    node_size=sizes,
                    edgecolors='#FFFFFF',  # Viền trắng sáng
                    linewidths=2.0,
                    alpha=0.9
                )

            # --- LAYER 3: LABELS - Rõ ràng trên nền đen ---
            label_pos = {k: (v[0], v[1] - 0.13) for k, v in pos.items()}

            text_items = nx.draw_networkx_labels(
                G, label_pos, ax=self.ax,
                font_size=9,
                font_color='#FFFFFF',  # Trắng sáng
                font_weight='bold',
                font_family='monospace'  # Font monospace cho cảm giác tech
            )

            # Viền đen đậm hơn cho chữ để tách biệt rõ
            for _, text_obj in text_items.items():
                text_obj.set_path_effects([
                    path_effects.withStroke(linewidth=3.5, foreground='#000000')
                ])

            self.canvas.draw()

        except Exception as e:
            print(f"Drawing Error: {e}")
            import traceback
            traceback.print_exc()

    def clear_highlights(self):
        """Xóa sạch các đường highlight cũ trên canvas."""
        if not self.highlight_artists:
            return

        for artist in self.highlight_artists:
            try:
                artist.remove()
            except ValueError:
                pass

        self.highlight_artists.clear()
        self.canvas.draw()

    def highlight_path(self, path_nodes):
        """Highlight đường đi với hiệu ứng neon nổi bật."""
        self.clear_highlights()

        if not self.current_G or not path_nodes or not self.current_pos:
            return
        
        pos = self.current_pos
        path_edges = list(zip(path_nodes, path_nodes[1:]))

        # Highlight Edges - Neon magenta sáng
        edge_artists = nx.draw_networkx_edges(
            self.current_G, pos, ax=self.ax,
            edgelist=path_edges,
            edge_color='#FF00FF',  # Magenta neon
            width=4.0,
            alpha=1.0
        )
        if edge_artists:
            self.highlight_artists.append(edge_artists)

        # Highlight Nodes
        for node in path_nodes:
            node_data = self.current_G.nodes[node]
            n_type = node_data.get('type', 'PC')
            shape = SHAPE_MAP.get(n_type, 'o')
            size = node_data.get('size', 450)

            node_artist = nx.draw_networkx_nodes(
                self.current_G, pos, ax=self.ax,
                nodelist=[node],
                node_shape=shape,
                node_color='#FF00FF',  # Magenta neon
                node_size=size + 250,
                edgecolors='#FFFFFF',
                linewidths=3.0,
                alpha=0.95
            )
            if node_artist:
                self.highlight_artists.append(node_artist)

        self.canvas.draw()