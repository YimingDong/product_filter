from enum import Enum
from typing import Dict, Tuple, Optional


class SCLevel(Enum):
    """温度等级枚举"""
    SC1 = "SC1"
    SC2 = "SC2"
    SC3 = "SC3"
    SC4 = "SC4"
    SC5 = "SC5"

    @classmethod
    def get_level_by_value(cls, value: float) -> Optional['SCLevel']:
        """根据温度值获取等级"""
        if value > 10:
            raise ValueError(f"{value}在范围之外")
        if -4 <= value <= 10:
            return cls.SC1
        elif -15 <= value <= -5:
            return cls.SC2
        elif -27 <= value <= -16:
            return cls.SC3
        elif -35 <= value <= -28:
            return cls.SC4
        else:
            return cls.SC5

    @classmethod
    def from_value(cls, value):
        """通过值获取枚举"""
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"{value} is not a valid {cls.__name__}")

    @classmethod
    def get_q(cls, evap_temp: float, refrigerant_supply_type: str):
        target_refrigerant = cls.get_level_by_value(evap_temp)
        target_refrigerant_supply_type = RefrigerantSupplyType.from_value(refrigerant_supply_type)
        q = {
            cls.SC1: {
                RefrigerantSupplyType.DIRECT: 1.481,
                RefrigerantSupplyType.PUMP: 1.403
            },
            cls.SC2: {
                RefrigerantSupplyType.DIRECT: 1.0,
                RefrigerantSupplyType.PUMP: 1.005
            },
            cls.SC3: {
                RefrigerantSupplyType.DIRECT: 0.769,
                RefrigerantSupplyType.PUMP: 0.758
            },
            cls.SC4: {
                RefrigerantSupplyType.DIRECT: 0.638,
                RefrigerantSupplyType.PUMP: 0.616
            },
            cls.SC5: {
                RefrigerantSupplyType.DIRECT: 0.603,
                RefrigerantSupplyType.PUMP: 0.6
            }

        }
        return q.get(target_refrigerant).get(target_refrigerant_supply_type)


class Refrigerant(Enum):
    """制冷剂等级枚举"""
    R404A = "R404A"
    R22 = "R22"
    R407C = "R407C"
    R410A = "R410A"
    R507C = "R507C"
    R23 = "R23"

    @classmethod
    def from_value(cls, value):
        """通过值获取枚举"""
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"{value} is not a valid {cls.__name__}")

    @classmethod
    def get_q(cls, refrigerant: str, refrigerant_supply_type: str):
        target_refrigerant = cls.from_value(refrigerant)
        target_refrigerant_supply_type = RefrigerantSupplyType.from_value(refrigerant_supply_type)
        q = {
            cls.R404A: {
                RefrigerantSupplyType.DIRECT: 1.0,
                RefrigerantSupplyType.PUMP: 1.005
            },
            cls.R22: {
                RefrigerantSupplyType.DIRECT: 0.927,
                RefrigerantSupplyType.PUMP: 0.999
            },
            cls.R407C: {
                RefrigerantSupplyType.DIRECT: 0.98,
                RefrigerantSupplyType.PUMP: 1.027
            },
            cls.R410A: {
                RefrigerantSupplyType.DIRECT: 0.995,
                RefrigerantSupplyType.PUMP: 1.066
            },
            cls.R507C: {
                RefrigerantSupplyType.DIRECT: 0.961,
                RefrigerantSupplyType.PUMP: 0.999
            },
            cls.R23: {
                RefrigerantSupplyType.DIRECT: 1.017,
                RefrigerantSupplyType.PUMP: 1.099
            },

        }
        return q.get(target_refrigerant).get(target_refrigerant_supply_type)


class RefrigerantSupplyType(Enum):
    """制冷量等级枚举"""
    DIRECT = "直膨"
    PUMP = "泵供液"

    @classmethod
    def from_value(cls, value):
        """通过值获取枚举"""
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"{value} is not a valid {cls.__name__}")


if __name__ == '__main__':
    print(Refrigerant.get_q("R404A", "直膨"))
    print(SCLevel.get_q(5, "直膨"))
