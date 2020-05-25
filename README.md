# Polyglot Databases

## Getting Started:

**FIRST** [download the popualte CSV files here](https://mega.nz/file/2w4jUBKK#TMA60vJY_zuoPhmy1_g3G5IdwDi9Ak0PIXe_oLoFIjI)

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
