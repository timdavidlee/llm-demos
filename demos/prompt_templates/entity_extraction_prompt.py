from dataclasses import dataclass
import json
import os
from typing import Dict, Any, Optional, List
import openai
from openai import OpenAI
from dotenv import load_dotenv


@dataclass
class Entity:
    name: str
    description: str | None = None
    examples: list[str] | None = None


ENTITY_TYPES = {
    "company": Entity(
        name="company",
        description="A company is a legal entity that is registered and has a unique identifier.",
        examples=["Apple Inc.", "Google LLC", "Microsoft Corporation"],
    ),
    "city": Entity(
        name="city",
        description="A city is a large human settlement.",
        examples=["New York", "London", "Paris"],
    ),
    "organization": Entity(
        name="organization",
        description="An organization is a group of people who share a common purpose.",
        examples=["United Nations", "World Health Organization", "Red Cross"],
    ),
    "business_unit": Entity(
        name="business_unit",
        description="A business unit is a division of a company that is responsible for a specific function or product.",
        examples=[
            "Sales",
            "Marketing",
            "Finance",
            "Engineering",
            "IT Support",
            "Accounting",
        ],
    ),
    "person": Entity(
        name="person",
        description="A person is a human being.",
        examples=["John Doe", "Jane Smith", "Bob Johnson"],
    ),
    "job_title": Entity(
        name="job_title",
        description="A job title is a title given to a person who is employed by a company.",
        examples=[
            "Software Engineer",
            "Product Manager",
            "Marketing Manager",
            "Sales Manager",
            "Accountant",
            "IT Support",
            "Engineer",
        ],
    ),
}


ENTITY_EXTRACTION_PROMPT = """
You are an entity extraction expert. You are given a text and you need to extract the entities from the text.

Here is a list of the entity types you can extract:
{entity_types}

The text to extract entities from is:
{text}

Return the entities in the following JSON format:
{{"entities": [{{"predicted_entity_type": "entity_type", "predicted_entity_name": "entity_name", "predicted_entity_description": "entity_description"}}]}}
"""


def assemble_ner_prompt(
    text: str,
    entity_types: Optional[Dict[str, Entity]] = None,
    prompt_template: str = ENTITY_EXTRACTION_PROMPT,
    include_examples: bool = True,
    custom_instructions: Optional[str] = None,
) -> str:
    """
    Assemble the LLM prompt for Named Entity Recognition (NER) extraction.

    Args:
        text (str): The text to extract entities from
        entity_types (Optional[Dict[str, Entity]]): Dictionary of entity types to extract.
                                                   If None, uses default ENTITY_TYPES
        prompt_template (str): The prompt template to use (defaults to ENTITY_EXTRACTION_PROMPT)
        include_examples (bool): Whether to include examples in the entity type descriptions
        custom_instructions (Optional[str]): Additional custom instructions to append

    Returns:
        str: The assembled prompt ready for LLM processing

    Raises:
        ValueError: If required parameters are missing
    """

    # Validate inputs
    if not text.strip():
        raise ValueError("text cannot be empty")

    # Use default entity types if none provided
    if entity_types is None:
        entity_types = ENTITY_TYPES

    # Format entity types for the prompt
    entity_types_formatted = []

    for entity_key, entity in entity_types.items():
        entity_description = f"- {entity.name}: {entity.description}"

        if include_examples and entity.examples:
            examples_str = ", ".join(entity.examples)
            entity_description += f" Examples: {examples_str}"

        entity_types_formatted.append(entity_description)

    entity_types_text = "\n".join(entity_types_formatted)

    # Format the prompt template
    formatted_prompt = prompt_template.format(entity_types=entity_types_text, text=text)

    # Add custom instructions if provided
    if custom_instructions:
        formatted_prompt += f"\n\nAdditional Instructions:\n{custom_instructions}"

    return formatted_prompt


def extract_entities_with_openai(
    text: str,
    entity_types: Optional[Dict[str, Entity]] = None,
    prompt_template: str = ENTITY_EXTRACTION_PROMPT,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.1,
    max_tokens: int = 2000,
    api_key: Optional[str] = None,
    include_examples: bool = True,
    custom_instructions: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Extract entities from text using OpenAI's API with the assembled NER prompt.

    Args:
        text (str): The text to extract entities from
        entity_types (Optional[Dict[str, Entity]]): Dictionary of entity types to extract
        prompt_template (str): The prompt template to use
        model (str): OpenAI model to use (default: "gpt-3.5-turbo")
        temperature (float): Controls randomness (0.0 = deterministic, 1.0 = very random)
        max_tokens (int): Maximum number of tokens in response
        api_key (Optional[str]): OpenAI API key. If None, uses environment variable
        include_examples (bool): Whether to include examples in entity descriptions
        custom_instructions (Optional[str]): Additional custom instructions

    Returns:
        Dict[str, Any]: Response with extracted entities and metadata

    Raises:
        ValueError: If required parameters are missing
        openai.OpenAIError: If API call fails
    """

    # Validate inputs
    if not text.strip():
        raise ValueError("text cannot be empty")

    # Get API key
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter"
        )

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Assemble the prompt
    assembled_prompt = assemble_ner_prompt(
        text=text,
        entity_types=entity_types,
        prompt_template=prompt_template,
        include_examples=include_examples,
        custom_instructions=custom_instructions,
    )

    try:
        # Make API call
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": assembled_prompt}],
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
                "extracted_entities": parsed_json,
                "input_text": text,
                "entity_types_used": list(entity_types.keys())
                if entity_types
                else list(ENTITY_TYPES.keys()),
                "model_used": model,
                "tokens_used": response.usage.total_tokens if response.usage else None,
            }
        except json.JSONDecodeError as e:
            result = {
                "error": "Failed to parse JSON response from OpenAI",
                "raw_response": response_content,
                "json_error": str(e),
                "input_text": text,
                "entity_types_used": list(entity_types.keys())
                if entity_types
                else list(ENTITY_TYPES.keys()),
            }

        return result

    except openai.OpenAIError as e:
        return {
            "error": f"OpenAI API error: {str(e)}",
            "input_text": text,
            "entity_types_used": list(entity_types.keys())
            if entity_types
            else list(ENTITY_TYPES.keys()),
        }

    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "input_text": text,
            "entity_types_used": list(entity_types.keys())
            if entity_types
            else list(ENTITY_TYPES.keys()),
        }


def extract_entities_simple(text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Simplified version of entity extraction with minimal parameters.

    Args:
        text (str): The text to extract entities from
        api_key (Optional[str]): OpenAI API key. If None, uses environment variable

    Returns:
        Dict[str, Any]: Response with extracted entities
    """
    return extract_entities_with_openai(text=text, api_key=api_key)


# Example usage
if __name__ == "__main__":
    load_dotenv()

    # Example 1: Simple entity extraction
    sample_texts = [
        """
        John Smith works as a Software Engineer at Apple Inc. in San Francisco. 
        He previously worked at Google LLC in Mountain View, California. 
        The company's Marketing team is located in New York.
        """,
        """
        Valued at EUR412.8 million, the all-share deal is set to integrate the Greek stock exchange into Euronext's extensive European network, which currently manages about 25% of total cash equity trading activity across several major financial hubs. This integration is expected to provide Greek companies with access to a broader investment base, enhancing liquidity and offering greater opportunities for capital raises and bond issuances. Please mention the Source: https://www.indexbox.io/blog/euronexts-acquisition-of-athens-stock-exchange-a-new-era-for-greece/
        """,
        """
OpenAI on Thursday said it is launching a Stargate-branded AI data center in Norway, marking its first foray into Europe with such a project.

British firm Nscale will design and build the site as part of a 50-50 joint venture with Norwegian energy infrastructure firm Aker.

OpenAI will be a so-called “off-taker” in the project, meaning it will effectively buy capacity from the data center.

“Part of the purpose of this project is to partner with OpenAI and leverage European sovereign compute to release additional services and features to the European continent,” Josh Payne, CEO of Nscale, told CNBC in an interview on Thursday.
        """,
    ]

    for j, text in enumerate(sample_texts):
        print(f"Example {j}: Simple entity extraction")
        print(f"Text: {text}")

        try:
            result = extract_entities_simple(text)
            print("Result:")
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"Error: {e}")
            print("Make sure to set your OPENAI_API_KEY environment variable")

        print("\n" + "=" * 50 + "\n")
