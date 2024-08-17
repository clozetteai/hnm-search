from services.text2sql.text2sql import Text2SQL


# Run this script if want to convert csv to SQL
# csv_to_sqlite(
#     r"C:\Users\Pratyush\Projects\hnm-search\backend\data\articles.csv", 
#     r"C:\Users\Pratyush\Projects\hnm-search\backend\data\articles.sqlite",
#     table_name="articles"
# )


# Create .env with fields PREM_API_KEY, PREM_LLM_MODEL, PREM_PROJECT_ID
# t2s = Text2SQL()

# sql_query = t2s.convert(input("Enter query: "))
# print(sql_query)
# result = t2s.execute_query(sql_query["sql_prompt"])
# print(result)
# print(len(result))



from services.conversation_module import ConversationModule
import json

cm = ConversationModule(3)

while True:
    user_input = input("Enter message:")
    output = cm.converse(user_input)
    print(json.dumps(output, indent=2))

    if (output["conversation_ended"]):
        break


# import os
# import mysql.connector
# class TiDBConfig:
#     host = os.getenv('TIDB_HOST')
#     port = os.getenv('TIDB_PORT')
#     user = os.getenv('TIDB_USERNAME')
#     password = os.getenv('TIDB_PASSWORD')
#     db_name = os.getenv('TIDB_DATABASE')
#     table_name = os.getenv("TIDB_TABLENAME")
#     autocommit = True
#     use_pure = True
    
#     def to_json(self):
#         config_dict = {
#             "host": self.host,
#             "port": self.port,
#             "user": self.user,
#             "password": self.password,
#             "database": self.db_name,
#             "autocommit": self.autocommit,
#             "use_pure": self.use_pure
#         }
#         return config_dict

# db_config = TiDBConfig()
# database = mysql.connector.connect(
#     **db_config.to_json()
# )

# cursor = database.cursor()
# cursor.execute("")