from sqlalchemy.orm import Session

from app.models.repositories import SCQuantRepository, CoolerRepository, CoolingCapacityRepository
from app.schemas.product import CoolerFilter
from app.utils.enums import SCLevel, Refrigerant
from app.utils.logger import logger


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
            q = SCLevel.get_q(filter_params.evaporating_temp, filter_params.refrigerant_supply_type)
        else:
            q = q_dto.quant

        refrigerant_quant = Refrigerant.get_q(filter_params.refrigerant, filter_params.refrigerant_supply_type)

        target_cap = filter_params.required_cooling_cap / q / refrigerant_quant

        cooler_repo = CoolerRepository(db)
        cooler_cap_repo = CoolingCapacityRepository(db)

        cooler_cap_dtos = cooler_cap_repo.get_by_working_status_and_refrigerant(working_status, filter_params.refrigerant)
        logger.info(cooler_cap_dtos)
        cooler_ids = []
        allowed_cooler = []
        for cap in cooler_cap_dtos:
            delta = abs(cap.capacity - target_cap)
            allowed_cooler.append((cap.cooler_id, delta))
        sorted_allowed_cooler = sorted(allowed_cooler, key=lambda x: x[1])
        top5 = [element[0] for element in sorted_allowed_cooler[:5]]
        coolers = cooler_repo.get_by_cooler_ids(top5)

        # 计算总数
        total = len(coolers)

        # # 应用分页
        # skip = (pagination.page - 1) * pagination.size
        # items = query.offset(skip).limit(pagination.size).all()
        #
        # # 计算总页数
        # pages = (total + pagination.size - 1) // pagination.size
        print(len(coolers))
        return {
            "items": [cooler.to_pydantic() for cooler in coolers],
            "total": total
        }

