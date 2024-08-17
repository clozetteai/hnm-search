import os
from .prompt_generator import PromptGenerator
from dotenv import load_dotenv, find_dotenv
import concurrent.futures
from premai import Prem
import json

load_dotenv(find_dotenv())


class LLMConfig:
    temperature = 0.7
    api_key = os.getenv("PREM_API_KEY")
    model = os.getenv("PREM_LLM_MODEL")
    project_id = os.getenv("PREM_PROJECT_ID")

class ConversationModule:
    def __init__(self, message_length) -> None:
        self.llm_config = LLMConfig()
        self.client = Prem(api_key=self.llm_config.api_key)
        self.message_length = message_length
        self.message_list = []
        self.system_prompt = """
You are a chat bot that helps users to recommend clothes. You job is to ask user questions only and not recommend anything, 
related to their query. Use short and concise text messages. Remember answers to the questions will be mapped to these columns
So try to ask question from this only. Make sure the values used are from the 'unique_values' fields only for those that have it.
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
        
    def create_exit_outputs(self):
        pg = PromptGenerator(self.message_list)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_bot_output = executor.submit(self.call_llm, pg.output_prompt())
            future_search_query = executor.submit(self.call_llm, pg.search_prompt())

            return {
                "bot_output": json.loads(future_bot_output.result()["message"]["content"]),
                "search_query": json.loads(future_search_query.result()["message"]["content"])
            }
            
    def reset(self):
        self.message_list = []
    
    def converse(self, message: str):
        self.message_list.append({
            "role": "user",
            "content": message
        })
        
        if (len(self.message_list) == (self.message_length * 2) - 1):
            self.message_list.append({
                "role": "assistant",
                "content": "Lemme search, we might have something!"
            })
            
            return {
                "message_list": self.message_list,
                "conversation_ended": True,
                "outputs": self.create_exit_outputs()
            }
            
        llm_output = self.call_llm(self.message_list)
        self.message_list.append({
            "role": llm_output["message"]["role"],
            "content": llm_output["message"]["content"]
        })
        return {
            "message_list": self.message_list,
            "conversation_ended": False
        }
        
        
    def call_llm(self, message):
        response = self.client.chat.completions.create(
            messages=message if type(message) == list else [{"role": "user", "content": message}],
            system_prompt=self.system_prompt if type(message) == list else "",
            model=self.llm_config.model,
            temperature=self.llm_config.temperature,
            project_id=self.llm_config.project_id
        )
        
        return response.choices[0].to_dict()