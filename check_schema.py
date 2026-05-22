import mysql.connector
import os
from dotenv import load_dotenv

# Try to find db config or just run a query if I can
# Usually I can't easily connect without credentials.
# I'll check the source code for DB connection.
