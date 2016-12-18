# 创建用户
create table bank_user(
	use_id int not null PRIMARY KEY AUTO_INCREMENT,
	username varchar(100) NOT NULL,
	password varchar(100) NOT NULL,
	money int(100) not null default 0,
	create_time timestamp not null default now() 
);
# 修改钱数的默认值
# alter table bank_user alter column money set default 100;
# 创建管理员
create table bank_manager(
	user_id int not null PRIMARY KEY AUTO_INCREMENT,
	username varchar(100) NOT NULL,
	password varchar(100) NOT NULL,
	create_time timestamp NOT NULL default now()
);

# 相关操作
create table some_operation(
	user_id int not null PRIMARY KEY AUTO_INCREMENT,
	username varchar(100) NOT NULL,
	money int NOT NULL default 0,
	time_operate timestamp NOT NULL DEFAULT NOW()
);

# 插入普通用户
sql = "insert into bank_user(username, password) values('%s', '%s');" % (username, password)
# 查找
sql = "select username, password from bank_user;"
# 删除
sql = "delete from bank_user where username = '%s';" % (username,)
# 数据库中添加一列，用于判断当前的一行数据是不是正在使用
alter table bank_user ADD column bool_id tinyint default 0 after money;
# 修改列顺序
ALTER TABLE bank_user MODIFY bool_id boolean_id tinyint default 0 after money;
# 删除一列
alter table bank_user drop bool_id;
# 更新数据
sql_update = "update bank_user set bool_id = 1 where username = '%s';"%

insert into bank_user(username, password) values('小周周', 'zhou');
insert into bank_manager(username, password) values('wuxiushu', 'wuxiushu');

alter table some_operation ADD column receive_username varchar(100) NOT NULL after username;

ALTER TABLE some_operation MODIFY receive_username varchar(100) after username;