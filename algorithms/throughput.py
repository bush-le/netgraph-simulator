import networkx as nx
import logging

class BandwidthAnalyzer:
    """
    Class chịu trách nhiệm phân tích hiệu năng và băng thông mạng.
    Sử dụng thuật toán Max Flow (Edmonds-Karp) để tìm luồng cực đại.
    """

    @staticmethod
    def analyze_max_bandwidth(G, source, target):
        """
        Tính toán băng thông tối đa (Max Flow) giữa nguồn và đích.
        Đồng thời xác định các điểm nghẽn (Bottlenecks).

        Args:
            G (nx.Graph): Đồ thị mạng.
            source (str): Node gửi.
            target (str): Node nhận.

        Returns:
            tuple: (max_throughput, bottleneck_edges)
                   - max_throughput: Tổng băng thông (Mbps).
                   - flow_dict: Dictionary chứa luồng đi qua từng cạnh.
        """
        try:
            if not G.has_node(source) or not G.has_node(target):
                return 0, {}

            # Thuật toán Max Flow (dựa trên capacity của cạnh)
            # capacity='capacity': Thuộc tính băng thông ta đã định nghĩa trong network_data
            flow_value, flow_dict = nx.maximum_flow(
                G, source, target, capacity='capacity'
            )
            
            logging.info(f"Max Bandwidth {source}->{target}: {flow_value} Mbps")
            return flow_value, flow_dict

        except Exception as e:
            logging.error(f"Lỗi tính toán băng thông: {str(e)}")
            return 0, {}

    @staticmethod
    def get_utilization_color(current_flow, max_capacity):
        """
        Trả về màu sắc dựa trên mức độ sử dụng băng thông.
        """
        if max_capacity == 0: return '#555555'
        
        utilization = current_flow / max_capacity
        if utilization >= 0.9: return '#FF0000' # Đỏ: Nghẽn (>90%)
        if utilization >= 0.5: return '#FFA500' # Cam: Tải cao (>50%)
        if utilization > 0:    return '#00FF00' # Xanh: Đang truyền
        return '#333333'                        # Xám tối: Không dùng