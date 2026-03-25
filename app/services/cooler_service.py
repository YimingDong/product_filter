from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid

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
        delta_t = abs(filter_params.repo_temp - filter_params.evaporating_temp)
        working_status = SCLevel.get_level_by_value(filter_params.evaporating_temp).value
        logger.info(f"working status: {working_status}")
        quant_repo = SCQuantRepository(db)
        q_dto = quant_repo.get_by_evaporating_temp_and_delta_t(filter_params.evaporating_temp, delta_t)
        if not q_dto:
            logger.debug(f"can't find target quant evap_temp: {filter_params.evaporating_temp}, delta_t: {delta_t}")
            raise FilterException(code=500, message="温差过高或过低，请直接联系厂家")
            # q = SCLevel.get_q(filter_params.evaporating_temp, filter_params.refrigerant_supply_type)
        else:
            q = q_dto.quant

        refrigerant_quant = Refrigerant.get_q(filter_params.refrigerant, filter_params.refrigerant_supply_type)

        target_cap = filter_params.required_cooling_cap / q / refrigerant_quant

        cooler_repo = CoolerRepository(db)
        cooler_cap_repo = CoolingCapacityRepository(db)

        cooler_cap_dtos = cooler_cap_repo.get_by_working_status_and_refrigerant(working_status)
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
        res = get_data(target_ids, cooler_dic, filter_params.fan_distance, filter_params.series)

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
    
    @staticmethod
    def get_all_series(db: Session) -> List[str]:
        """获取所有冷风机系列，去重并按字母顺序排序"""
        try:
            cooler_repo = CoolerRepository(db)
            series_list = cooler_repo.get_all_series()
            # 按字母顺序排序
            series_list.sort()
            return series_list
        except Exception as e:
            logger.error(f"Error getting all series: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @staticmethod
    def upload_pdf(db: Session, cooler_id: int, file: UploadFile) -> dict:
        """上传冷风机 PDF 文件"""
        try:
            # 验证文件类型
            if not file.filename.endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Only PDF files are allowed")
            
            # 生成唯一的文件名
            file_extension = file.filename.split('.')[-1]
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            
            # 确保 doc 目录存在
            doc_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'doc')
            os.makedirs(doc_dir, exist_ok=True)
            
            # 保存文件
            file_path = os.path.join(doc_dir, unique_filename)
            with open(file_path, 'wb') as buffer:
                content = file.file.read()
                buffer.write(content)
            
            # 生成相对路径
            relative_path = f"doc/{unique_filename}"
            
            # 更新数据库
            cooler_repo = CoolerRepository(db)
            cooler = cooler_repo.update_pdf_path(cooler_id, relative_path)
            
            if not cooler:
                # 如果 cooler 不存在，删除已保存的文件
                os.remove(file_path)
                raise HTTPException(status_code=404, detail=f"Cooler with id {cooler_id} not found")
            
            logger.info(f"PDF uploaded successfully for cooler {cooler_id}: {relative_path}")
            
            return {
                "cooler_id": cooler_id,
                "pdf_path": relative_path
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error uploading PDF: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    @staticmethod
    def get_pdf_file(cooler_id: int, db: Session) -> tuple:
        """获取冷风机 PDF 文件路径和文件名"""
        try:
            cooler_repo = CoolerRepository(db)
            cooler = cooler_repo.get_by_id(cooler_id)
            
            if not cooler:
                raise HTTPException(status_code=404, detail=f"Cooler with id {cooler_id} not found")
            
            if not cooler.pdf_path:
                raise HTTPException(status_code=404, detail=f"No PDF file found for cooler {cooler_id}")
            
            # 构建完整文件路径
            # 数据库存储的是 Linux 格式路径 (doc/xxx.pdf)，需要转换为当前系统的路径格式
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            # 将 Linux 路径分隔符替换为当前系统的分隔符
            relative_path = cooler.pdf_path.replace('/', os.sep).replace('\\', os.sep)
            file_path = os.path.join(base_dir, relative_path)
            
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"PDF file not found: {file_path}")
            
            # 提取文件名
            filename = "text"
            
            return file_path, filename
        except HTTPException:
            raise
        except FileNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error getting PDF file: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")


def get_data(target_ids: list[str], cooler_dic: dict, fan_distance: float, series: str = None):
    res = []
    for target_id in target_ids:

        if target_id not in cooler_dic:
            continue
        coolers = cooler_dic[target_id]
        for cooler in coolers:
            if fan_distance and cooler.fin_spacing_num != fan_distance:
                continue
            if series and cooler.series != series:
                continue
            if len(res) > 5:
                return res
            res.append(cooler)
    return res
