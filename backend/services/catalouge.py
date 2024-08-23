import json
from typing import Any, Optional

from config import TABLE_COLUMNS
from fastapi import Query

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

fetch_article_info_sql_statement = """
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
WHERE
  article_id = {article_id};
"""


def get_default_catalog(
    database: Any,
    limit: Optional[int] = Query(10, ge=1, le=300),
):
    cursor = database.cursor()
    cursor.execute(fetch_random_all_sql_statement.format(limit=limit))
    results = cursor.fetchall()
    return [dict(zip(TABLE_COLUMNS, result)) for result in results]


def get_article_info(
    database: Any,
    article_id: int,
):
    cursor = database.cursor()
    cursor.execute(fetch_article_info_sql_statement.format(article_id=article_id))
    result = cursor.fetchone()
    return dict(zip(TABLE_COLUMNS, result))
