from services.text2sql.text2sql import Text2SQL
from services.text2sql.utils import csv_to_sqlite, load_sqlite_db
from services.text2sql.prompts import Prompts

t2s = Text2SQL()
csv_to_sqlite(
    r"C:\Users\Pratyush\Projects\hnm-search\backend\data\articles.csv", 
    r"C:\Users\Pratyush\Projects\hnm-search\backend\data\articles.sqlite",
    table_name="articles"
)

db = load_sqlite_db(r"C:\Users\Pratyush\Projects\hnm-search\backend\data\articles.sqlite")

prompt = Prompts(
    table_name="articles",
    database=db,
    query="Give me data of items who's 'prod_name' starts with 'A'"
)

print(t2s.call_llm(prompt()))
