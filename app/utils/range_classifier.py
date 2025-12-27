from typing import Type, TypeVar, Optional, List, Tuple, Dict, Any
from enum import Enum
from app.utils.enums import (
    TemperatureLevel,
    CapacityLevel,
    PressureLevel,
    FlowLevel,
    EfficiencyLevel,
    PowerLevel,
    WorkingStatus,
    SizeLevel
)

T = TypeVar('T', bound=Enum)


def get_enum_by_range(
    value: float,
    enum_class: Type[T],
    custom_ranges: Optional[List[Tuple[float, float, T]]] = None
) -> Optional[T]:
    """
    根据数字范围返回对应的枚举值
    
    Args:
        value: 要判断的数字值
        enum_class: 枚举类类型
        custom_ranges: 自定义范围列表，每个元素为 (最小值, 最大值, 枚举值) 的元组
    
    Returns:
        对应的枚举值，如果不在任何范围内则返回None
    
    Example:
        # 使用预定义的枚举类
        level = get_enum_by_range(15, TemperatureLevel)
        # 返回 TemperatureLevel.HIGH
        
        # 使用自定义范围
        custom_ranges = [
            (0, 10, MyEnum.SMALL),
            (10, 100, MyEnum.MEDIUM),
            (100, float('inf'), MyEnum.LARGE)
        ]
        level = get_enum_by_range(50, MyEnum, custom_ranges)
    """
    if custom_ranges:
        for min_val, max_val, enum_value in custom_ranges:
            if min_val <= value < max_val:
                return enum_value
        return None
    
    if hasattr(enum_class, 'get_level_by_value'):
        return enum_class.get_level_by_value(value)
    
    return None


def get_enum_by_value(
    value: Any,
    enum_class: Type[T]
) -> Optional[T]:
    """
    根据值直接获取枚举
    
    Args:
        value: 要匹配的值
        enum_class: 枚举类类型
    
    Returns:
        对应的枚举值，如果匹配失败则返回None
    
    Example:
        status = get_enum_by_value("SC1", WorkingStatus)
        # 返回 WorkingStatus.SC1
    """
    try:
        return enum_class(value)
    except (ValueError, KeyError):
        return None


def get_temperature_level(temperature: float) -> Optional[TemperatureLevel]:
    """
    根据温度值获取温度等级
    
    Args:
        temperature: 温度值（摄氏度）
    
    Returns:
        温度等级枚举
    """
    return get_enum_by_range(temperature, TemperatureLevel)


def get_capacity_level(capacity: float) -> Optional[CapacityLevel]:
    """
    根据制冷量值获取制冷量等级
    
    Args:
        capacity: 制冷量值（KW）
    
    Returns:
        制冷量等级枚举
    """
    return get_enum_by_range(capacity, CapacityLevel)


def get_pressure_level(pressure: float) -> Optional[PressureLevel]:
    """
    根据压力值获取压力等级
    
    Args:
        pressure: 压力值（MPa）
    
    Returns:
        压力等级枚举
    """
    return get_enum_by_range(pressure, PressureLevel)


def get_flow_level(flow: float) -> Optional[FlowLevel]:
    """
    根据流量值获取流量等级
    
    Args:
        flow: 流量值（m³/h）
    
    Returns:
        流量等级枚举
    """
    return get_enum_by_range(flow, FlowLevel)


def get_efficiency_level(efficiency: float) -> Optional[EfficiencyLevel]:
    """
    根据效率值获取效率等级
    
    Args:
        efficiency: 效率值（百分比）
    
    Returns:
        效率等级枚举
    """
    return get_enum_by_range(efficiency, EfficiencyLevel)


def get_power_level(power: float) -> Optional[PowerLevel]:
    """
    根据功率值获取功率等级
    
    Args:
        power: 功率值（kW）
    
    Returns:
        功率等级枚举
    """
    return get_enum_by_range(power, PowerLevel)


def get_working_status(status: str) -> Optional[WorkingStatus]:
    """
    根据工况字符串获取工况枚举
    
    Args:
        status: 工况字符串（如"SC1"）
    
    Returns:
        工况枚举
    """
    return get_enum_by_value(status, WorkingStatus)


def get_size_level(size: float) -> Optional[SizeLevel]:
    """
    根据尺寸值获取尺寸等级
    
    Args:
        size: 尺寸值（mm）
    
    Returns:
        尺寸等级枚举
    """
    return get_enum_by_range(size, SizeLevel)


def classify_by_ranges(
    value: float,
    ranges: Dict[str, Tuple[float, float]]
) -> Optional[str]:
    """
    根据自定义范围对数值进行分类
    
    Args:
        value: 要分类的数值
        ranges: 范围字典，格式为 {分类名称: (最小值, 最大值)}
    
    Returns:
        分类名称，如果不在任何范围内则返回None
    
    Example:
        ranges = {
            "小型": (0, 10),
            "中型": (10, 50),
            "大型": (50, 100),
            "超大型": (100, float('inf'))
        }
        category = classify_by_ranges(25, ranges)
        # 返回 "中型"
    """
    for category, (min_val, max_val) in ranges.items():
        if min_val <= value < max_val:
            return category
    return None


def get_all_enum_values(enum_class: Type[T]) -> List[T]:
    """
    获取枚举类的所有枚举值
    
    Args:
        enum_class: 枚举类类型
    
    Returns:
        枚举值列表
    """
    return list(enum_class)


def get_enum_value_mapping(enum_class: Type[T]) -> Dict[Any, T]:
    """
    获取枚举类的值到枚举的映射
    
    Args:
        enum_class: 枚举类类型
    
    Returns:
        值到枚举的映射字典
    """
    return {enum_value.value: enum_value for enum_value in enum_class}
