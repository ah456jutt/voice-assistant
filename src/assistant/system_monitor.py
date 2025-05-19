import psutil
import os
import platform
from datetime import datetime

class SystemMonitor:
    def get_system_vitals(self):
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return f"""System Status:
• CPU Usage: {cpu_usage}%
• Memory Used: {memory.percent}%
• Disk Space: {disk.percent}% used
• Available Storage: {disk.free / (1024**3):.1f} GB"""

    def get_network_status(self):
        network = psutil.net_io_counters()
        return f"""Network Status:
• Bytes Sent: {network.bytes_sent/1024/1024:.2f} MB
• Bytes Received: {network.bytes_recv/1024/1024:.2f} MB
• Packets Sent: {network.packets_sent}
• Packets Received: {network.packets_recv}"""

    def get_battery_info(self):
        battery = psutil.sensors_battery()
        if battery:
            return f"Battery: {battery.percent}% {'Plugged In' if battery.power_plugged else 'Not Plugged In'}"
        return "No battery detected"

    def get_running_processes(self):
        processes = []
        for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    'name': proc.info['name'],
                    'cpu': proc.info['cpu_percent'],
                    'memory': proc.info['memory_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage and get top 5
        top_processes = sorted(processes, key=lambda x: x['cpu'], reverse=True)[:5]
        return "\n".join([f"• {p['name']}: CPU {p['cpu']}%, RAM {p['memory']:.1f}%" for p in top_processes])