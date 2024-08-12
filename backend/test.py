from services.text2sql.text2sql import Text2SQL


# Run this script if want to convert csv to SQL
# csv_to_sqlite(
#     r"C:\Users\Pratyush\Projects\hnm-search\backend\data\articles.csv", 
#     r"C:\Users\Pratyush\Projects\hnm-search\backend\data\articles.sqlite",
#     table_name="articles"
# )


# Create .env with fields PREM_API_KEY, PREM_LLM_MODEL, PREM_PROJECT_ID
t2s = Text2SQL(
    table_name="articles",
    sqlite_path=r"C:\Users\Pratyush\Projects\hnm-search\backend\data\articles.sqlite"
)

try:
    sql_query = t2s("Give me data of items who's 'prod_name' starts with 'A'")
    print(sql_query)
except Exception as e:
    print(e)