CREATE TABLE cooler (
	id BIGINT UNSIGNED auto_increment NOT NULL COMMENT 'pk',
	heat_exchange_area FLOAT NOT NULL COMMENT '换热面积',
	tube_volumn FLOAT NULL COMMENT '管容(dm³)',
	air_flow_rate FLOAT NULL COMMENT '风量(m³/h)',
	total_fan_power varchar(100) NULL COMMENT '电机总功率(kW)',
	total_fan_current varchar(100) NULL COMMENT '电机总电流(A)',
	air_flow FLOAT NULL COMMENT '射程(m)',
	defrost_water_flow_rate FLOAT NULL COMMENT '冲霜水量(m³/h)',
	pipe_dia varchar(100) NULL COMMENT '接口管径(进/出Φmm）',
	noise FLOAT NULL COMMENT '噪音(dB)(5米)',
	weight FLOAT NULL COMMENT '重量(kg）',
	model varchar(100) NULL COMMENT '型号',
	fin_spacing varchar(100) NULL COMMENT '翅片间距',
	series varchar(100) NULL COMMENT '系列',
	create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '创建时间',
	update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP NOT NULL,
	is_deleted TINYINT DEFAULT 0 NULL COMMENT '逻辑删除',
	comment varchar(255) NULL COMMENT '参数注释',
	CONSTRAINT cooler_pk PRIMARY KEY (id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci
COMMENT='冷风机';

CREATE TABLE cooling_capacity (
	id BIGINT UNSIGNED auto_increment NOT NULL COMMENT 'pk',
	cooler_id varchar(255) NOT NULL COMMENT '冷风机的id',
	working_status varchar(100) NOT NULL COMMENT '工况：SC1;SC2;SC3;SC4;SC5',
	capacity FLOAT NOT NULL COMMENT '制冷量（KW）',
	created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL COMMENT '创建时间',
	updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP NULL COMMENT '更新时间',
	is_deleted TINYINT DEFAULT 0 NULL COMMENT '逻辑删除',
	CONSTRAINT cooling_capacity_pk PRIMARY KEY (id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci
COMMENT='冷量映射表';