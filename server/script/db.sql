create table pay_app
(
    id             bigint unsigned not null auto_increment comment '自增主键',
    appname        varchar(32)     not null default '' comment 'app名称',
    pay_appid      char(16)        not null default '' comment '项目appid',
    pay_secret_key char(32)        not null default '' comment 'secret_key',
    allow_payment  char(1)         not null default 'Y' comment '是否允许付款，Y 允许退款；N 不允许退款',
    allow_refund   char(1)         not null default 'N' comment '是否允许退款，Y 允许退款；N 不允许退款',
    create_time    int unsigned    not null default 0 comment '创建时间',
    update_time    int unsigned    not null default 0 comment '更新时间',
    delete_time    int unsigned    not null default 0 comment '删除时间',
    unique key (pay_appid),
    primary key (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4 COMMENT ='app表';

create table pay_wx_mch_cfg
(
    id            bigint unsigned not null auto_increment comment '自增主键',
    cfg_name      varchar(32)     not null default '' comment '配置名称',
    mch_id        varchar(16)     not null default '' comment '商户ID',
    mch_v3_key    varchar(64)     not null default '' comment '商户APIv3密钥',
    mch_pk_path   varchar(128)    not null default '' comment '商户API证书私钥路径',
    mch_serial_no varchar(64)     not null default '' comment '商户API证书序列号',
    create_time   int unsigned    not null default 0 comment '创建时间',
    update_time   int unsigned    not null default 0 comment '更新时间',
    delete_time   int unsigned    not null default 0 comment '删除时间',
    primary key (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4 COMMENT ='微信支付商户后台配置 pay.weixin.qq.com';

create table pay_wx_mp_cfg
(
    id               bigint unsigned not null auto_increment comment '自增主键',
    cfg_name         varchar(32)     not null default '' comment '配置名称',
    mp_appid         varchar(32)     not null default '' comment '公众号开发者ID(AppID)',
    mp_app_secret    varchar(64)     not null default '' comment '公众号开发者密码(AppSecret)',
    auth_url_path    varchar(64)     not null default '' comment '如：MP_verify_Sgz1uuMyJEr8yF5c.txt',
    auth_content     varchar(64)     not null default '' comment 'auth_url_path的内容',
    encoding_aes_key varchar(64)     not null default '' comment '设置与开发-基本配置-服务器配置-消息加解密密钥',
    create_time      int unsigned    not null default 0 comment '创建时间',
    update_time      int unsigned    not null default 0 comment '更新时间',
    delete_time      int unsigned    not null default 0 comment '删除时间',
    primary key (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4 COMMENT ='微信公众号后台配置 mp.weixin.qq.com';

create table pay_wx_miniapp_cfg
(
    id            bigint unsigned not null auto_increment comment '自增主键',
    cfg_name      varchar(32)     not null default '' comment '配置名称',
    mp_appid      varchar(32)     not null default '' comment '小程序开发者ID(AppID)',
    mp_app_secret varchar(64)     not null default '' comment '小程序开发者密码(AppSecret)',
    create_time   int unsigned    not null default 0 comment '创建时间',
    update_time   int unsigned    not null default 0 comment '更新时间',
    delete_time   int unsigned    not null default 0 comment '删除时间',
    primary key (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4 COMMENT ='微信小程序后台配置 mp.weixin.qq.com';

create table pay_wx_open_cfg
(
    id          bigint unsigned not null auto_increment comment '自增主键',
    cfg_name    varchar(32)     not null default '' comment '配置名称',
    open_appid  varchar(32)     not null default '' comment '开放平台 AppID',
    create_time int unsigned    not null default 0 comment '创建时间',
    update_time int unsigned    not null default 0 comment '更新时间',
    delete_time int unsigned    not null default 0 comment '删除时间',
    primary key (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4 COMMENT ='微信开放平台配置 open.weixin.qq.com';

create table pay_cfg
(
    id          bigint unsigned not null auto_increment comment '自增主键',
    pay_appid   char(16)        not null default '' comment '项目appid',
    pt          varchar(16)     not null default '' comment '支付平台 wx_mp_cfg 微信公众支付；wx_miniapp_cfg 微信公众支付；wx_open_cfg 微信app支付；alipay_cfg 支付宝支付',
    tp          varchar(16)     not null default '' comment '支付方式 h5；mp；miniapp；app；pc',
    cfg_id      bigint unsigned not null default 0 comment '配置ID',
    create_time int unsigned    not null default 0 comment '创建时间',
    update_time int unsigned    not null default 0 comment '更新时间',
    delete_time int unsigned    not null default 0 comment '删除时间',
    primary key (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4 COMMENT ='支付配置';

create table pay_unified_order
(
    id               bigint unsigned not null auto_increment comment '自增主键',
    pay_appid        char(16)        not null default '' comment '项目appid',
    unified_order_id varchar(64)     not null default '' comment '统一订单ID',
    pay_order_id     varchar(64)     not null default '' comment '支付订单ID',
    amount           bigint unsigned not null default 0 comment '订单金额(分)',
    refund_amount    bigint unsigned not null default 0 comment '已退款金额（分）',
    pay_time         int unsigned    not null default 0 comment '支付时间',
    expire_time      int unsigned    not null default 0 comment ' 过期时间 ',
    last_refund_time int unsigned    not null default 0 comment '上一次退款时间',
    extra            varchar(512)    not null default '' comment '额外参数，回调原样返回',
    notify_url       varchar(256)    not null default '' comment '回调地址',
    return_url       varchar(256)    not null default '' comment '支付成功地址',
    create_time      int unsigned    not null default 0 comment ' 创建时间 ',
    update_time      int unsigned    not null default 0 comment ' 更新时间 ',
    unique key (unified_order_id),
    primary key (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4 COMMENT ='统一订单 ';

create table pay_order
(
    id               bigint unsigned not null auto_increment comment '自增主键',
    pay_appid        char(16)        not null default '' comment '项目appid',
    cfg_id           bigint unsigned not null default 0 comment 'pay_cfg.id',
    pay_order_id     varchar(64)     not null default '' comment '支付订单ID',
    unified_order_id varchar(64)     not null default '' comment '支付订单ID',
    pay_content      varchar(512)    not null default '' comment '支付请求内容',
    notify_content   varchar(512)    not null default '' comment '支付回调内容',
    last_notify_time int unsigned    not null default 0 comment ' 创建时间 ',
    create_time      int unsigned    not null default 0 comment ' 创建时间 ',
    update_time      int unsigned    not null default 0 comment ' 更新时间 ',
    unique key (pay_order_id),
    primary key (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4 COMMENT ='支付订单';

create table pay_access_token
(
    id           bigint unsigned not null auto_increment comment '自增主键',
    pt           varchar(16)     not null default '' comment '支付平台 wx_mp_cfg 微信公众支付；wx_miniapp_cfg 微信公众支付；wx_open_cfg 微信app支付；alipay_cfg 支付宝支付',
    appid        varchar(32)     not null default '' comment '发者ID(AppID)',
    access_token varchar(256)    not null default '' comment '令牌',
    expire_time  bigint unsigned not null default 0 comment '过期间隔',
    create_time  int unsigned    not null default 0 comment ' 创建时间 ',
    primary key (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4 COMMENT ='Access Token';

###############################################

create table pay_alipay_cfg
(
    id          bigint unsigned not null auto_increment comment '自增主键',
    cfg_name    varchar(32)     not null default '' comment '配置名称',
    create_time int unsigned    not null default 0 comment '创建时间',
    update_time int unsigned    not null default 0 comment '更新时间',
    delete_time int unsigned    not null default 0 comment '删除时间',
    primary key (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4 COMMENT ='支付宝支付配置';

create table pay_refund_order
(
    id              bigint unsigned not null auto_increment comment '自增主键',
    refund_order_id varchar(64)     not null default '' comment '支付订单ID',
    refund_amount   bigint unsigned not null default 0 comment '退款金额',
    create_time     int unsigned    not null default 0 comment ' 创建时间 ',
    update_time     int unsigned    not null default 0 comment ' 更新时间 ',
    primary key (id)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4 COMMENT ='退款订单';