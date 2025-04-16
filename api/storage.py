# storage.py
from typing import Dict, Any
import uuid

# 全局内存存储（线程安全建议使用 threading.Lock 或 multiprocessing.Manager 的 dict）
data_store: Dict[str, Any] = {}

def save_data(data: Any) -> str:
    """保存数据并返回唯一ID"""
    data_id = str(uuid.uuid4())
    data_store[data_id] = data
    return data_id

def get_data(data_id: str) -> Any:
    """根据ID获取数据"""
    return data_store.get(data_id)