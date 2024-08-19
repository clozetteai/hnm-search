# Author: Anidyadeep Sanigrahi https://github.com/Anindyadeep

from textwrap import dedent


class Text2SQLPrompts:
    def __init__(
        self,
        table_name: str,
        database,
    ):
        self.table_name = table_name
        self.db = database.cursor()

    def _sample_rows(self, limit=3):
        self.db.execute(
            dedent(
                f"""SELECT 
            article_id, prod_name, product_type_name, product_group_name, department_name,
            index_name, section_name, detail_desc, graphical_appearance_name, colour_group_name,
            perceived_colour_value_name
        FROM {self.table_name} LIMIT {limit}"""
            )
        )

        columns = [desc[0] for desc in self.db.description]
        rows = self.db.fetchall()
        results = [dict(zip(columns, row)) for row in rows]

        return results

    def __call__(self, query):
        sampled_rows = "\n".join([str(row) for row in self._sample_rows()])
        return dedent(
            f"""
        ## TASK: convert the given QUERY to a SQL statement. Strictly don't change the values of column names, keep the required spaces, etc.
        Always add required quotes for all the names, db or columns, as the names may contain spaces.
        Make sure the values used are from the 'unique_values' fields only for those that have it.

        ## IMPORTANT Things to keep in mind: 
        1. For the SQL query generated, the 'where' clause should not exactly match for a string
        as it may be slightly different, do a 'fuzzy-search' or 'contains' matching
        2. Never do 'SELECT *' always do 'SELECT             
        article_id, prod_name, product_type_name, product_group_name, department_name,
        index_name, section_name, detail_desc, graphical_appearance_name, colour_group_name,
        perceived_colour_value_name'
        3. With 'WHERE' clause conditions, NEVER use 'AND', always use 'OR', and make sure conditions are 
        not case-sensitive, so make them LOWER before comparing.

        """
            + f"""
        ## QUERY: {query}
        """
            + f"""
        ## TABLE DETAILS:
        ### TABLE NAME: {self.table_name}
        ### COLUMN NAMES: """
            + """
        [
            {"column_name": "article_id", "datatype": "int64"},
            {"column_name": "prod_name", "datatype": "object"},
            {"column_name": "product_type_name", "datatype": "object", unique_values: ["Swimwear bottom","Kids Underwear top","Unknown","Hoodie","Sneakers","Pyjama set","Leggings/Tights","Cap/peaked","Gloves","Jacket","Other shoe","Earring","Socks","Hair/alice band","Shorts","Bra","Bikini top","Hair string","Bag","Swimsuit","Cardigan","T-shirt","Umbrella","Belt","Underwear Tights","Trousers","Skirt","Shirt","Costumes","Hair clip","Bodysuit","Robe","Pyjama jumpsuit/playsuit","Underwear bottom","Boots","Top","Jumpsuit/Playsuit","Dress","Hat/beanie","Sleep Bag","Blazer","Vest top","Sweater","Sunglasses","Sandals"]},
            {"column_name": "product_group_name", "datatype": "object", unique_values: ["Garment Lower body","Shoes","Unknown","Underwear/nightwear","Swimwear","Socks & Tights","Nightwear","Garment Upper body","Items","Underwear","Accessories","Garment Full body"]},
            {"column_name": "department_name", "datatype": "object", unique_values: ["Jersey","Tops Knitwear DS","Jersey Fancy","Kids Boy Jersey Basic","Kids Girl UW/NW","Young Boy Trouser","Trouser","Clean Lingerie","Underwear Jersey","Men Sport Woven","Casual Lingerie","Socks","Shorts","Trousers DS","Mama Lingerie","Shopbasket Socks","Hair Accessories","Nursing","Shoes / Boots inactive from s5","Blazer S&T","Gloves/Hats","Bags","Men Sport Tops","Belts","Dresses DS","Jersey Fancy DS","Divided Shoes","Everyday Waredrobe Denim","Basics","Knitwear","Men Sport Acc","UW","Swimwear","Young Girl Jersey Basic","Tights basic","Socks Bin","Baby basics","Kids Girl S&T","Men Sport Bottoms","Jewellery","Other Accessories","Other items","Kids Boy Denim","Expressive Lingerie","Outdoor/Blazers DS","Trousers","Knit & Woven","Denim Other Garments","Young Girl S&T","Shirt","Woven bottoms","Small Accessories","EQ & Special Collections","Nightwear","Accessories","Young Girl UW/NW","Shoes","Outdoor/Blazers","Jacket Street","Basic 1","Denim Trousers","Functional Lingerie","Baby Nightwear","Jersey Basic","Sunglasses","Young Boy Jersey Basic"]},
            {"column_name": "index_name", "datatype": "object", unique_values:  ["Children Sizes 92-140","Divided","Children Sizes 134-170","Lingeries/Tights","Ladieswear","Baby Sizes 50-98","Sport","Menswear","Ladies Accessories"]},
            {"column_name": "section_name", "datatype": "object", unique_values: ["Womens Everyday Basics","Men Underwear","Womens Big accessories","Divided Accessories","Men Accessories","Womens Everyday Collection","Contemporary Street","Divided Basics","Mama","Contemporary Casual","Divided Collection","Womens Swimwear, beachwear","Womens Lingerie","Mens Outerwear","Baby Essentials & Complements","Men Shoes","Divided Selected","Men Suits & Tailoring","Womens Small accessories","Kids Boy","Men H&M Sport","Boys Underwear & Basics","H&M+","Womens Nightwear, Socks & Tigh","Girls Underwear & Basics","Young Boy","Contemporary Smart","Ladies Denim"]},
            {"column_name": "detail_desc", "datatype": "object"},
            {"column_name": "graphical_appearance_name", "datatype": "object", unique_values: ["Melange","Contrast","Check","Treatment","Lace","Neps","Dot","Chambray","Solid","Other pattern","Glittering/Metallic","Mixed solid/pattern","Placement print","Application/3D","Colour blocking","Front print","All over pattern","Transparent","Metallic","Stripe","Embroidery","Denim","Other structure","Jacquard"]},
            {"column_name": "colour_group_name", "datatype": "object", unique_values: ["Dark Blue","Other Pink","Turquoise","Other Yellow","Yellow","Dark Green","Dark Orange","White","Other Red","Other Orange","Dark Red","Light Pink","Other","Dark Beige","Orange","Light Green","Red","Light Orange","Blue","Black","Off White","Silver","Green","Yellowish Brown","Dark Purple","Dark Pink","Dark Yellow","Light Beige","Light Turquoise","Pink","Greenish Khaki","Grey","Greyish Beige","Purple","Light Red","Transparent","Light Grey","Light Blue","Beige","Light Yellow","Dark Grey","Gold"]},
            {"column_name": "perceived_colour_value_name", "datatype": "object", unique_values: ["Undefined","Light","Medium","Dark","Medium Dusty","Bright","Dusty Light"]}
        ]
        """+ f"""

        ### EXAMPLE ROWS FROM THE TABLE:
        {sampled_rows}
        """
            + """
        ## OUTPUT FORMAT:"
        {
            \"sql_prompt\": SQL_PROMPT
        }
        """
        )
