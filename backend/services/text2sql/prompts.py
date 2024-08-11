import json
from .utils import get_db_columns

class Prompts:
    def __init__(
        self,
        table_name: str,
        database,
        query: str
    ):
        self.table_name = table_name
        self.db = database
        self.prompt = f"""
## TASK: convert the given QUERY to a SQL statement. Strictly don't change the values of column names, keep the required spaces, etc.
Always add required quotes for all the names, db or columns, as the names may contain spaces.
""" + f"""
## QUERY: {query}
""" + f"""
## TABLE DETAILS:
### TABLE NAME: {table_name}
### COLUMN NAMES: {json.dumps(get_db_columns(self.db), indent=4)}""" + f"""

### EXAMPLE ROWS FROM THE TABLE:
{"\n".join([str(row) for row in self._sample_rows()])}
""" + """
## OUTPUT FORMAT:"
{
    \"sql_prompt\": SQL_PROMPT
}
"""

    def _sample_rows(self, limit=3):
        self.db.execute(f"SELECT * FROM {self.table_name} LIMIT {limit}")
        rows = self.db.fetchall()
        return rows
    
    def __call__(self):
        return self.prompt