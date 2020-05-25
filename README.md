# Polyglot Databases

## Getting Started:

**FIRST** [download the popualte CSV files here](https://mega.nz/file/msgFXCbL#63lEoxsXYK3GLsnmMUvU4Lu6rVXh6o6dL-H_a4NZLmM)

### Postgres:

-   Create two databases. `db_exam_logistics` and `db_exam_customers`.
-   Download the DDL files [located here](https://github.com/DBois/db_exam_commerce/tree/master/postgres) and setup your databases.

#### Setting up Logistics database

-   Download the CSV files mentioned above
-   Select your logistics database
-   Import the scripts inside `Postgres\Logistics` in the order they are named.

#### Setting up Customer database

-   Download the CSV files mentioned above
-   Select your customer database
-   Import the scripts inside `Postgres\customer` in the order they are named.

### Setting up MongoDB

-   Download the CSV files mentioned above
-   Download [Compass](https://www.mongodb.com/products/compass)
-   Setup your database and create a new collection
-   On the top bar press Collection -> Import Data and use the following settings (**InvoiceDate: Date**):  
    ![](./img/compass_settings.png)

### Setting up Neo4j

-   Create database (we used 3.5.18)
-   Place items.csv in import folder
-   Load in csv

```
LOAD CSV WITH HEADERS
FROM "file:///items.csv"
AS Line
CREATE (c:Item {ProductNo: Line.product_number, Name: Line.name, Price: toInteger(Line.price)})
```

- In-order to set-up the users and roles execute the following commands, one by one.

```
CALL dbms.security.createUser('admin_user', 'admin', false); 
CALL dbms.security.addRoleToUser('admin', 'admin_user');

CALL dbms.security.createUser('reader_user', 'reader', false); 
CALL dbms.security.addRoleToUser('reader', 'reader_user');
```

### Setting up redis cluster
*For this project we've used redis version 5+ which is required for using the following instructions. Otherwise go to this [redis cluster tutorial](https://redis.io/topics/cluster-tutorial), see how it differs for 3+ and 4+*

This is quick guide to how we set our redis clusters up. For further explanations read the aforementioned link.

#### Requirements
- unix system/subsystem
- redis-cli 5+

#### Steps

1. Make folders for cluster and then make folders for each port you want to run a redis-server application on. In our case 3 masters and 3 slaves so folders 7000-7005
```shell
mkdir redis-cluster
cd redis-cluster
mkdir 7000 7001 7002 7003 7004 7005
```
2. In each of the 7000-7005 folders make a redis.conf file which consists of the following text. **REMEMBER TO UPDATE PORT  TO CORRESPONDING FOLDER YOU'RE IN**
```shell
port 7000
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
appendonly yes
```
3. Download newest git repo of [unstable branch of redis ](https://github.com/antirez/redis)
```git
cd <file path to your redis-cluster folder>
git clone https://github.com/antirez/redis

```

4. Make executable of this source code
```
sudo apt-get update
sudo apt-get install tcl
cd redis-unstable
make
make test
```

5. After `make test` open a terminal in each of the 7000-7005 folders and run the following command
```
../redis-unstable/src/redis-server ./redis.conf
```

6. Now you have the nodes ready to make a cluster. Run the following command to create the cluster:
```
redis-cli --cluster create 127.0.0.1:7000 127.0.0.1:7001 \
127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 \
--cluster-replicas 1
```
