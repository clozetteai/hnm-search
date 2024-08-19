# Author: Anidyadeep Sanigrahi https://github.com/Anindyadeep

import json
from fastapi import Query
from typing import Any
from typing import Optional

from config import TABLE_COLUMNS

# Right now we having random catalouge but it should have business
# logic embedded when showing some default catalouge

fetch_random_all_sql_statement = """
SELECT
  article_id,
  prod_name,
  product_type_name,
  product_group_name,
  department_name,
  index_name,
  section_name,
  detail_desc,
  graphical_appearance_name,
  colour_group_name,
  perceived_colour_value_name
FROM
  product
ORDER BY
  RAND()
LIMIT
  {limit};
"""


def get_default_catalog(
    database: Any,
    limit: Optional[int] = Query(10, ge=1, le=300),
):
    cursor = database.cursor()
    cursor.execute(fetch_random_all_sql_statement.format(limit=limit))
    results = cursor.fetchall()
    return [dict(zip(TABLE_COLUMNS, result)) for result in results]


# catalouge = []
# for result in results:
#     result = dict(zip(TABLE_COLUMNS, result))
#     image_path = ASSET_PATH / f"0{result['article_id']}.jpg"

#     if image_path.exists():
#         image_base64 = image_to_base64(image_path)
#     else:
#         image_base64 = None
#     result["image"] = image_base64
#     catalouge.append(result)
# return  json.dumps(catalouge)
