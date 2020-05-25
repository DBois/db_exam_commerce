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
-   To setup the roles, login to your mongoDB admin account.
-   Switch to the admin database by typing `use admin`
-   Copy paste the roles and users from [this file](./mongodb/mongo_users_and_roles.js)
-   **If you do not have authorization enabled do the following:**
-   Locate your `mongod.cfg` file. Mine was inside `C:\Program Files\MongoDB\Server\4.2\bin` and add the following lines:

```
security:
  authorization: "enabled"
```

-   Restart your MongoDB service:  
    **For windows:**
-   Search for Services.msc and open it.
-   Right click on MongoDB Server and Restart  
    **For Linux:**
-   Write `sudo service mongod restart` in the console

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

-   In-order to set-up the users and roles execute the following commands, one by one.

```
CALL dbms.security.createUser('admin_user', 'admin', false);
CALL dbms.security.addRoleToUser('admin', 'admin_user');

CALL dbms.security.createUser('reader_user', 'reader', false);
CALL dbms.security.addRoleToUser('reader', 'reader_user');
```
