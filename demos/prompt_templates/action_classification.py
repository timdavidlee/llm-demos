"""python -m demos.prompt_templates.classify_product_items"""

from enum import Enum
from dataclasses import dataclass
import json
import os
from typing import Dict, Any, Optional, List
import openai
from openai import OpenAI
from dotenv import load_dotenv


@dataclass
class WebsiteAction:
    action_name: str
    action_description: str


WEBSITE_ACTIONS = {
    "search": WebsiteAction(
        action_name="search",
        action_description="Search for a product or service on the website.",
    ),
    "return_product": WebsiteAction(
        action_name="return_product",
        action_description="Return a product or service on the website.",
    ),
    "add_to_cart": WebsiteAction(
        action_name="add_to_cart",
        action_description="Add a product or service to the cart on the website.",
    ),
    "checkout": WebsiteAction(
        action_name="checkout",
        action_description="Checkout from the website.",
    ),
    "add_payment_method": WebsiteAction(
        action_name="add_payment_method",
        action_description="Add a payment method to the website.",
    ),
    "sign_up_newsletter": WebsiteAction(
        action_name="sign_up_newsletter",
        action_description="Sign up for the website's newsletter.",
    ),
}
