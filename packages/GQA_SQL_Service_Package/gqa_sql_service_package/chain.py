from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.llms import OpenAI
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy import URL
import os
# DB connection

SERVER = os.environ.get("SERVER")
DATABASE = os.environ.get("DATABASE")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
DRIVER = os.environ.get("DRIVER", 'ODBC Driver 17 for SQL Server')

connectionString = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
url = URL.create("mssql+pyodbc", query={"odbc_connect": connectionString})

db = SQLDatabase.from_uri(
    url,
    include_tables=[
                        "CONTACTS_normalized",
                        "USERS_normalized",
                        "QUOTES_normalized",
                        "DEALERS_normalized"
                   ],
    view_support=True
)



# Create the chain

llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", openai_api_key=os.environ.get("OPENAI_API_KEY"))

sql_query_execution_interpret_chain = SQLDatabaseChain.from_llm(
    llm,
    db,
    verbose=True
)

# Run chain

chain = sql_query_execution_interpret_chain
