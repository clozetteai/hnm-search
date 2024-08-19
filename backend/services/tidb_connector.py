# Author: Anidyadeep Sanigrahi https://github.com/Anindyadeep

import mysql.connector
from dotenv import load_dotenv, find_dotenv
from config import TiDBConfig
from sqlalchemy.orm import declarative_base, Session
from tidb_vector.sqlalchemy import VectorType
from sqlalchemy import Column, Integer, String, Text, create_engine, URL
from config import TiDBConfig

load_dotenv(find_dotenv())


def connect_to_tidb(tidb_config: TiDBConfig):
    database = mysql.connector.connect(
        **{
            "host": tidb_config.host,
            "port": tidb_config.port,
            "user": tidb_config.user,
            "password": tidb_config.password,
            "database": tidb_config.db_name,
            "autocommit": tidb_config.autocommit,
            "use_pure": tidb_config.use_pure,
        }
    )
    return database


def connect_to_tidb_engine(tidb_config: TiDBConfig = TiDBConfig()):
    Base = declarative_base()

    class HandMProductEntity(Base):
        __tablename__ = "product"

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

        text_embedding = Column(
            VectorType(dim=tidb_config.text_embedding_dim), comment="hnsw(distance=l2)"
        )
        image_embedding = Column(
            VectorType(dim=tidb_config.image_embedding_dim), comment="hnsw(distance=l2)"
        )

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

    url = URL(
        drivername="mysql+pymysql",
        username=tidb_config.user,
        password=tidb_config.password,
        host=tidb_config.host,
        port=int(tidb_config.port),
        database=tidb_config.db_name,
        query={"ssl_verify_cert": True, "ssl_verify_identity": True},
    )

    engine = create_engine(url, pool_recycle=300)
    return engine, HandMProductEntity
