import datetime

class ReportGenerator:
    """
    Tạo báo cáo dạng văn bản (Text Report) về trạng thái mạng.
    """

    @staticmethod
    def export_summary(G, stats, audit_result, filepath):
        """
        Ghi báo cáo tổng hợp ra file .txt
        """
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("==================================================\n")
                f.write(f" NETGRAPH SENTINEL - SECURITY AUDIT REPORT\n")
                f.write(f" Date: {timestamp}\n")
                f.write("==================================================\n\n")
                
                f.write("[1] TOPOLOGY OVERVIEW\n")
                f.write(f"    - Total Nodes:    {stats['total_nodes']}\n")
                f.write(f"    - Total Edges:    {stats['total_edges']}\n")
                f.write(f"    - Core Routers:   {stats['routers']}\n")
                f.write(f"    - Switches:       {stats['switches']}\n")
                f.write(f"    - Endpoints:      {stats['endpoints']}\n\n")
                
                f.write("[2] HEALTH CHECK\n")
                status = "STABLE" if audit_result['is_connected'] and not audit_result['critical_links'] else "CRITICAL"
                f.write(f"    - System Status:  {status}\n")
                f.write(f"    - Connectivity:   {'Full' if audit_result['is_connected'] else 'Partitioned'}\n")
                f.write(f"    - Redundancy:     {audit_result['average_redundancy']:.2f} links/node\n")
                
                f.write("\n[3] VULNERABILITIES (Single Points of Failure)\n")
                if audit_result['critical_links']:
                    for u, v in audit_result['critical_links']:
                        f.write(f"    [!] Weak Link: {u} <---> {v}\n")
                else:
                    f.write("    [OK] No critical weak links detected.\n")
                
                f.write("\n==================================================\n")
                f.write(" CONFIDENTIAL - INTERNAL USE ONLY\n")
                f.write("==================================================\n")
                
            return True, f"Report exported to {filepath}"
        except Exception as e:
            return False, str(e)