from openai import OpenAI
from enum import Enum
import json
import copy


class Categories(Enum):
    INVESTMENT = "investment"
    RENT = "rent"
    INSURANCE = "insurance"
    BUINESS_INCOME = "business income"
    PASSIVE_INCOME = "passive income"
    TAX = "tax"
    FINANCIAL_AID = "financial aid"

    FOOD = "food"
    GROCERIES = "groceries"
    RESTAURANT = "restaurant"
    CLOTHING = "clothing"
    GIFTS_DONATIONS = "gifts and donations"
    ENTERTAINMENT = "entertainment"
    SUBSCRIPTIONS_MEMBERSHIP = "subscriptions and membership"
    EQUIPMENT = "equipment"
    MUSIC = "music"
    HOBBIES = "hobbies"

    HEALTH = "health"
    SPORTS = "sports"
    PERSONAL_CARE = "personal care"

    SAVINGS = "savings"
    LOAN = "loan"
    FEES = "fees"

    UTILITIES = "utilities"
    INTERNET_CABLE = "internet and cable"
    PHONE = "phone"
    WATER = "water"
    ELECTRICITY = "electricity"
    GAS = "gas"

    TRAVEL = "travel"
    VACATION = "vacation"
    TRANSPORT = "transport"
    CAR = "car"
    PUBLIC_TRANSPORT = "public transport"
    TAXI = "taxi"
    FLIGHT = "flight"
    FUEL = "fuel"



enhancing_role_system = "Your are an intelligent system that takes in a transaction description from my banking history and enhances that description to make it more readable and understandable for an entry in a database. The description should be one sentence. Don't incoperate any infromation about the payment method , date, transaction number or other unnecessary detail. Just a short context about the transaction. Do not hallucinate or add any information that is not present in the original description. If the descriptions is not in english please translate it into english."
enhancing_role_user= "Please enhance the following transaction description from my banking history. The description should not be longer than a sentence. Don't incoperate any infromation about the payment method, date, transaction number or other unnecessary detail.. Just a short context about the transaction. Do not hallucinate or add any information that is not present in the original description. If the descriptions is in german please translate it into english. Description:"

extraction_role_system = "Your are an intelligent system that takes in a transaction description from my banking history and extracts the best matching categories for the transaction from the following list and gives me back a json array with the best matching categories. Form a precise decision. Do not hallucinate. Don't bload your answers with non matchign categories. If you are uncertain leave the catergory out. The categories are:"
categories = [category.value for category in Categories]
categories_string = ", ".join(categories)
extraction_role_system += categories_string
extraction_role_user = "Please take in the following transaction description from my banking history and extract the best matching categories. Give me back a json array with the best matching categories. Form a precise decision. Do not hallucinate. Don't bload your answers with non matchign categories. If you are uncertain leave the catergory out. The description is:"



function_name = "extractCategories"

function_schema = {
    "name": function_name,
    "parameters": {
        "type": "object",
        "properties": {
            "categories": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": [category.value for category in Categories]
                }
            }
        },
        "required": ["categories"]
    }
}



def create_message_structure(role_system, role_user):
    return [{"role": "system", "content": role_system}, {"role": "user", "content": role_user}]

class ChatGPTBanking:
    def __init__(self, api_key, model):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.enhancing_model_message_construct = create_message_structure(enhancing_role_system, enhancing_role_user)
        self.extraction_model_message_construct = create_message_structure(extraction_role_system, extraction_role_user)

    def enhance_description(self, description, amount):
        prefix = "Paid: " if amount < 0 else "Received: "
        description = f"{prefix}{description}"
        messages = copy.deepcopy(self.enhancing_model_message_construct)
        messages[1]["content"] += description
        try:
            completion = self.client.chat.completions.create(model=self.model, messages=messages)
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error during description enhancement: {e}")
            return None

    def extract_categories(self, description):
        messages = copy.deepcopy(self.extraction_model_message_construct)
        messages[1]["content"] += description
        try:
            completion = self.client.chat.completions.create(model=self.model, messages=messages, functions=[function_schema], function_call={"name": "extractCategories"})
            json_output = json.loads(completion.choices[0].message.function_call.arguments)
            json_output = json_output["categories"]
            return json_output
        except Exception as e:
            print(f"Error during category extraction: {e}")
            return None

