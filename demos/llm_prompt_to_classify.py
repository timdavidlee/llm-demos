import json
import os
from typing import Dict, Any, Optional, List
import openai
from openai import OpenAI


def classify_text_with_openai(
    text_to_classify: str,
    classification_categories: List[str],
    system_prompt: Optional[str] = None,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.1,
    max_tokens: int = 1000,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Classify text using OpenAI's API and return results as JSON.

    Args:
        text_to_classify (str): The text to be classified
        classification_categories (List[str]): List of possible classification categories
        system_prompt (Optional[str]): Custom system prompt. If None, uses default
        model (str): OpenAI model to use (default: "gpt-3.5-turbo")
        temperature (float): Controls randomness (0.0 = deterministic, 1.0 = very random)
        max_tokens (int): Maximum number of tokens in response
        api_key (Optional[str]): OpenAI API key. If None, uses environment variable

    Returns:
        Dict[str, Any]: JSON response with classification results

    Raises:
        ValueError: If required parameters are missing
        openai.OpenAIError: If API call fails
    """

    # Validate inputs
    if not text_to_classify.strip():
        raise ValueError("text_to_classify cannot be empty")

    if not classification_categories:
        raise ValueError("classification_categories cannot be empty")

    # Get API key
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter"
        )

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    # Create default system prompt if none provided
    if system_prompt is None:
        system_prompt = f"""You are a text classification expert. Your task is to classify the given text into one of the following categories: {", ".join(classification_categories)}.

Please respond with a JSON object containing:
- "classification": the chosen category
- "confidence": a confidence score between 0 and 1
- "reasoning": a brief explanation of why this classification was chosen
- "alternative_categories": list of other categories that could apply (if any)

Example response format:
{{
    "classification": "category_name",
    "confidence": 0.85,
    "reasoning": "Brief explanation of the classification decision",
    "alternative_categories": ["other_category1", "other_category2"]
}}"""

    # Create the user message
    user_message = f"Please classify the following text:\n\n{text_to_classify}"

    try:
        # Make API call
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"},
        )

        # Extract and parse the response
        response_content = response.choices[0].message.content

        # Parse JSON response
        try:
            result = json.loads(response_content)

            # Add metadata to the response
            result.update(
                {
                    "input_text": text_to_classify,
                    "available_categories": classification_categories,
                    "model_used": model,
                    "tokens_used": response.usage.total_tokens
                    if response.usage
                    else None,
                }
            )

            return result

        except json.JSONDecodeError as e:
            # If JSON parsing fails, return a structured error response
            return {
                "error": "Failed to parse JSON response from OpenAI",
                "raw_response": response_content,
                "json_error": str(e),
                "input_text": text_to_classify,
                "available_categories": classification_categories,
            }

    except openai.OpenAIError as e:
        # Handle OpenAI API errors
        return {
            "error": f"OpenAI API error: {str(e)}",
            "input_text": text_to_classify,
            "available_categories": classification_categories,
        }

    except Exception as e:
        # Handle any other unexpected errors
        return {
            "error": f"Unexpected error: {str(e)}",
            "input_text": text_to_classify,
            "available_categories": classification_categories,
        }


def classify_text_simple(
    text_to_classify: str, categories: List[str], api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Simplified version of the classification function with minimal parameters.

    Args:
        text_to_classify (str): The text to be classified
        categories (List[str]): List of possible classification categories
        api_key (Optional[str]): OpenAI API key. If None, uses environment variable

    Returns:
        Dict[str, Any]: JSON response with classification results
    """
    return classify_text_with_openai(
        text_to_classify=text_to_classify,
        classification_categories=categories,
        api_key=api_key,
    )


# Example usage and testing
if __name__ == "__main__":
    # Example 1: Simple classification
    sample_text = (
        "I love this product! It works perfectly and exceeded my expectations."
    )
    categories = ["positive", "negative", "neutral"]

    print("Example 1: Simple sentiment classification")
    print(f"Text: {sample_text}")
    print(f"Categories: {categories}")

    # Note: You'll need to set your OpenAI API key as an environment variable
    # export OPENAI_API_KEY="your-api-key-here"

    try:
        result = classify_text_simple(sample_text, categories)
        print("Result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set your OPENAI_API_KEY environment variable")

    print("\n" + "=" * 50 + "\n")

    # Example 2: More complex classification with custom prompt
    sample_text2 = "The customer service was terrible. I waited on hold for 2 hours and they couldn't solve my problem."
    categories2 = [
        "customer_service_issue",
        "product_complaint",
        "billing_issue",
        "technical_support",
    ]

    custom_prompt = """You are a customer service classifier. Analyze the customer's message and categorize it appropriately.

Focus on the primary issue being described. If multiple issues are mentioned, choose the most prominent one."""

    print("Example 2: Customer service classification with custom prompt")
    print(f"Text: {sample_text2}")
    print(f"Categories: {categories2}")

    try:
        result2 = classify_text_with_openai(
            text_to_classify=sample_text2,
            classification_categories=categories2,
            system_prompt=custom_prompt,
        )
        print("Result:")
        print(json.dumps(result2, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set your OPENAI_API_KEY environment variable")
