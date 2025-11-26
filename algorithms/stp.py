import networkx as nx
import logging

class STPManager:
    """
    Class mô phỏng giao thức Spanning Tree Protocol (STP).
    Nhiệm vụ: Loại bỏ các vòng lặp (Loops) trong mạng bằng cách tính toán Cây khung nhỏ nhất (MST).
    """

    @staticmethod
    def compute_spanning_tree(G):
        """
        Tính toán trạng thái STP cho toàn bộ mạng.
        
        Args:
            G (nx.Graph): Đồ thị mạng gốc.
            
        Returns:
            list: Danh sách các cạnh thuộc về STP (Active Links).
            list: Danh sách các cạnh bị khóa (Blocked Links).
        """
        try:
            # Tính toán Minimum Spanning Tree (MST) dựa trên trọng số (Weight/Latency)
            # Trong thực tế STP dùng Path Cost, ở đây ta dùng Weight tương đương.
            mst_graph = nx.minimum_spanning_tree(G, weight='weight')
            
            mst_edges = list(mst_graph.edges())
            
            # Tất cả các cạnh trong G mà KHÔNG nằm trong MST sẽ bị Block
            all_edges = list(G.edges())
            blocked_edges = []
            
            # Chuẩn hóa cạnh để so sánh (u, v) vs (v, u)
            mst_set = set(tuple(sorted(e)) for e in mst_edges)
            
            for u, v in all_edges:
                edge_tuple = tuple(sorted((u, v)))
                if edge_tuple not in mst_set:
                    blocked_edges.append((u, v))
            
            logging.info(f"STP Converged. Active: {len(mst_edges)}, Blocked: {len(blocked_edges)}")
            return mst_edges, blocked_edges

        except Exception as e:
            logging.error(f"Lỗi STP: {str(e)}")
            return [], []