import networkx as nx
import logging
from collections import deque

class VirusSimulator:
    """
    Class mô phỏng sự lây lan của mã độc trong mạng.
    Sử dụng thuật toán BFS (Breadth-First Search) để mô phỏng lây lan theo từng lớp.
    """

    @staticmethod
    def simulate_spread(G, start_node):
        """
        Mô phỏng lây nhiễm virus bắt đầu từ 'start_node'.
        
        Returns:
            list: Một danh sách các bước (steps). Mỗi bước là một list các node bị nhiễm mới.
                  VD: [ ['PC1'], ['SW1'], ['R1', 'PC2'] ]
        """
        if start_node not in G:
            return []

        visited = set()
        visited.add(start_node)
        
        queue = deque([start_node])
        steps = [] # Lưu lịch sử lây nhiễm để làm Animation

        # Thêm bước đầu tiên: Patient Zero
        steps.append([start_node])

        while queue:
            # Lấy tất cả node ở lớp hiện tại (để virus lan đồng thời)
            current_level_nodes = []
            level_size = len(queue)

            for _ in range(level_size):
                current_node = queue.popleft()
                
                # Tìm các máy hàng xóm chưa bị nhiễm
                neighbors = list(G.neighbors(current_node))
                for neighbor in neighbors:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        current_level_nodes.append(neighbor)
            
            # Nếu lớp này có máy bị lây, ghi nhận vào lịch sử
            if current_level_nodes:
                steps.append(current_level_nodes)

        logging.info(f"Simulation calculated: {len(steps)} steps of infection.")
        return steps