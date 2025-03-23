import psutil
import GPUtil
import logging
from typing import Dict, List, Optional
import time

class SystemMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_gpu_info(self) -> List[Dict]:
        """获取GPU信息"""
        try:
            gpus = GPUtil.getGPUs()
            return [
                {
                    "id": gpu.id,
                    "name": gpu.name,
                    "memory_total": gpu.memoryTotal,
                    "memory_used": gpu.memoryUsed,
                    "memory_free": gpu.memoryFree,
                    "gpu_load": gpu.load * 100,
                    "temperature": gpu.temperature
                }
                for gpu in gpus
            ]
        except Exception as e:
            self.logger.error(f"Error getting GPU info: {str(e)}")
            return []
    
    def get_cpu_info(self) -> Dict:
        """获取CPU信息"""
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "cpu_count": psutil.cpu_count(),
                "cpu_freq": {
                    "current": psutil.cpu_freq().current,
                    "min": psutil.cpu_freq().min,
                    "max": psutil.cpu_freq().max
                }
            }
        except Exception as e:
            self.logger.error(f"Error getting CPU info: {str(e)}")
            return {}
    
    def get_memory_info(self) -> Dict:
        """获取内存信息"""
        try:
            memory = psutil.virtual_memory()
            return {
                "total": round(memory.total / (1024**3), 2),  # GB
                "available": round(memory.available / (1024**3), 2),  # GB
                "used": round(memory.used / (1024**3), 2),  # GB
                "percent": memory.percent
            }
        except Exception as e:
            self.logger.error(f"Error getting memory info: {str(e)}")
            return {}
    
    def get_disk_info(self) -> Dict:
        """获取磁盘信息"""
        try:
            disk = psutil.disk_usage('/')
            return {
                "total": round(disk.total / (1024**3), 2),  # GB
                "used": round(disk.used / (1024**3), 2),  # GB
                "free": round(disk.free / (1024**3), 2),  # GB
                "percent": disk.percent
            }
        except Exception as e:
            self.logger.error(f"Error getting disk info: {str(e)}")
            return {}
    
    def get_network_info(self) -> Dict:
        """获取网络信息"""
        try:
            net_io = psutil.net_io_counters()
            return {
                "bytes_sent": round(net_io.bytes_sent / (1024**2), 2),  # MB
                "bytes_recv": round(net_io.bytes_recv / (1024**2), 2),  # MB
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv
            }
        except Exception as e:
            self.logger.error(f"Error getting network info: {str(e)}")
            return {}
    
    def get_process_info(self, pid: Optional[int] = None) -> Dict:
        """获取进程信息"""
        try:
            if pid is None:
                pid = psutil.Process().pid
                
            process = psutil.Process(pid)
            return {
                "pid": process.pid,
                "name": process.name(),
                "status": process.status(),
                "cpu_percent": process.cpu_percent(),
                "memory_percent": process.memory_percent(),
                "create_time": time.strftime(
                    '%Y-%m-%d %H:%M:%S',
                    time.localtime(process.create_time())
                )
            }
        except Exception as e:
            self.logger.error(f"Error getting process info: {str(e)}")
            return {}
    
    def get_all_info(self) -> Dict:
        """获取所有系统信息"""
        return {
            "gpu": self.get_gpu_info(),
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_info(),
            "network": self.get_network_info(),
            "process": self.get_process_info()
        }
    
    def monitor_resources(self, interval: int = 1, duration: Optional[int] = None):
        """监控系统资源使用情况
        
        Args:
            interval: 监控间隔（秒）
            duration: 监控持续时间（秒），None表示持续监控
        """
        start_time = time.time()
        
        try:
            while True:
                if duration and (time.time() - start_time) > duration:
                    break
                    
                info = self.get_all_info()
                self.logger.info(f"System Info: {info}")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.logger.info("Resource monitoring stopped by user")
        except Exception as e:
            self.logger.error(f"Error in resource monitoring: {str(e)}") 