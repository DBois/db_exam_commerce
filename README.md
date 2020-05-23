# Polyglot Databases

## Getting Started:
**FIRST** [download the popualte CSV files here](https://mega.nz/file/C0xVDAAK#MiTAFdhtzXrtc-Vo_mwuQfII4CIw7m0BxD3pUFh5SO0) 
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
-   Run this command with your own filepath `\Mongodb\order_fixed.csv` and username to populate your database and collection: `mongoimport -d db_exam_orders -c orders --type csv --file <filepath> -u <username> --authenticationDatabase admin --drop --headerline`

### Setting up Neo4j
- Create database (we used 3.5.18)
- Place items.csv in import folder
- Load in csv 
```
LOAD CSV WITH HEADERS 
FROM "file:///items.csv" 
AS Line
CREATE (c:Item {ProductNo: Line.product_number, Name: Line.name, Price: toInteger(Line.price)})
```
