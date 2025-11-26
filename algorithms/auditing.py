import networkx as nx
import logging

class NetworkAuditor:
    """
    Class chịu trách nhiệm kiểm tra sức khỏe và độ tin cậy của mạng.
    """

    @staticmethod
    def perform_full_audit(G):
        """
        Thực hiện quét toàn bộ mạng để tìm lỗi và điểm yếu.
        
        Args:
            G (nx.Graph): Đồ thị mạng.
            
        Returns:
            dict: Báo cáo chi tiết gồm tình trạng liên thông, danh sách điểm yếu (Bridges).
        """
        report = {
            "is_connected": False,
            "connected_components": 0,
            "critical_links": [], # Các cạnh cầu (Bridges)
            "average_redundancy": 0.0
        }

        try:
            # 1. Kiểm tra tính liên thông (Connectivity)
            # Mạng tốt phải liên thông hoàn toàn (1 thành phần)
            report["is_connected"] = nx.is_connected(G)
            report["connected_components"] = nx.number_connected_components(G)

            # 2. Tìm điểm yếu chí tử (Network Bridges)
            # Bridge là cạnh mà nếu xóa đi, số thành phần liên thông tăng lên -> Nguy hiểm
            bridges = list(nx.bridges(G))
            report["critical_links"] = bridges

            # 3. Tính độ dư thừa trung bình (Average Node Degree)
            # Độ dư thừa cao = Mạng lưới chằng chịt = Khó bị chia cắt
            degrees = [d for n, d in G.degree()]
            if degrees:
                report["average_redundancy"] = sum(degrees) / len(degrees)

            logging.info(f"Audit Complete. Critical Links found: {len(bridges)}")
            return report

        except Exception as e:
            logging.error(f"Lỗi Audit: {str(e)}")
            return report