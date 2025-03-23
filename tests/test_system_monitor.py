import pytest
from unittest.mock import MagicMock, patch
from core.system_monitor import SystemMonitor

@pytest.fixture
def system_monitor():
    """创建系统监控实例"""
    monitor = SystemMonitor()
    yield monitor
    del monitor

def test_init(system_monitor):
    """测试初始化"""
    assert system_monitor is not None

def test_get_cpu_info(system_monitor):
    """测试获取CPU信息"""
    cpu_info = system_monitor.get_cpu_info()
    assert cpu_info is not None
    assert "usage" in cpu_info
    assert "cores" in cpu_info
    assert "frequency" in cpu_info
    assert "temperature" in cpu_info

def test_get_memory_info(system_monitor):
    """测试获取内存信息"""
    memory_info = system_monitor.get_memory_info()
    assert memory_info is not None
    assert "total" in memory_info
    assert "used" in memory_info
    assert "free" in memory_info
    assert "percentage" in memory_info

def test_get_disk_info(system_monitor):
    """测试获取磁盘信息"""
    disk_info = system_monitor.get_disk_info()
    assert disk_info is not None
    assert isinstance(disk_info, list)
    assert len(disk_info) > 0
    assert "device" in disk_info[0]
    assert "total" in disk_info[0]
    assert "used" in disk_info[0]
    assert "free" in disk_info[0]
    assert "percentage" in disk_info[0]

def test_get_gpu_info(system_monitor):
    """测试获取GPU信息"""
    gpu_info = system_monitor.get_gpu_info()
    assert gpu_info is not None
    assert isinstance(gpu_info, list)
    assert len(gpu_info) > 0
    assert "name" in gpu_info[0]
    assert "memory_total" in gpu_info[0]
    assert "memory_used" in gpu_info[0]
    assert "memory_free" in gpu_info[0]
    assert "temperature" in gpu_info[0]
    assert "utilization" in gpu_info[0]

def test_get_network_info(system_monitor):
    """测试获取网络信息"""
    network_info = system_monitor.get_network_info()
    assert network_info is not None
    assert isinstance(network_info, list)
    assert len(network_info) > 0
    assert "interface" in network_info[0]
    assert "bytes_sent" in network_info[0]
    assert "bytes_recv" in network_info[0]
    assert "packets_sent" in network_info[0]
    assert "packets_recv" in network_info[0]

def test_get_process_info(system_monitor):
    """测试获取进程信息"""
    process_info = system_monitor.get_process_info()
    assert process_info is not None
    assert isinstance(process_info, list)
    assert len(process_info) > 0
    assert "pid" in process_info[0]
    assert "name" in process_info[0]
    assert "cpu_percent" in process_info[0]
    assert "memory_percent" in process_info[0]
    assert "status" in process_info[0]

def test_get_system_info(system_monitor):
    """测试获取系统信息"""
    system_info = system_monitor.get_system_info()
    assert system_info is not None
    assert "platform" in system_info
    assert "version" in system_info
    assert "machine" in system_info
    assert "processor" in system_info

def test_get_all_info(system_monitor):
    """测试获取所有信息"""
    all_info = system_monitor.get_all_info()
    assert all_info is not None
    assert "cpu" in all_info
    assert "memory" in all_info
    assert "disk" in all_info
    assert "gpu" in all_info
    assert "network" in all_info
    assert "process" in all_info
    assert "system" in all_info

def test_monitor_interval(system_monitor):
    """测试监控间隔"""
    with patch('time.sleep') as mock_sleep:
        system_monitor.start_monitoring(interval=1)
        mock_sleep.assert_called_with(1)

def test_monitor_callback(system_monitor):
    """测试监控回调"""
    callback_called = False
    
    def callback(info):
        nonlocal callback_called
        callback_called = True
        assert info is not None
    
    system_monitor.start_monitoring(callback=callback)
    assert callback_called

def test_stop_monitoring(system_monitor):
    """测试停止监控"""
    system_monitor.start_monitoring()
    system_monitor.stop_monitoring()
    assert not system_monitor.is_monitoring

def test_cleanup(system_monitor):
    """测试清理"""
    system_monitor.start_monitoring()
    del system_monitor
    # 验证资源是否被正确清理
    # 这里需要根据具体的实现来验证 