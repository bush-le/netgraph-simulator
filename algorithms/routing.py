import networkx as nx
import logging

class RoutingManager:
    """
    Class chịu trách nhiệm tính toán đường đi trong mạng.
    Sử dụng thuật toán Dijkstra để tìm Shortest Path dựa trên trọng số (Weight/Latency).
    """
    
    @staticmethod
    def find_shortest_path(G, source_id, target_id):
        """
        Tìm đường đi ngắn nhất giữa 2 node.
        
        Args:
            G (nx.Graph): Đồ thị mạng hiện tại.
            source_id (str): ID node bắt đầu (VD: PC-SW1-1).
            target_id (str): ID node đích (VD: SRV-SW2-1).
            
        Returns:
            list: Danh sách các node trên đường đi [NodeA, NodeB, NodeC...]
            None: Nếu không tìm thấy đường.
        """
        try:
            if not G.has_node(source_id) or not G.has_node(target_id):
                logging.error("Source hoặc Target node không tồn tại.")
                return None

            # Sử dụng thuật toán Dijkstra của NetworkX
            # weight='weight': Ưu tiên đường có độ trễ thấp (Latency thấp)
            path = nx.dijkstra_path(G, source=source_id, target=target_id, weight='weight')
            
            # Tính tổng độ trễ (Cost)
            total_latency = nx.path_weight(G, path, weight='weight')
            
            logging.info(f"Route found: {path} (Latency: {total_latency}ms)")
            return path, total_latency

        except nx.NetworkXNoPath:
            logging.warning(f"Không có đường đi từ {source_id} đến {target_id}.")
            return None, 0
        except Exception as e:
            logging.error(f"Lỗi Routing: {str(e)}")
            return None, 0