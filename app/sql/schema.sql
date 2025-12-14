-- Database schema generated from request_data.md
-- Generated automatically based on user requirements

-- Table: condenser (冷凝机)
CREATE TABLE `condenser` (
  `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键',
  `model_code` VARCHAR(100) NOT NULL COMMENT '型号编码',
  `applicable_temperature` INT NOT NULL COMMENT '适用库温',
  `compressor_count` INT NOT NULL COMMENT '压缩机数量',
  `fan_count` INT NOT NULL COMMENT '风机数量',
  `suction_inlet` FLOAT NOT NULL COMMENT '吸气进口',
  `liquid_supply_interface` FLOAT NOT NULL COMMENT '液供接口',
  `length` FLOAT NOT NULL COMMENT '长',
  `width` FLOAT NOT NULL COMMENT '宽',
  `height` FLOAT NOT NULL COMMENT '高',
  `installation_height` FLOAT NOT NULL COMMENT '安装尺寸高',
  `installation_width` FLOAT NOT NULL COMMENT '安装尺寸宽',
  `range` FLOAT NOT NULL COMMENT '射程',
  `coil_defrost_power` FLOAT NOT NULL COMMENT '盘管化霜功率',
  `water_pan_defrost_power` FLOAT NOT NULL COMMENT '水盘化霜功率',
  `refrigeration_capacity` FLOAT NOT NULL COMMENT '制冷量',
  `weight` FLOAT NOT NULL COMMENT '重量',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` TINYINT DEFAULT 0 COMMENT '是否逻辑删除',
  `deleted_at` DATETIME DEFAULT NULL COMMENT '删除时间',
  UNIQUE KEY `uk_condenser_model_code` (`model_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='冷凝机';

-- Table: power_supply (电源)
CREATE TABLE `power_supply` (
  `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键',
  `model_code` VARCHAR(100) NOT NULL COMMENT '型号编码',
  `voltage` FLOAT NOT NULL COMMENT '电压',
  `current` FLOAT NOT NULL COMMENT '电流',
  `power` FLOAT NOT NULL COMMENT '功率',
  `plug_type` TINYINT NOT NULL COMMENT '插头类型',
  `weight` FLOAT NOT NULL COMMENT '重量',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` TINYINT DEFAULT 0 COMMENT '是否逻辑删除',
  `deleted_at` DATETIME DEFAULT NULL COMMENT '删除时间',
  UNIQUE KEY `uk_power_supply_model_code` (`model_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='电源';

-- Table: compressor (压缩机)
CREATE TABLE `compressor` (
  `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键',
  `model_code` VARCHAR(100) NOT NULL COMMENT '型号编码',
  `type` TINYINT NOT NULL COMMENT '类型',
  `compression_ratio` FLOAT NOT NULL COMMENT '压缩比',
  `working_pressure` FLOAT NOT NULL COMMENT '工作压力',
  `working_flow` FLOAT NOT NULL COMMENT '工作流量',
  `working_efficiency` FLOAT NOT NULL COMMENT '工作效率',
  `installation_height` FLOAT NOT NULL COMMENT '安装尺寸高',
  `installation_width` FLOAT NOT NULL COMMENT '安装尺寸宽',
  `installation_depth` FLOAT NOT NULL COMMENT '安装尺寸深',
  `weight` FLOAT NOT NULL COMMENT '重量',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` TINYINT DEFAULT 0 COMMENT '是否逻辑删除',
  `deleted_at` DATETIME DEFAULT NULL COMMENT '删除时间',
  UNIQUE KEY `uk_compressor_model_code` (`model_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='压缩机';

-- Table: fan (风机)
CREATE TABLE `fan` (
  `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键',
  `name` VARCHAR(100) NOT NULL COMMENT '名称',
  `model_code` VARCHAR(100) NOT NULL COMMENT '型号编码',
  `type` TINYINT NOT NULL COMMENT '类型',
  `working_voltage` FLOAT NOT NULL COMMENT '工作电压',
  `working_power` FLOAT NOT NULL COMMENT '工作功率',
  `installation_height` FLOAT NOT NULL COMMENT '安装尺寸高',
  `installation_width` FLOAT NOT NULL COMMENT '安装尺寸宽',
  `installation_depth` FLOAT NOT NULL COMMENT '安装尺寸深',
  `weight` FLOAT NOT NULL COMMENT '重量',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` TINYINT DEFAULT 0 COMMENT '是否逻辑删除',
  `deleted_at` DATETIME DEFAULT NULL COMMENT '删除时间',
  UNIQUE KEY `uk_fan_model_code` (`model_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='风机';

-- Table: evaporator (蒸发器)
CREATE TABLE `evaporator` (
  `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键',
  `name` VARCHAR(100) NOT NULL COMMENT '名称',
  `model_code` VARCHAR(100) NOT NULL COMMENT '型号编码',
  `type` TINYINT NOT NULL COMMENT '类型',
  `working_voltage` FLOAT NOT NULL COMMENT '工作电压',
  `working_power` FLOAT NOT NULL COMMENT '工作功率',
  `installation_height` FLOAT NOT NULL COMMENT '安装尺寸高',
  `installation_width` FLOAT NOT NULL COMMENT '安装尺寸宽',
  `installation_depth` FLOAT NOT NULL COMMENT '安装尺寸深',
  `weight` FLOAT NOT NULL COMMENT '重量',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` TINYINT DEFAULT 0 COMMENT '是否逻辑删除',
  `deleted_at` DATETIME DEFAULT NULL COMMENT '删除时间',
  UNIQUE KEY `uk_evaporator_model_code` (`model_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='蒸发器';

-- Table: image (图片)
CREATE TABLE `image` (
  `id` INT PRIMARY KEY AUTO_INCREMENT COMMENT '自增主键',
  `related_id` VARCHAR(255) NOT NULL COMMENT '关联id',
  `image_url` VARCHAR(255) NOT NULL COMMENT '图片URL',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` TINYINT DEFAULT 0 COMMENT '是否逻辑删除',
  `deleted_at` DATETIME DEFAULT NULL COMMENT '删除时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='图片';
