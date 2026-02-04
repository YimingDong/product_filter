from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.repositories import SCQuantRepository, CoolerRepository, CoolingCapacityRepository
from app.schemas.product import CoolerFilter
from app.utils.enums import SCLevel, Refrigerant
from app.utils.error_handlers import FilterException
from app.utils.logger import logger

N = 6

class CoolerService:
    """产品服务类"""
    @staticmethod
    def filter_cooler(db: Session, filter_params: CoolerFilter) -> dict:
        """过滤产品"""
        logger.info("aaaa")
        delta_t = filter_params.repo_temp - filter_params.evaporating_temp
        working_status = SCLevel.get_level_by_value(filter_params.evaporating_temp).value
        logger.info(f"working status: {working_status}")
        quant_repo = SCQuantRepository(db)
        q_dto = quant_repo.get_by_evaporating_temp_and_delta_t(filter_params.evaporating_temp, delta_t)
        if not q_dto:
            logger.debug(f"can't find target quant evap_temp: {filter_params.evaporating_temp}, delta_t: {delta_t}")
            raise FilterException(code=500, message="温度过高或过低，请直接联系厂家")
            # q = SCLevel.get_q(filter_params.evaporating_temp, filter_params.refrigerant_supply_type)
        else:
            q = q_dto.quant

        refrigerant_quant = Refrigerant.get_q(filter_params.refrigerant, filter_params.refrigerant_supply_type)

        target_cap = filter_params.required_cooling_cap / q / refrigerant_quant

        cooler_repo = CoolerRepository(db)
        cooler_cap_repo = CoolingCapacityRepository(db)

        cooler_cap_dtos = cooler_cap_repo.get_by_working_status_and_refrigerant(working_status, filter_params.refrigerant)
        logger.info(cooler_cap_dtos)
        cooler_id_cap_map = {}
        allowed_cooler = []
        for cap in cooler_cap_dtos:
            delta = abs(cap.capacity - target_cap)
            if cap.cooler_id in cooler_id_cap_map:
                continue
            allowed_cooler.append((cap.cooler_id, delta))
            cooler_id_cap_map[cap.cooler_id] = cap
        sorted_allowed_cooler = sorted(allowed_cooler, key=lambda x: x[1])
        target_ids = [element[0] for element in sorted_allowed_cooler]
        coolers = cooler_repo.get_by_cooler_ids(target_ids)
        cooler_dic = {}
        for cooler in coolers:
            if cooler.model not in cooler_dic:
                cooler_dic[cooler.model] = []
            cooler_dic[cooler.model].append(cooler)
        res = get_data(target_ids, cooler_dic, filter_params.fan_distance)

        # 计算总数
        total = len(res)

        # # 应用分页
        # skip = (pagination.page - 1) * pagination.size
        # items = query.offset(skip).limit(pagination.size).all()
        #
        # # 计算总页数
        # pages = (total + pagination.size - 1) // pagination.size
        print(len(res))
        return {
            "items": [cooler.to_pydantic(cooler_id_cap_map[cooler.model].capacity,
                                         cooler_id_cap_map[cooler.model].working_status) for cooler in res],
            "total": total
        }


def get_data(target_ids: list[str], cooler_dic: dict, fan_distance: float):
    res = []
    for target_id in target_ids:

        if target_id not in cooler_dic:
            continue
        coolers = cooler_dic[target_id]
        for cooler in coolers:
            if fan_distance and cooler.fin_spacing_num != fan_distance:
                continue
            if len(res) > 5:
                return res
            res.append(cooler)
    return res
