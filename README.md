# PIZZA ANALYZER

## Authors: Mikołaj Cichocki 257272, Szymon Machała 257281

## How to run the project

1. Clone the repository
2. Create and activate python virtual environment
3. Install dependencies `pip install -r requirements.txt`
4. Run `python main.py`

## Connecting to DB
To connect to database:
    - set a user that has permission to pizza database
    - add in .env file this line:
   `SQL_CONNECTION_STRING="Driver={ODBC Driver 18 for SQL Server};Server=<server-name>;Database=pizza;UID=<user-name>;PWD=<password>;TrustServerCertificate=yes"`
    or you can also provide any valid string that is able to connect to SQL Server.

## Packages:
    - matplotlib
    - dotenv
    - pyodbc
