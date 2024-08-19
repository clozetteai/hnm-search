# from services.catalouge import get_catalog
# from services.tidb_connector import connect_to_tidb, TiDBConfig

# config = TiDBConfig()
# db = connect_to_tidb(db_config=config)

# results = get_catalog(database=db, limit=1)
# print(results)

# t2s = Text2SQLPrompt(
#     table_name="product",
#     db_config=config
# )

# print(t2s(query="hello how are you"))

### Using the Text to SQL Service

# from services.text2sql.retriever import Text2SQLCandidateGenerator
# t2s = Text2SQLCandidateGenerator()


# sql_query = t2s.convert(input("Enter query: "))
# print(sql_query)
# result = t2s.execute_query(sql_query["sql_prompt"])
# print(result)
# print(len(result))

### Using the embedding text service
# from services.search import EmbeddingSearchService

# search = EmbeddingSearchService()
# articles = search.perform_text_search(
#     "hello world", limit=2
# )
# print(articles)

# images = search.perform_image_search_from_file(
#     image_file_path="/Users/anindyadeepsannigrahi/workspace/personal/Hackathon/hnm-search/backend/assets/0108775015.jpg",
#     limit=3
# )

# print(images)

# from services.conversation.conversation import ConversationModule
# from config import LLMConfig

# converse = ConversationModule(
#     llm_config=LLMConfig(),
#     history_length=3
# )

# result1 = converse.converse(message="show me some red tops")
# result2 = converse.converse(message="whats upp?")
# result3 = converse.converse(message="blue jeans")

# print(result1.keys())
# print("-------")
# print(result2["outputs"]["search_query"])
# print("-------")
# print(result3["outputs"]["search_query"])

# import base64
# from services.workflow import WorkFlow

# flow = WorkFlow()
# image_path = "/Users/anindyadeepsannigrahi/workspace/personal/Hackathon/hnm-search/backend/assets/0309434009.jpg"
# with open(image_path, "rb") as f:
#     image_bytes = f.read()
# image_bs64 = base64.b64encode(image_bytes).decode("utf-8")

# result = flow.run(
#     payload={
#         "customer_message": "birthday gift for my baby boy",
#         "attached_image": image_bs64,
#     }
# )


# print(len(result["catalouge"]))


from services.text2sql.retriever import Text2SQLCandidateGenerator

t2s = Text2SQLCandidateGenerator()
sql_query = t2s.convert("show me some red tops")
result, error_list = t2s.execute_query(sql_query["sql_prompt"])
# print the json format of result with some indent
import json
print(json.dumps(result, indent=4))
