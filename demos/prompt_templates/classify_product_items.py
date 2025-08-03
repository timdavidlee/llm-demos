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
class ProductCategory:
    category_name: str
    category_description: str


PRODUCT_CATEGORIES = {
    "personal_electronics": ProductCategory(
        category_name="Personal Electronics",
        category_description="Personal electronics products include laptops, smartphones, tablets, and other electronic devices.",
    ),
    "home_electronics": ProductCategory(
        category_name="Home Electronics",
        category_description="Home electronics products include smart home devices, smart speakers, smart lights, and other electronic devices.",
    ),
    "office_electronics": ProductCategory(
        category_name="Office Electronics",
        category_description="Office electronics products include printers, scanners, and other electronic devices.",
    ),
    "gaming_electronics": ProductCategory(
        category_name="Gaming Electronics",
        category_description="Gaming electronics products include gaming consoles, gaming accessories, and other electronic devices.",
    ),
    "audio_electronics": ProductCategory(
        category_name="Audio Electronics",
        category_description="Audio electronics products include headphones, speakers, and other audio devices.",
    ),
    "clothing": ProductCategory(
        category_name="Clothing",
        category_description="Clothing products include shirts, pants, shoes, and other clothing items.",
    ),
    "home_and_garden": ProductCategory(
        category_name="Home and Garden",
        category_description="Home and garden products include furniture, appliances, tools, and other items for the home and garden.",
    ),
    "sports_and_outdoors": ProductCategory(
        category_name="Sports and Outdoors",
        category_description="Sports and outdoors products include sports equipment, outdoor gear, and other items for sports and outdoor activities.",
    ),
    "unclassified": ProductCategory(
        category_name="Unclassified",
        category_description="Unclassified products include items that do not fit into any other category. This is a catch-all category for items that are not classified into any other category.",
    ),
}

CLASSIFY_PRODUCT_ITEMS_PROMPT = """
You are a product classification expert. You are given a list of product items and you need to classify them into the appropriate category.
If the product item is not classified into any other category, classify it into the "unclassified" category.

Return the classification in the following JSON format:
{{"product_item_name": "product_item_name", "product_description": "product_description", "predicted_category": "category_name", "predicted_category_description": "category_description"}}

The product item name to classify is:
{product_item_name}

The product description (if available) to classify is:
{product_description}

The possible classification categories are:
{categories}
"""


def generate_product_classification_text(
    product_item_name: str,
    product_description: str | None = None,
    prompt_template: str = CLASSIFY_PRODUCT_ITEMS_PROMPT,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.1,
    max_tokens: int = 2000,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate text for product classification using the prompt template and categories.

    Args:
        product_items (List[str]): List of product items to classify
        prompt_template (str): The prompt template to use (defaults to CLASSIFY_PRODUCT_ITEMS_PROMPT)
        model (str): OpenAI model to use (default: "gpt-3.5-turbo")
        temperature (float): Controls randomness (0.0 = deterministic, 1.0 = very random)
        max_tokens (int): Maximum number of tokens in response
        api_key (Optional[str]): OpenAI API key. If None, uses environment variable

    Returns:
        Dict[str, Any]: Response with generated classification text and metadata
    """

    # Validate inputs
    if not product_items:
        raise ValueError("product_items cannot be empty")

    # Get API key
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter"
        )

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Prepare categories for the template
    categories_text = "\n".join(
        [
            f"- {category}: {product_category.category_name} - {product_category.category_description}"
            for category, product_category in PRODUCT_CATEGORIES.items()
        ]
    )

    # Prepare product items list
    product_items_text = "\n".join([f"- {item}" for item in product_items])

    # Format the prompt template
    formatted_prompt = prompt_template.format(
        product_item_name=product_item_name,
        product_description=product_description,
        categories=categories_text,
    )

    try:
        # Make API call
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": formatted_prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"},
        )

        # Extract response content
        response_content = response.choices[0].message.content

        # Parse JSON response
        try:
            parsed_json = json.loads(response_content)
            result = {
                "parsed_json": parsed_json,
                "product_item_name": product_item_name,
                "product_description": product_description,
                "categories_used": list(PRODUCT_CATEGORIES.keys()),
                "model_used": model,
                "tokens_used": response.usage.total_tokens if response.usage else None,
            }
        except json.JSONDecodeError as e:
            result = {
                "generated_text": response_content,
                "json_parse_error": str(e),
                "product_item_name": product_item_name,
                "product_description": product_description,
                "categories_used": list(PRODUCT_CATEGORIES.keys()),
                "model_used": model,
                "tokens_used": response.usage.total_tokens if response.usage else None,
            }

        return result

    except openai.OpenAIError as e:
        return {
            "error": f"OpenAI API error: {str(e)}",
            "product_item_name": product_item_name,
            "product_description": product_description,
            "categories_used": list(PRODUCT_CATEGORIES.keys()),
        }

    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "product_item_name": product_item_name,
            "product_description": product_description,
            "categories_used": list(PRODUCT_CATEGORIES.keys()),
        }


# Example usage
if __name__ == "__main__":
    load_dotenv()
    # Example 1: Product classification using the template
    product_items = [
        "iPhone 15 Pro",
        "Sony WH-1000XM5 headphones",
        "Nike Air Max running shoes",
        "Samsung Smart TV",
        "Gaming mouse with RGB lighting",
        "childrens play set",
    ]

    for j, product_item in enumerate(product_items):
        print(f"Example {j}: Product classification using template")
        print(f"Product item: {product_item}")
        try:
            result = generate_product_classification_text(product_item)
            print("Result:")
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"Error: {e}")

        print("\n" + "=" * 50 + "\n")
