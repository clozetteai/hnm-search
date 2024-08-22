import logging
from sqlalchemy import create_engine, Column, Integer, Text, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import ProgrammingError
from constants.constants import (
    TIDB_HOST,
    TIDB_PORT,
    TIDB_USERNAME,
    TIDB_PASSWORD,
    TIDB_DB_NAME,
    TIDB_TABLE_NAME
)

logger = logging.getLogger(__name__)

class TiDBConfig:
    def __init__(self):
        self.host = TIDB_HOST
        self.port = TIDB_PORT
        self.user = TIDB_USERNAME
        self.password = TIDB_PASSWORD
        self.db_name = TIDB_DB_NAME
        self.table_name = TIDB_TABLE_NAME
        self.autocommit = True
        self.use_pure = True
        self.text_embedding_dim = 768 
        self.image_embedding_dim = 512

def connect_to_tidb_engine(tidb_config: TiDBConfig = TiDBConfig()):
    Base = declarative_base()

    class HandMProductEntity(Base):
        __tablename__ = tidb_config.table_name

        article_id = Column(Integer, primary_key=True)
        prod_name = Column(Text)
        product_type_name = Column(Text)
        product_group_name = Column(Text)
        department_name = Column(Text)
        index_name = Column(Text)
        section_name = Column(Text)
        detail_desc = Column(Text)
        graphical_appearance_name = Column(Text)
        colour_group_name = Column(Text)
        perceived_colour_value_name = Column(Text)
        text_embedding = Column(LargeBinary)  # Changed from VectorType to LargeBinary
        image_embedding = Column(LargeBinary)  # Changed from VectorType to LargeBinary

        def to_json(self):
            return {
                "article_id": self.article_id,
                "prod_name": self.prod_name,
                "product_type_name": self.product_type_name,
                "product_group_name": self.product_group_name,
                "department_name": self.department_name,
                "index_name": self.index_name,
                "section_name": self.section_name,
                "detail_desc": self.detail_desc,
                "graphical_appearance_name": self.graphical_appearance_name,
                "colour_group_name": self.colour_group_name,
                "perceived_colour_value_name": self.perceived_colour_value_name,
            }
            
    connection_url = f"mysql+pymysql://{tidb_config.user}:{tidb_config.password}@{tidb_config.host}:{tidb_config.port}/{tidb_config.db_name}"
    engine = create_engine(connection_url, pool_recycle=300)
    
    try:
        Base.metadata.create_all(engine)
        logger.info(f"Table '{tidb_config.table_name}' created successfully or already exists.")
        # print()
    except ProgrammingError as e:
        logger.error(f"Error creating table: {e}")

    return engine, HandMProductEntity