import networkx as nx
import random
import logging

# Cấu hình Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NetworkGenerator:
    """
    Class chịu trách nhiệm sinh dữ liệu mạng giả lập (Model Layer).
    Sử dụng NetworkX để quản lý cấu trúc đồ thị.
    """

    def __init__(self):
        self.G = nx.Graph()  # Đồ thị vô hướng (Undirected Graph)
        self.device_counter = 0 # Dùng để sinh ID duy nhất

    def _reset_graph(self):
        """Xóa dữ liệu cũ để tạo mạng mới."""
        self.G.clear()
        self.device_counter = 0

    def generate_hierarchical_network(self, num_routers=3, switches_per_router=2, pcs_per_switch=3):
        """
        Sinh mạng theo mô hình Phân cấp (Hierarchical Model):
        Core (Router) -> Distribution (Switch) -> Access (PC/Server).
        
        Args:
            num_routers (int): Số lượng Router (Core Layer).
            switches_per_router (int): Số Switch nối vào mỗi Router.
            pcs_per_switch (int): Số PC nối vào mỗi Switch.
        
        Returns:
            nx.Graph: Đồ thị mạng đã được sinh kèm thuộc tính.
        """
        try:
            self._reset_graph()
            logging.info(f"Đang khởi tạo mạng Phân cấp: {num_routers} Router, {switches_per_router} Switch/Router, {pcs_per_switch} PC/Switch.")

            routers = []

            # --- 1. CORE LAYER (Tầng Lõi - Routers) ---
            for i in range(num_routers):
                router_id = f"R{i+1}"
                # Giả lập IP Public hoặc Gateway: 10.0.i.1
                ip_addr = f"10.0.{i+1}.1"
                
                self.G.add_node(router_id, 
                                type="Router", 
                                label=router_id,
                                ip=ip_addr,
                                status="online",
                                size=500,           # Kích thước hiển thị
                                color="#FF4500",    # Màu cam neon (Cyberpunk style)
                                layer=0)            # Dùng để vẽ Layout phân tầng
                routers.append(router_id)

            # Tạo kết nối Mesh giữa các Router (Backbone)
            # Router nối với nhau bằng cáp quang tốc độ cao (Low Latency, High Bandwidth)
            for i in range(len(routers)):
                for j in range(i + 1, len(routers)):
                    # Xác suất kết nối 100% để đảm bảo tính liên thông
                    self.G.add_edge(routers[i], routers[j], 
                                    weight=random.randint(1, 5),      # Latency: 1-5ms
                                    capacity=10000,                   # Bandwidth: 10Gbps
                                    type="Fiber")

            # --- 2. DISTRIBUTION LAYER (Tầng Phân Phối - Switches) ---
            for r_idx, router_id in enumerate(routers):
                for s in range(switches_per_router):
                    switch_id = f"SW{router_id[1:]}-{s+1}"
                    # Switch Management IP
                    ip_addr = f"10.0.{r_idx+1}.{10 + s}"
                    
                    self.G.add_node(switch_id, 
                                    type="Switch", 
                                    label=switch_id,
                                    ip=ip_addr,
                                    status="online",
                                    size=300,
                                    color="#00BFFF", # Màu xanh dương neon
                                    layer=1)
                    
                    # Nối Switch về Router quản lý nó
                    self.G.add_edge(router_id, switch_id, 
                                    weight=random.randint(5, 10),    # Latency: 5-10ms
                                    capacity=1000,                   # Bandwidth: 1Gbps
                                    type="Ethernet_Gigabit")

                    # --- 3. ACCESS LAYER (Tầng Truy Nhập - PCs/Servers) ---
                    for p in range(pcs_per_switch):
                        # Random hóa: Có thể là PC hoặc Server
                        is_server = random.choice([True, False, False, False]) # 25% là Server
                        
                        device_type = "Server" if is_server else "PC"
                        dev_prefix = "SRV" if is_server else "PC"
                        dev_id = f"{dev_prefix}-{switch_id[2:]}-{p+1}"
                        
                        # Cấp DHCP giả lập: 192.168.subnet.host
                        ip_addr = f"192.168.{r_idx+1}.{100 + p + (s*10)}"

                        node_color = "#32CD32" if is_server else "#D3D3D3" # Server: Xanh lá, PC: Xám trắng
                        node_size = 250 if is_server else 150

                        self.G.add_node(dev_id, 
                                        type=device_type, 
                                        label=dev_id,
                                        ip=ip_addr,
                                        status="online",
                                        size=node_size,
                                        color=node_color,
                                        layer=2)
                        
                        # Nối thiết bị vào Switch
                        self.G.add_edge(switch_id, dev_id, 
                                        weight=random.randint(10, 50),   # Latency: 10-50ms
                                        capacity=100,                    # Bandwidth: 100Mbps
                                        type="Ethernet_Fast")

            logging.info(f"Đã tạo mạng thành công: {self.G.number_of_nodes()} Nodes, {self.G.number_of_edges()} Edges.")
            return self.G

        except Exception as e:
            logging.error(f"Lỗi nghiêm trọng khi sinh mạng: {str(e)}")
            # Trả về graph rỗng hoặc graph hiện tại để tránh crash UI
            return self.G

    def get_topology_stats(self):
        """Trả về thống kê nhanh về mạng hiện tại."""
        stats = {
            "total_nodes": self.G.number_of_nodes(),
            "total_edges": self.G.number_of_edges(),
            "routers": len([n for n, d in self.G.nodes(data=True) if d.get('type') == 'Router']),
            "switches": len([n for n, d in self.G.nodes(data=True) if d.get('type') == 'Switch']),
            "endpoints": len([n for n, d in self.G.nodes(data=True) if d.get('type') in ['PC', 'Server']]),
        }
        return stats

# --- Block kiểm tra nhanh (Unit Test) ---
if __name__ == "__main__":
    # Code này chỉ chạy khi test file trực tiếp
    generator = NetworkGenerator()
    G = generator.generate_hierarchical_network(num_routers=2, switches_per_router=2, pcs_per_switch=2)
    
    print("--- Network Nodes Attributes ---")
    for node, data in list(G.nodes(data=True))[:5]: # In thử 5 node đầu
        print(f"Node: {node}, Data: {data}")
    
    print("\n--- Network Edges Attributes ---")
    for u, v, data in list(G.edges(data=True))[:5]: # In thử 5 cạnh đầu
        print(f"Link: {u} <-> {v}, Data: {data}")