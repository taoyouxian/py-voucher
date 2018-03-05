--首先需要创建这两个表
CREATE TABLE `t_publish_detail` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT comment '主键',
  `name` varchar(63) DEFAULT NULL comment '企业名称',
  `code` varchar(63) DEFAULT NULL comment '组织机构代码',
  `date` datetime DEFAULT NULL comment '处罚处理时间',
  `branch` varchar(63) DEFAULT NULL comment '处罚处理机构',
  `category` varchar(63) DEFAULT NULL comment '行政 处罚种类',
  `content` text comment '处罚内容详情',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=739 DEFAULT CHARSET=utf8;

CREATE TABLE `t_publish_detail_temp` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT comment '主键',
  `name` varchar(63) DEFAULT NULL comment '企业名称',
  `code` varchar(63) DEFAULT NULL comment '组织机构代码',
  `date` datetime DEFAULT NULL comment '处罚处理时间',
  `branch` varchar(63) DEFAULT NULL comment '处罚处理机构',
  `category` varchar(63) DEFAULT NULL comment '行政 处罚种类',
  `content` text comment '处罚内容详情',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=739 DEFAULT CHARSET=utf8;

CREATE TABLE `douban` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT comment '主键',
  `title` varchar(63) DEFAULT NULL,
  `abstract` varchar(63) DEFAULT NULL,
  `content` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

