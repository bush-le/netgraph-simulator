import json
import networkx as nx
import logging

class FileManager:
    """
    Quản lý việc Lưu (Save) và Mở (Load) cấu hình mạng.
    Định dạng file: JSON.
    """

    @staticmethod
    def save_network_to_json(G, filepath):
        """
        Lưu đồ thị mạng xuống file JSON.
        """
        try:
            if G is None:
                return False, "Empty Graph"
            
            # Chuyển đổi Graph object thành Dictionary
            data = nx.node_link_data(G)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
                
            logging.info(f"Network saved to {filepath}")
            return True, "Success"
        except Exception as e:
            logging.error(f"Save Error: {str(e)}")
            return False, str(e)

    @staticmethod
    def load_network_from_json(filepath):
        """
        Đọc file JSON và tái tạo lại đồ thị mạng.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Tái tạo Graph từ Dictionary
            G = nx.node_link_graph(data)
            
            logging.info(f"Network loaded from {filepath}")
            return G, "Success"
        except Exception as e:
            logging.error(f"Load Error: {str(e)}")
            return None, str(e)