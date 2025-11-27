import networkx as nx
import numpy as np

class GraphTheoryManager:
    """
    Class chuyên xử lý các bài toán lý thuyết đồ thị học thuật.
    Đáp ứng các yêu cầu: DFS, Bipartite, Biểu diễn ma trận, Chu trình Euler.
    """

    def run_dfs(self, G, start_node=None):
        """4. Duyệt đồ thị theo chiều sâu (DFS)."""
        if G.number_of_nodes() == 0: return "Đồ thị rỗng."
        
        # Nếu không chọn nút bắt đầu, lấy nút đầu tiên
        if start_node is None or start_node not in G:
            start_node = next(iter(G.nodes()))

        # Sử dụng NetworkX để duyệt DFS
        # Kết quả trả về là một generator các cạnh theo thứ tự duyệt
        dfs_edges = list(nx.dfs_edges(G, source=start_node))
        
        # Format kết quả cho dễ đọc
        result = f"DFS Traversal starting from '{start_node}':\n"
        path_nodes = [start_node] + [v for u, v in dfs_edges]
        result += " -> ".join(path_nodes)
        
        # Liệt kê chi tiết các bước duyệt
        result += "\n\n[Detailed Steps (Edges Visited)]:\n"
        for i, (u, v) in enumerate(dfs_edges):
            result += f"{i+1}. {u} -> {v}\n"
            
        return result

    def check_bipartite(self, G):
        """5. Kiểm tra đồ thị 2 phía (Bipartite Graph) & Giải thích chi tiết."""
        if G.number_of_nodes() == 0: return "Đồ thị rỗng."
        
        is_bip = nx.is_bipartite(G)
        result = f"KẾT QUẢ KIỂM TRA ĐỒ THỊ 2 PHÍA (BIPARTITE):\n"
        result += f" => {str(is_bip).upper()}\n\n"
        
        if is_bip:
            # Nếu là 2 phía, liệt kê 2 tập hợp
            result += "GIẢI THÍCH: Đồ thị CÓ THỂ chia làm 2 tập đỉnh riêng biệt (A và B) sao cho không có cạnh nào nối 2 đỉnh cùng một tập.\n\n"
            try:
                sets = nx.bipartite.sets(G)
                # Giới hạn hiển thị nếu danh sách quá dài
                set_a = list(sets[0])
                set_b = list(sets[1])
                result += f"[TẬP A - {len(set_a)} node]: {str(set_a[:10])}..." if len(set_a) > 10 else f"[TẬP A]: {str(set_a)}"
                result += "\n"
                result += f"[TẬP B - {len(set_b)} node]: {str(set_b[:10])}..." if len(set_b) > 10 else f"[TẬP B]: {str(set_b)}"
            except:
                pass
        else:
            # Nếu KHÔNG phải 2 phía, tìm bằng chứng (Chu trình lẻ)
            result += "GIẢI THÍCH: Đồ thị chứa CHU TRÌNH LẺ (Odd Cycle). Theo định lý Kőnig, đồ thị chứa chu trình lẻ không thể là đồ thị 2 phía.\n\n"
            result += "[BẰNG CHỨNG - CÁC NÚT GÂY XUNG ĐỘT]:\n"
            
            try:
                # Tìm cơ sở chu trình (Cycle Basis)
                cycles = nx.cycle_basis(G)
                found_odd = False
                for cycle in cycles:
                    if len(cycle) % 2 != 0:
                        # Tìm thấy chu trình lẻ!
                        path_str = " -> ".join(cycle) + f" -> {cycle[0]}"
                        result += f"(!) Phát hiện chu trình độ dài {len(cycle)} (Lẻ):\n    {path_str}\n"
                        
                        # Giải thích logic tô màu
                        result += "\nLý do xung đột màu:\n"
                        result += f"  1. Giả sử {cycle[0]} màu ĐỎ.\n"
                        result += f"  2. Thì {cycle[1]} phải màu XANH.\n"
                        if len(cycle) == 3:
                            result += f"  3. Thì {cycle[2]} phải màu ĐỎ.\n"
                            result += f"  => NHƯNG {cycle[2]} nối lại về {cycle[0]} (cũng ĐỎ). XUNG ĐỘT!"
                        
                        found_odd = True
                        break # Chỉ cần chỉ ra 1 cái là đủ chứng minh
                
                if not found_odd:
                    result += "(Không tìm thấy chu trình lẻ đơn giản trong cơ sở, nhưng cấu trúc phức tạp gây xung đột)."
            except Exception as e:
                result += f"Không thể trích xuất chu trình cụ thể: {str(e)}"
            
        return result

    def get_representations(self, G):
        """6. Chuyển đổi các phương pháp biểu diễn đồ thị."""
        if G.number_of_nodes() == 0: return "Đồ thị rỗng."
        
        nodes = sorted(list(G.nodes()))
        node_to_idx = {node: i for i, node in enumerate(nodes)}
        n = len(nodes)

        res = "=== CÁC PHƯƠNG PHÁP BIỂU DIỄN ĐỒ THỊ ===\n\n"
        res += f"Danh sách đỉnh (Mapping): {nodes}\n\n"

        # 1. MA TRẬN KỀ (Adjacency Matrix)
        res += "[1] MA TRẬN KỀ (Adjacency Matrix):\n"
        adj_matrix = np.zeros((n, n), dtype=int)
        for u, v in G.edges():
            i, j = node_to_idx[u], node_to_idx[v]
            adj_matrix[i][j] = 1
            adj_matrix[j][i] = 1 # Đồ thị vô hướng
        
        # In ma trận đẹp hơn
        res += "   " + " ".join([f"{i:2d}" for i in range(n)]) + "\n"
        for i in range(n):
            res += f"{i:2d} [" + " ".join([f"{x:2d}" for x in adj_matrix[i]]) + "]\n"

        # 2. DANH SÁCH KỀ (Adjacency List)
        res += "\n[2] DANH SÁCH KỀ (Adjacency List):\n"
        for node in nodes:
            neighbors = sorted(list(G.neighbors(node)))
            res += f"  {node}: {neighbors}\n"

        # 3. DANH SÁCH CẠNH (Edge List)
        res += "\n[3] DANH SÁCH CẠNH (Edge List):\n"
        edges = sorted([sorted(e) for e in G.edges()]) # Chuẩn hóa để (u,v) giống (v,u)
        seen_edges = set()
        for u, v in edges:
            edge_tuple = tuple(sorted((u,v)))
            if edge_tuple not in seen_edges:
                 res += f"  ({u}, {v})\n"
                 seen_edges.add(edge_tuple)

        return res

    def find_eulerian(self, G):
        """7.4 & 7.5. Tìm đường đi/Chu trình Euler (Đại diện cho Fleury/Hierholzer)."""
        # Lưu ý: NetworkX sử dụng thuật toán tối ưu (thường là Hierholzer cải tiến) 
        # để tìm chu trình Euler. Nó đáp ứng yêu cầu tìm kiếm Euler.
        
        if G.number_of_nodes() == 0: return "Đồ thị rỗng."
        
        # Kiểm tra điều kiện Euler cho đồ thị vô hướng:
        # - Liên thông (trừ các đỉnh cô lập bậc 0)
        # - Chu trình Euler: Tất cả các đỉnh có bậc chẵn.
        # - Đường đi Euler: Có đúng 0 hoặc 2 đỉnh bậc lẻ.
        
        res = "=== PHÂN TÍCH EULER (Fleury / Hierholzer) ===\n\n"
        
        # Kiểm tra tính liên thông của các cạnh
        if not nx.is_connected(G):
             # Loại bỏ các node cô lập để kiểm tra phần có cạnh
             G_core = G.subgraph([n for n, d in G.degree() if d > 0])
             if not nx.is_connected(G_core) and G_core.number_of_nodes() > 0:
                 return res + "Kết quả: KHÔNG CÓ đường đi hay chu trình Euler.\nLý do: Đồ thị không liên thông (có nhiều thành phần chứa cạnh)."

        odd_degree_nodes = [n for n, d in G.degree() if d % 2 != 0]
        num_odd = len(odd_degree_nodes)
        
        res += f"Số đỉnh bậc lẻ: {num_odd} ({odd_degree_nodes})\n\n"
        
        if num_odd == 0:
            res += "=> KẾT LUẬN: Đồ thị có CHU TRÌNH EULER (Eulerian Circuit).\n"
            try:
                circuit = list(nx.eulerian_circuit(G))
                res += "\nChu trình tìm được:\n"
                path_str = " -> ".join([str(u) for u, v in circuit] + [str(circuit[-1][1])])
                res += path_str
            except Exception as e:
                 res += f"\nKhông thể tìm chu trình cụ thể: {e}"

        elif num_odd == 2:
            res += "=> KẾT LUẬN: Đồ thị có ĐƯỜNG ĐI EULER (Eulerian Path).\n"
            res += f"(Bắt đầu/Kết thúc tại các đỉnh bậc lẻ: {odd_degree_nodes})\n"
            try:
                # NetworkX < 3.0 dùng eulerian_path, >= 3.0 cần kiểm tra
                if hasattr(nx, 'eulerian_path'):
                     path = list(nx.eulerian_path(G))
                     res += "\nĐường đi tìm được:\n"
                     path_str = " -> ".join([str(u) for u, v in path] + [str(path[-1][1])])
                     res += path_str
                else:
                    res += "\n(Phiên bản NetworkX hiện tại cần cài đặt thêm để hiển thị đường đi cụ thể)."
            except Exception as e:
                 res += f"\nKhông thể tìm đường đi cụ thể: {e}"
        else:
             res += "=> KẾT LUẬN: KHÔNG CÓ đường đi hay chu trình Euler.\n"
             res += "Lý do: Số đỉnh bậc lẻ khác 0 và 2."
             
        return res