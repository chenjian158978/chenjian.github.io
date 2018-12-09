---
layout:     post
title:      "使用Golang操作PostgreSQL数据库的增删改查"
subtitle:   "CRUD Of PostgreSQL By Golang"
date:       Sat, Nov 24 2018 07:59:45 GMT+8
author:     "ChenJian"
header-img: "img/in-post/CRUD-Of-PostgreSQL-By-Golang/head_blog.jpg"
catalog:    true
tags: [工作, Linux]
---

### PG驱动库包github.com/lib/pq

该驱动包没有提供创建PG表结构的函数，因此需要手动创建。SQL文件如下：

##### node_infos.sql

``` sql
---------------------------
---postgresql SQL by Chen Jian
---------------------------
drop table if exists "node_infos";

CREATE TABLE "node_infos"(
    "node_name" varchar(45) PRIMARY KEY,
    "node_ip" varchar(45) NOT NULL,
    "node_port" varchar(45) NOT NULL,
    "node_username" varchar(45) NOT NULL,
    "node_password" varchar(255) NOT NULL

);

COMMENT ON COLUMN "node_infos"."node_name" is '节点名称';
COMMENT ON COLUMN "node_infos"."node_ip" is '节点IP地址';
COMMENT ON COLUMN "node_infos"."node_port" is '节点端口号';
COMMENT ON COLUMN "node_infos"."node_username" is '节点用户名';
COMMENT ON COLUMN "node_infos"."node_password" is '节点密码';

INSERT INTO node_infos(node_name, node_ip, node_port, node_username, node_password)
VALUES ('chen', '10.16.11.92', '22', 'root', 'xxxx');

INSERT INTO node_infos(node_name, node_ip, node_port, node_username, node_password)
VALUES ('jian', '10.16.11.94', '22', 'root', 'xxxx');

INSERT INTO node_infos(node_name, node_ip, node_port, node_username, node_password)
VALUES ('blabla', '10.16.11.95', '22', 'root', 'xxxx');
```

##### PGs数据库的简单操作

``` shell
# 进入PG数据库
psql -U postgres

# 查看当前数据库：
\l;

<<'COMMENT'
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
-----------+----------+----------+------------+------------+-----------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
(3 rows)
COMMENT

# 链接数据库postgres
\c postgres;

<<'COMMENT'
You are now connected to database "postgres" as user "postgres".
COMMENT

# 创建表
\i node_infos.sql;

# 结果输出
psql:node_infos.sql:4: NOTICE:  table "node_infos" does not exist, skipping
DROP TABLE
CREATE TABLE
COMMENT
COMMENT
COMMENT
COMMENT
COMMENT
INSERT 0 1
INSERT 0 1
INSERT 0 1

# 查看当前表
\dt;

<<'COMMENT'
           List of relations
 Schema |    Name    | Type  |  Owner   
--------+------------+-------+----------
 public | node_infos | table | postgres
(1 row)
COMMENT

# 查看表结构
\d node_infos;

<<'COMMENT'
             Table "public.node_infos"
    Column     |          Type          | Modifiers 
---------------+------------------------+-----------
 node_name     | character varying(45)  | not null
 node_ip       | character varying(45)  | not null
 node_port     | character varying(45)  | not null
 node_username | character varying(45)  | not null
 node_password | character varying(255) | not null
Indexes:
    "node_infos_pkey" PRIMARY KEY, btree (node_name)
COMMENT

# 查看表中所有数据
select * from node_infos;

<<'COMMENT'
 node_name |   node_ip   | node_port | node_username | node_password 
-----------+-------------+-----------+---------------+---------------
 chen      | 10.16.11.92 | 22        | root          | xxxx
 jian      | 10.16.11.94 | 22        | root          | xxxx
 blabla    | 10.16.11.95 | 22        | root          | xxxx
(3 rows)
COMMENT

# 删除表
drop table node_infos;

<<'COMMENT'
DROP TABLE
COMMENT

# 退出PG数据库
\q;
```

##### CRUD代码

``` golang
package main

/*
Author: Chen Jian
Blog:   https://www.o-my-chenjian.com
Date:   2018-11-20
*/

import (
	"fmt"
	"log"

	"database/sql"

	_ "github.com/lib/pq"
)

var db *sql.DB
var err error

// PGs数据库信息
const (
	pg_host     = "10.16.11.95"
	pg_port     = 5432
	pg_user     = "postgres"
	pg_password = "postgres"
	pg_dbname   = "postgres"
)

func InsertNodeInfo() error {
	stmt, err := db.Prepare("INSERT INTO \"node_infos\"(\"node_name\", \"node_ip\", \"node_port\", \"node_username\", \"node_password\") VALUES ($1, $2, $3, $4, $5)")
	if err != nil {
		log.Fatal("PG Statements Wrong: ", err)
	}

	res, err := stmt.Exec("nicai", "10.51.42.66", "9999", "nicai", "gophdddeer")
	if err != nil {
		log.Fatal("PG Statements Exec Wrong: ", err)
	}

	id, err := res.RowsAffected()
	if err != nil {
		log.Fatal("PG Affecte Wrong: ", err)
	}

	fmt.Println(id)
	return nil
}

func DeleteNodeInfo() error {
	stmt, err := db.Prepare("DELETE FROM \"node_infos\" WHERE \"node_name\" = $1")
	if err != nil {
		log.Fatal("PG Statements Wrong: ", err)
	}

	res, err := stmt.Exec("nicai")
	if err != nil {
		log.Fatal("PG Statements Exec Wrong: ", err)
	}

	id, err := res.RowsAffected()
	if err != nil {
		log.Fatal("PG Affecte Wrong: ", err)
	}

	fmt.Println(id)
	return nil
}

func SelectAllNodeInfo() error {
	rows, err := db.Query("SELECT * FROM  \"node_infos\"")
	if err != nil {
		log.Fatal("PG Statements Wrong: ", err)
	}

	for rows.Next() {
		var nodename string
		var nodeip string
		var nodeport string
		var nodeusername string
		var nodepassword string

		if err := rows.Scan(&nodename, &nodeip, &nodeport, &nodeusername, &nodepassword); err != nil {
			log.Fatal("PG Rows Scan Failed: ", err)
		}

		fmt.Printf("node_name = \"%s\", "+
			"node_ip = \"%s\", "+
			"node_port = \"%s\", "+
			"node_username = \"%s\", "+
			"node_password = \"%s\"\n", nodename, nodeip, nodeport, nodeusername, nodepassword)
	}

	if err := rows.Err(); err != nil {
		log.Fatal("PG Query Failed: ", err)
	}

	rows.Close()
	db.Close()
	return nil
}

func UpdateNodeInfo() error {
	stmt, err := db.Prepare("UPDATE \"node_infos\" SET \"node_username\" = $1 WHERE \"node_name\" = $2")
	if err != nil {
		log.Fatal("PG Statements Wrong: ", err)
	}

	res, err := stmt.Exec("blabla", "blabla")
	if err != nil {
		log.Fatal("PG Statements Exec Wrong: ", err)
	}

	id, err := res.RowsAffected()
	if err != nil {
		log.Fatal("PG Affecte Wrong: ", err)
	}

	fmt.Println(id)
	return nil
}

func main() {
	// 链接PostgreSQL数据库
	log.Println("Connecting PostgreSQL....")

	psqlInfo := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable", pg_host, pg_port, pg_user, pg_password, pg_dbname)
	db, err = sql.Open("postgres", psqlInfo)
	if err != nil {
		log.Fatal("Connect PG Failed: ", err)
	}

	db.SetMaxOpenConns(2000)
	db.SetMaxIdleConns(1000)
	defer db.Close()

	err = db.Ping()
	if err != nil {
		log.Fatal("Ping GP Failed: ", err)
	}
	fmt.Println("PG Successfull Connected!")

	// 插入数据
	//err := InsertNodeInfo()
	//if err != nil {
	//	log.Fatal("Insert Data Failed: ", err)
	//}

	// 删除数据
	//err := DeleteNodeInfo()
	//if err != nil {
	//	log.Fatal("Delete Data Failed: ", err)
	//}

	// 查询所有数据
	//err := SelectAllNodeInfo()
	//if err != nil {
	//	log.Fatal("Select All Data Failed: ", err)
	//}

	// 更新某一数据
	err := UpdateNodeInfo()
	if err != nil {
		log.Fatal("Update Data Failed: ", err)
	}
}
```

### PG驱动库包github.com/lib/pq

采用`github.com/lib/pq`主要是其提供创建数据库表的方法。

``` golang
package main

/*
Author: Chen Jian
Blog:   https://www.o-my-chenjian.com
Date:   2018-11-20
*/

import (
	"fmt"
	"log"

	"github.com/go-pg/pg"
	"github.com/go-pg/pg/orm"
)

// PGs数据库信息
const (
	pg_addr     = "10.16.11.95:5432"
	pg_user     = "postgres"
	pg_password = "postgres"
	pg_dbname   = "postgres"
)

// 定义表结构
type NodeInfo struct {
	NodeName     string `sql:"type:varchar(45),unique,notnull,pk"`
	NodeIp       string `sql:"type:varchar(45),notnull"`
	NodePort     string `sql:"type:varchar(45),notnull"`
	NodeUsername string `sql:"type:varchar(45),notnull"`
	NodePassword string `sql:"type:varchar(255),notnull"`
}

func CreateTable(db *pg.DB) error {
	for _, model := range []interface{}{(*NodeInfo)(nil)} {
		err := db.CreateTable(model, &orm.CreateTableOptions{
			IfNotExists:   true,
			FKConstraints: true,
		})
		if err != nil {
			return err
		}
	}
	return nil
}

func DeleteTable(db *pg.DB) error {

	err := db.DropTable(&NodeInfo{}, &orm.DropTableOptions{
		IfExists: true,
		Cascade:  true,
	})

	return err
}

func InsertNodeInfo(db *pg.DB) error {
	// 插入数据方法一
	//nodeinfodata := &NodeInfo{
	//	NodeName:     "chenjian",
	//	NodeIp:       "10.0.0.5",
	//	NodePort:     "2222",
	//	NodeUsername: "chenjian",
	//	NodePassword: "1234321",
	//}
	//err := db.Insert(nodeinfodata)
	//if err!=nil {
	//	return err
	//}

	// 插入数据方法二
	err := db.Insert(&NodeInfo{
		NodeName:     "chenjian",
		NodeIp:       "10.0.0.5",
		NodePort:     "2222",
		NodeUsername: "chenjian",
		NodePassword: "1234321",
	})
	if err != nil {
		return err
	}
	return nil
}

func SelectAllNodeInfo(db *pg.DB) error {
	var nodeinfodata []NodeInfo
	err := db.Model(&nodeinfodata).Select()
	if err != nil {
		return err
	}
	fmt.Println(nodeinfodata)
	return nil
}

func SelectNodeInfo(db *pg.DB) error {
	nodeinfodata := &NodeInfo{
		NodeName: "chenjian",
	}
	err := db.Select(nodeinfodata)
	if err != nil {
		return err
	}
	fmt.Println(nodeinfodata)
	return nil
}

func UpdateNodeInfo(db *pg.DB) error {
	var nodeinfodata []NodeInfo

	updatedata := &NodeInfo{
		NodeName:     "chenjian",
		NodeIp:       "10.0.0.5",
		NodePort:     "3333",
		NodeUsername: "chenjian",
		NodePassword: "1234321",
	}

	_, err := db.Model(&nodeinfodata).
		Set("node_port = ?", updatedata.NodePort).
		Where("node_name = ?", updatedata.NodeName).
		Returning("*").
		Update()
	if err != nil {
		return err
	}
	return nil
}

func main() {
	// 链接PostgreSQL数据库
	log.Println("Connecting PostgreSQL....")

	db := pg.Connect(&pg.Options{
		Addr:     pg_addr,
		User:     pg_user,
		Password: pg_password,
		Database: pg_dbname,
	})
	defer db.Close()

	fmt.Println("Successfull Connected!")

	// 创建表
	//err := CreateTable(db)
	//if err != nil {
	//	log.Fatal("Create Table Failed: ",err)
	//}

	// 删除表
	//err := DeleteTable(db)
	//if err != nil {
	//	log.Fatal("Delete Table Failed: ", err)
	//}

	// 插入数据
	//err := InsertNodeInfo(db)
	//if err != nil {
	//	log.Fatal("Insert Data Failed: ", err)
	//}

	// 查询所有数据
	//err := SelectAllNodeInfo(db)
	//if err != nil {
	//	log.Fatal("Select All Data Failed: ", err)
	//}

	// 查询某一数据
	//err := SelectNodeInfo(db)
	//if err != nil {
	//	log.Fatal("Select Data Failed: ", err)
	//}

	// 更新某一数据
	err := UpdateNodeInfo(db)
	if err != nil {
		log.Fatal("Update Data Failed: ", err)
	}
}
```

### govendor依赖管理工具

通过`govendor`可以很方便的管理项目中所有的依赖包。例如将依赖包放到项目路径下，便于项目的传递，从而不需再一次下载依赖包。

##### govendor的安装

``` shell
go get -u github.com/kardianos/govendor

# 无法下载成功，可以下载源码，进行编译
mkdir -p ${GOPATH}/src/github.com/kardianos
cd ${GOPATH}/src/github.com/kardianos
git clone https://github.com/kardianos/govendor.git govendor
```

##### govendor的操作

``` shell
# 进入项目路径
cd ${GOPATH}/src/chenjian

# 初始化govendor。随后会生成一个vender文件夹，里面有个vender.json，记录着依赖包的信息
govendor init

# 查看项目中所需依赖列表，状态内容如下
govendor list

# 查看正在使用的依赖包
govendor list -v fmt

# 下载missing的依赖包，下载完后，+missing变为+external状态
govendor get k8s.io/klog

# 下载特定版本的依赖包
govendor fetch golang.org/x/net/context@a4bbce9fcae005b22ae5443f6af064d80a6f5a55
# Get latest v1.*.* tag or branch.
govendor fetch golang.org/x/net/context@v1
# Get the tag or branch named "v1".
govendor fetch golang.org/x/net/context@=v1  

# 将+external状态的依赖包归到govender管理
govendor add k8s.io/klog

# 批量add
govendor add +e
```

- vender.json

``` json
{
	"comment": "",
	"ignore": "test",
	"package": [
		{
			"checksumSHA1": "asksIwylfIjaYsF2nMY69jTyxC0=",
			"path": "github.com/lib/pq",
			"revision": "9eb73efc1fcc404148b56765b0d3f61d9a5ef8ee",
			"revisionTime": "2018-10-16T16:26:27Z"
		}
	],
	"rootPath": "chenjian"
}

```

- 依赖包状态

| 状态 | 缩写 | 含义 |
| :---: | :---: | :---: |
| +local | l | 在项目中的包 | 
| +external | e | 外部包，即被 $GOPATH 管理，但不在 vendor 目录下 |
| +vendor | v | 已被 govendor 管理，即在 vendor 目录下 |
| +std | s | 标准库中的包 |
| +unused | u | 未使用的包，即包在 vendor 目录下，但项目并没有用到 |
| +missing | m | 代码引用了依赖包，但该包并没有找到 |
| +program | p | 主程序包，意味着可以编译为执行文件 |
| +outside | | 外部包和缺失的包|
| +all | | 所有的包 |



### 文献博文

1. [Golang 访问PostgreSQL数据库增删改查](https://blog.csdn.net/lengyuezuixue/article/details/79158532)
2. [PostgreSQL一些常用命令](https://blog.csdn.net/u010856284/article/details/70142810)
3. [PostgreSQL client and ORM for Golang](https://github.com/go-pg/pg)
4. [golang基础-Postgresql-ORM框架github.com/go-pg/pg学习一](https://blog.csdn.net/u013210620/article/details/82732637)
5. [The Vendor Tool for Go](https://github.com/kardianos/govendor)
6. [go依赖管理-govendor](https://studygolang.com/articles/9785)