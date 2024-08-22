# Author: Anidyadeep Sanigrahi https://github.com/Anindyadeep

import json

CONVERSATION_SYSTEM_PROMPT = """
You are a chat bot that helps users to recommend clothes. You job is to ask user questions only and not recommend anything, 
related to their query. Use short and concise text messages. Remember answers to the questions will be mapped to these columns
So try to ask question from this only. Make sure the values used are from the 'unique_values' fields only for those that have it.
Converse with the user, if they want to.
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
"""


class PromptGenerator:
    def __init__(self, message_list, num_queries=3) -> None:
        self.message_list = [
            f"{message['role']}: {message['content']}" for message in message_list
        ]
        self.num_queries = num_queries

    def search_prompt(self):
        return f"""
# TASK: Given a conversation about a user looking for a product. Give a list of textual search queries. Make sure 
each search query should have all the things the user asked for and you may add extra variations based on user requirements.
If you think, use has not entered in chat, what he wants, then you can return empty list.

# NUMBER OF QUERIES TO BE GENERATED: {self.num_queries}

# CONVERSATION: 
{json.dumps(self.message_list, indent=2)}

# OUTPUT FORMAT: # if you think, user has asked about some clothing product
[
    ...,
    ...
]

# OUTPUT FORMAT: # if you think, user has not given any info about what he wants, just wants to chat
[]
"""

    def output_prompt(self):
        PROMPT = (
            f"""
# TASK: You are a bot that helps users to search for cloths and recommend them. The conversation between you and
user has ended, and list is at CONVERSATION. Now generate a good formal and yet fun text output for the user as
the search is completed. Also create one for when search couldn't find any data. Keep the text short and concise.

# CONVERSATION: 
{json.dumps(self.message_list, indent=2)}
"""
            " + "
            """
# OUTPUT FORMAT:
{
    "data_found_output": "output",
    "data_not_found_output": "output
}
"""
        )
        return PROMPT
