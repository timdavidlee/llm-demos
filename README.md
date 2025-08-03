# llm-demos


## How to Run 


### Demo 1

```sh
python -m demos.prompt_templates.classify_product_items
```

```
Example 0: Product classification using template
Product item: iPhone 15 Pro
Result:
{
  "parsed_json": {
    "product_item_name": "iPhone 15 Pro",
    "product_description": "None",
    "predicted_category": "personal_electronics",
    "predicted_category_description": "Personal electronics products include laptops, smartphones, tablets, and other electronic devices."
  },
  "product_item_name": "iPhone 15 Pro",
  "product_description": null,
  "categories_used": [
    "personal_electronics",
    "home_electronics",
    "office_electronics",
    "gaming_electronics",
    "audio_electronics",
    "clothing",
    "home_and_garden",
    "sports_and_outdoors",
    "unclassified"
  ],
  "model_used": "gpt-3.5-turbo",
  "tokens_used": 427
}

==================================================

Example 1: Product classification using template
Product item: Sony WH-1000XM5 headphones
Result:
{
  "parsed_json": {
    "product_item_name": "Sony WH-1000XM5 headphones",
    "product_description": "None",
    "predicted_category": "audio_electronics",
    "predicted_category_description": "Audio electronics products include headphones, speakers, and other audio devices."
  },
  "product_item_name": "Sony WH-1000XM5 headphones",
  "product_description": null,
  "categories_used": [
    "personal_electronics",
    "home_electronics",
    "office_electronics",
    "gaming_electronics",
    "audio_electronics",
    "clothing",
    "home_and_garden",
    "sports_and_outdoors",
    "unclassified"
  ],
  "model_used": "gpt-3.5-turbo",
  "tokens_used": 433
}

==================================================

Example 2: Product classification using template
Product item: Nike Air Max running shoes
Result:
{
  "parsed_json": {
    "product_item_name": "Nike Air Max running shoes",
    "product_description": "None",
    "predicted_category": "sports_and_outdoors",
    "predicted_category_description": "Sports and Outdoors - Sports and outdoors products include sports equipment, outdoor gear, and other items for sports and outdoor activities."
  },
  "product_item_name": "Nike Air Max running shoes",
  "product_description": null,
  "categories_used": [
    "personal_electronics",
    "home_electronics",
    "office_electronics",
    "gaming_electronics",
    "audio_electronics",
    "clothing",
    "home_and_garden",
    "sports_and_outdoors",
    "unclassified"
  ],
  "model_used": "gpt-3.5-turbo",
  "tokens_used": 439
}

==================================================

Example 3: Product classification using template
Product item: Samsung Smart TV
Result:
{
  "parsed_json": {
    "product_item_name": "Samsung Smart TV",
    "product_description": "None",
    "predicted_category": "home_electronics",
    "predicted_category_description": "Home Electronics - Home electronics products include smart home devices, smart speakers, smart lights, and other electronic devices."
  },
  "product_item_name": "Samsung Smart TV",
  "product_description": null,
  "categories_used": [
    "personal_electronics",
    "home_electronics",
    "office_electronics",
    "gaming_electronics",
    "audio_electronics",
    "clothing",
    "home_and_garden",
    "sports_and_outdoors",
    "unclassified"
  ],
  "model_used": "gpt-3.5-turbo",
  "tokens_used": 432
}

==================================================

Example 4: Product classification using template
Product item: Gaming mouse with RGB lighting
Result:
{
  "parsed_json": {
    "product_item_name": "Gaming mouse with RGB lighting",
    "product_description": "None",
    "predicted_category": "gaming_electronics",
    "predicted_category_description": "Gaming electronics products include gaming consoles, gaming accessories, and other electronic devices."
  },
  "product_item_name": "Gaming mouse with RGB lighting",
  "product_description": null,
  "categories_used": [
    "personal_electronics",
    "home_electronics",
    "office_electronics",
    "gaming_electronics",
    "audio_electronics",
    "clothing",
    "home_and_garden",
    "sports_and_outdoors",
    "unclassified"
  ],
  "model_used": "gpt-3.5-turbo",
  "tokens_used": 433
}

==================================================

Example 5: Product classification using template
Product item: childrens play set
Result:
{
  "parsed_json": {
    "product_item_name": "childrens play set",
    "product_description": "None",
    "predicted_category": "unclassified",
    "predicted_category_description": "Unclassified products include items that do not fit into any other category. This is a catch-all category for items that are not classified into any other category."
  },
  "product_item_name": "childrens play set",
  "product_description": null,
  "categories_used": [
    "personal_electronics",
    "home_electronics",
    "office_electronics",
    "gaming_electronics",
    "audio_electronics",
    "clothing",
    "home_and_garden",
    "sports_and_outdoors",
    "unclassified"
  ],
  "model_used": "gpt-3.5-turbo",
  "tokens_used": 442
}

==================================================
```

### Demo 2

```sh
python -m demos.prompt_templates.entity_extraction_prompt
```


```
Example 0: Simple entity extraction
Text:
        John Smith works as a Software Engineer at Apple Inc. in San Francisco.
        He previously worked at Google LLC in Mountain View, California.
        The company's Marketing team is located in New York.

Result:
{
  "extracted_entities": {
    "entities": [
      {
        "predicted_entity_type": "person",
        "predicted_entity_name": "John Smith",
        "predicted_entity_description": "A human being"
      },
      {
        "predicted_entity_type": "job_title",
        "predicted_entity_name": "Software Engineer",
        "predicted_entity_description": "A title given to a person who is employed by a company"
      },
      {
        "predicted_entity_type": "company",
        "predicted_entity_name": "Apple Inc.",
        "predicted_entity_description": "A legal entity that is registered and has a unique identifier"
      },
      {
        "predicted_entity_type": "city",
        "predicted_entity_name": "San Francisco",
        "predicted_entity_description": "A large human settlement"
      },
      {
        "predicted_entity_type": "company",
        "predicted_entity_name": "Google LLC",
        "predicted_entity_description": "A legal entity that is registered and has a unique identifier"
      },
      {
        "predicted_entity_type": "city",
        "predicted_entity_name": "Mountain View",
        "predicted_entity_description": "A large human settlement"
      },
      {
        "predicted_entity_type": "city",
        "predicted_entity_name": "California",
        "predicted_entity_description": "A large human settlement"
      },
      {
        "predicted_entity_type": "business_unit",
        "predicted_entity_name": "Marketing team",
        "predicted_entity_description": "A division of a company that is responsible for a specific function or product"
      },
      {
        "predicted_entity_type": "city",
        "predicted_entity_name": "New York",
        "predicted_entity_description": "A large human settlement"
      }
    ]
  },
  "input_text": "\n        John Smith works as a Software Engineer at Apple Inc. in San Francisco. \n        He previously worked at Google LLC in Mountain View, California. \n        The company's Marketing team is located in New York.\n        ",
  "entity_types_used": [
    "company",
    "city",
    "organization",
    "business_unit",
    "person",
    "job_title"
  ],
  "model_used": "gpt-3.5-turbo",
  "tokens_used": 670
}

==================================================

Example 1: Simple entity extraction
Text:
        Valued at EUR412.8 million, the all-share deal is set to integrate the Greek stock exchange into Euronext's extensive European network, which currently manages about 25% of total cash equity trading activity across several major financial hubs. This integration is expected to provide Greek companies with access to a broader investment base, enhancing liquidity and offering greater opportunities for capital raises and bond issuances. Please mention the Source: https://www.indexbox.io/blog/euronexts-acquisition-of-athens-stock-exchange-a-new-era-for-greece/

Result:
{
  "extracted_entities": {
    "entities": [
      {
        "predicted_entity_type": "company",
        "predicted_entity_name": "Euronext",
        "predicted_entity_description": "European stock exchange operator"
      },
      {
        "predicted_entity_type": "city",
        "predicted_entity_name": "Athens",
        "predicted_entity_description": "Capital city of Greece"
      },
      {
        "predicted_entity_type": "organization",
        "predicted_entity_name": "Greek stock exchange",
        "predicted_entity_description": "Stock exchange in Greece"
      },
      {
        "predicted_entity_type": "organization",
        "predicted_entity_name": "Euronext",
        "predicted_entity_description": "European stock exchange operator"
      },
      {
        "predicted_entity_type": "company",
        "predicted_entity_name": "Euronext",
        "predicted_entity_description": "European stock exchange operator"
      },
      {
        "predicted_entity_type": "organization",
        "predicted_entity_name": "Greek companies",
        "predicted_entity_description": "Companies based in Greece"
      }
    ]
  },
  "input_text": "\n        Valued at EUR412.8 million, the all-share deal is set to integrate the Greek stock exchange into Euronext's extensive European network, which currently manages about 25% of total cash equity trading activity across several major financial hubs. This integration is expected to provide Greek companies with access to a broader investment base, enhancing liquidity and offering greater opportunities for capital raises and bond issuances. Please mention the Source: https://www.indexbox.io/blog/euronexts-acquisition-of-athens-stock-exchange-a-new-era-for-greece/\n        ",
  "entity_types_used": [
    "company",
    "city",
    "organization",
    "business_unit",
    "person",
    "job_title"
  ],
  "model_used": "gpt-3.5-turbo",
  "tokens_used": 567
}

==================================================

Example 2: Simple entity extraction
Text:
OpenAI on Thursday said it is launching a Stargate-branded AI data center in Norway, marking its first foray into Europe with such a project.

British firm Nscale will design and build the site as part of a 50-50 joint venture with Norwegian energy infrastructure firm Aker.

OpenAI will be a so-called “off-taker” in the project, meaning it will effectively buy capacity from the data center.

“Part of the purpose of this project is to partner with OpenAI and leverage European sovereign compute to release additional services and features to the European continent,” Josh Payne, CEO of Nscale, told CNBC in an interview on Thursday.

Result:
{
  "extracted_entities": {
    "entities": [
      {
        "predicted_entity_type": "organization",
        "predicted_entity_name": "OpenAI",
        "predicted_entity_description": "A research organization focused on artificial intelligence"
      },
      {
        "predicted_entity_type": "city",
        "predicted_entity_name": "Norway",
        "predicted_entity_description": "A country in Europe"
      },
      {
        "predicted_entity_type": "company",
        "predicted_entity_name": "Nscale",
        "predicted_entity_description": "A British firm specializing in design and construction"
      },
      {
        "predicted_entity_type": "company",
        "predicted_entity_name": "Aker",
        "predicted_entity_description": "A Norwegian energy infrastructure firm"
      },
      {
        "predicted_entity_type": "person",
        "predicted_entity_name": "Josh Payne",
        "predicted_entity_description": "CEO of Nscale"
      }
    ]
  },
  "input_text": "\nOpenAI on Thursday said it is launching a Stargate-branded AI data center in Norway, marking its first foray into Europe with such a project.\n\nBritish firm Nscale will design and build the site as part of a 50-50 joint venture with Norwegian energy infrastructure firm Aker.\n\nOpenAI will be a so-called \u201coff-taker\u201d in the project, meaning it will effectively buy capacity from the data center.\n\n\u201cPart of the purpose of this project is to partner with OpenAI and leverage European sovereign compute to release additional services and features to the European continent,\u201d Josh Payne, CEO of Nscale, told CNBC in an interview on Thursday.\n        ",
  "entity_types_used": [
    "company",
    "city",
    "organization",
    "business_unit",
    "person",
    "job_title"
  ],
  "model_used": "gpt-3.5-turbo",
  "tokens_used": 597
}

==================================================
```