# Polyglot Databases

## Getting Started:

### Postgres:

-   Create two databases. `db_exam_logistics` and `db_exam_customers`.
-   Download the DDL files [located here](https://github.com/DBois/db_exam_commerce/tree/master/postgres) and setup your databases.

#### Setting up Logistics database

-   Download [populate files](https://mega.nz/file/q9xTWTqa#JVxRX6DwRztT3FtTDzIUjy8eep7rMpiEiYl2ZPqxXn4).
-   Run `job_position_202005211245.sql`
-   Run `item_202005211245.sql`
-   Run `department_202005211245.sql`
-   Run `employee_202005211245.sql`
-   Import `department_item_202005211302.csv`

#### Setting up Customer database

-   Download [customer and credit card populate files](https://mega.nz/file/bxRhEYIS#xKtcQruwCymRPgUBsP8XDynI2ySAOLIxQfIuVruFQtI)
-   Import the two CSV files
### Setting up MongoDB
-   Download [the order CSV file](https://mega.nz/file/OgpABA7T#ZCNRxE8dKmQxkzu5pwMpZLFin5VKIKu20t8iUk8MWR4)  
-   Run this command with your own filepath and username to populate your database and collection: `mongoimport -d db_exam_orders -c orders --type csv --file <filepath> -u <username> --authenticationDatabase admin --drop --headerline`
