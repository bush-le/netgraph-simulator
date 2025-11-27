import networkx as nx
import random

class NetworkGenerator:
    """
    Class chịu trách nhiệm sinh ra các đồ thị mạng giả lập với nhiều kiểu tô pô khác nhau.
    """

    def __init__(self):
        # Định nghĩa màu sắc và kích thước chuẩn cho các loại thiết bị
        self.device_styles = {
            'Router': {'color': '#FF4500', 'size': 450}, # Orange Red
            'Switch': {'color': '#00BFFF', 'size': 350}, # Deep Sky Blue
            'Server': {'color': '#32CD32', 'size': 300}, # Lime Green
            'PC':     {'color': '#D3D3D3', 'size': 250}  # Light Gray
        }

    def _add_node_with_style(self, G, node_name, node_type):
        """Hàm tiện ích để thêm node với style chuẩn."""
        style = self.device_styles.get(node_type, self.device_styles['PC'])
        G.add_node(node_name, 
                   type=node_type, 
                   label=node_name, 
                   color=style['color'], 
                   size=style['size'],
                   ip=f"192.168.{random.randint(1,254)}.{random.randint(1,254)}")

    def _add_edge_with_style(self, G, u, v, edge_type='Ethernet'):
        """Hàm tiện ích để thêm cạnh với style chuẩn."""
        if edge_type == 'Fiber':
            G.add_edge(u, v, type='Fiber', weight=1, capacity=10000) # Trễ thấp, băng thông cao
        else:
            G.add_edge(u, v, type='Ethernet', weight=10, capacity=1000) # Trễ cao, băng thông thấp

    # ===========================
    # CÁC HÀM SINH TÔ PÔ CỤ THỂ
    # ===========================

    def _gen_hierarchical(self):
        """Sinh mạng phân cấp (Hierarchical / Tree)."""
        G = nx.Graph()
        # 1. Core Layer (Routers)
        core_routers = ['R1', 'R2', 'R3']
        for r in core_routers: self._add_node_with_style(G, r, 'Router')
        # Nối các Core Router với nhau thành một vòng hoặc lưới nhỏ (Fiber)
        self._add_edge_with_style(G, 'R1', 'R2', 'Fiber')
        self._add_edge_with_style(G, 'R2', 'R3', 'Fiber')
        self._add_edge_with_style(G, 'R3', 'R1', 'Fiber')

        # 2. Distribution Layer (Switches)
        dist_switches = []
        for i, core in enumerate(core_routers):
            num_sw = random.randint(1, 2)
            for j in range(num_sw):
                sw_name = f"SW{i+1}-{j+1}"
                dist_switches.append(sw_name)
                self._add_node_with_style(G, sw_name, 'Switch')
                self._add_edge_with_style(G, core, sw_name, 'Fiber')

        # 3. Access Layer (PCs & Servers)
        for sw in dist_switches:
            # Thêm PCs
            num_pcs = random.randint(2, 4)
            for k in range(num_pcs):
                pc_name = f"PC-{sw[2:]}-{k+1}"
                self._add_node_with_style(G, pc_name, 'PC')
                self._add_edge_with_style(G, sw, pc_name, 'Ethernet')
            # Thêm Servers (tuỳ chọn)
            if random.random() > 0.5:
                num_srv = random.randint(1, 2)
                for k in range(num_srv):
                    srv_name = f"SRV-{sw[2:]}-{k+1}"
                    self._add_node_with_style(G, srv_name, 'Server')
                    self._add_edge_with_style(G, sw, srv_name, 'Fiber')
        return G

    def _gen_mesh(self):
        """Sinh mạng lưới (Mesh) - Ngẫu nhiên, độ kết nối cao."""
        # Sử dụng mô hình Watts-Strogatz để tạo mạng "thế giới nhỏ" (small-world)
        # Đảm bảo tính liên thông và có các cụm.
        n_routers = 8
        k_neighbors = 4 # Mỗi node nối với 4 node gần nhất
        p_rewire = 0.3  # Xác suất nối lại cạnh để tạo đường tắt
        
        G_base = nx.connected_watts_strogatz_graph(n_routers, k_neighbors, p_rewire, seed=random.randint(1, 1000))
        G = nx.Graph()

        # Đổi tên node và gán kiểu Router cho mạng lõi
        router_map = {i: f"R{i+1}" for i in range(n_routers)}
        for i in range(n_routers):
            self._add_node_with_style(G, router_map[i], 'Router')
        
        for u, v in G_base.edges():
            self._add_edge_with_style(G, router_map[u], router_map[v], 'Fiber')

        # Gắn thêm một vài PC vào các Router này để có điểm đầu/cuối
        for r_name in list(G.nodes()):
            if random.random() > 0.3:
                pc_name = f"PC-{r_name}"
                self._add_node_with_style(G, pc_name, 'PC')
                self._add_edge_with_style(G, r_name, pc_name, 'Ethernet')
        return G

    def _gen_star(self):
        """Sinh mạng hình sao (Star)."""
        G = nx.Graph()
        # Node trung tâm (Core Switch/Router)
        center_node = "CORE-SW"
        self._add_node_with_style(G, center_node, 'Switch')
        # Kích thước core switch lớn hơn một chút
        G.nodes[center_node]['size'] = 500 

        # Các node vệ tinh (PCs/Servers)
        num_spokes = random.randint(8, 15)
        for i in range(num_spokes):
            node_type = 'Server' if random.random() > 0.8 else 'PC'
            node_name = f"{node_type}-{i+1}"
            self._add_node_with_style(G, node_name, node_type)
            
            edge_type = 'Fiber' if node_type == 'Server' else 'Ethernet'
            self._add_edge_with_style(G, center_node, node_name, edge_type)
        return G

    def _gen_ring(self):
        """Sinh mạng vòng tròn (Ring)."""
        G = nx.Graph()
        num_switches = random.randint(5, 8)
        
        # Tạo các Switch trong vòng tròn
        switch_names = [f"SW{i+1}" for i in range(num_switches)]
        for name in switch_names:
            self._add_node_with_style(G, name, 'Switch')
            
        # Nối chúng thành vòng tròn (Cáp quang)
        for i in range(num_switches):
            u = switch_names[i]
            v = switch_names[(i + 1) % num_switches] # Nối với node tiếp theo, node cuối nối về đầu
            self._add_edge_with_style(G, u, v, 'Fiber')
            
        # Gắn PC vào mỗi Switch
        for sw in switch_names:
            num_pcs = random.randint(1, 3)
            for i in range(num_pcs):
                pc_name = f"PC-{sw}-{i+1}"
                self._add_node_with_style(G, pc_name, 'PC')
                self._add_edge_with_style(G, sw, pc_name, 'Ethernet')
        return G

    # ===========================
    # HÀM CHÍNH (PUBLIC API)
    # ===========================
    def generate_network(self, topology_type='hierarchical'):
        """
        Hàm chính để sinh mạng dựa trên kiểu tô pô được yêu cầu.
        Args:
            topology_type (str): 'hierarchical', 'mesh', 'star', hoặc 'ring'.
        """
        if topology_type == 'mesh':
            return self._gen_mesh()
        elif topology_type == 'star':
            return self._gen_star()
        elif topology_type == 'ring':
            return self._gen_ring()
        else:
            # Mặc định là hierarchical
            return self._gen_hierarchical()

    def get_topology_stats(self, G):
        """Trả về thống kê cơ bản của đồ thị hiện tại."""
        if G is None: return {}
        stats = {
            "total_nodes": G.number_of_nodes(),
            "total_edges": G.number_of_edges(),
            "routers": len([n for n, d in G.nodes(data=True) if d.get('type') == 'Router']),
            "switches": len([n for n, d in G.nodes(data=True) if d.get('type') == 'Switch']),
            "endpoints": len([n for n, d in G.nodes(data=True) if d.get('type') in ['PC', 'Server']]),
        }
        return stats