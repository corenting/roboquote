"""Handle the generation of the quote."""
import json
import random
import re

import nltk
import requests
from loguru import logger

from roboquote import config, constants
from roboquote.entities.exceptions import CannotGenerateQuoteException


def _get_random_prompt(background_search_query: str) -> str:
    """Get a random prompt for the model."""
    prompts = [
        f"On a {background_search_query} themed picture, a fitting inspirational quote would be::",
        f"On a {background_search_query} themed inspirational picture , a fitting inspirational short quote would be:",
        f"On a {background_search_query} themed inspirational picture, a fitting short quote would be:",
    ]

    prompt = random.choice(prompts)

    # Randomly replace picture with photography
    if random.randint(0, 1) == 0:
        prompt = prompt.replace("picture", "photography")

    # Randomly replace such as with like
    if random.randint(0, 1) == 0:
        prompt = prompt.replace("such as", "like")

    # Add random amount of space in the end
    prompt = prompt + (" " * random.randint(0, 1))

    return prompt


def _cleanup_text(generated_text: str) -> str:
    """Cleanup the text generated by the model.

    Remove quotes, and limit the text to the first sentence.
    """
    logger.debug(f'Cleaning up quote: "{generated_text}"')

    # If the model generated a quoted text, get it directly
    quoted_text = generated_text.strip()
    regex_quotes_list = r"\"\“\«\”"
    regex_results = re.findall(
        rf"[{regex_quotes_list}]*([^{regex_quotes_list}]+)[{regex_quotes_list}]*",
        quoted_text,
    )
    if len(regex_results) > 0:
        logger.debug(f'Cleaned up quote is: "{regex_results[0]}"')
        return regex_results[0]

    # Else tokenize the text and get the first sentence
    text = nltk.sent_tokenize(generated_text)[0].strip()

    logger.debug(f'Cleaned up quote is: "{text}"')
    return text


def get_random_quote(background_search_query: str) -> str:
    """For a given background category, get a random quote."""
    prompt = _get_random_prompt(background_search_query)
    logger.debug(f'Prompt for model: "{prompt}"')

    headers = {
        "Authorization": f"Bearer {config.HUGGING_FACE_API_TOKEN}",
        "Content-Type": "application/json",
    }
    data = json.dumps({"inputs": prompt, "use_cache": False})

    response = requests.request(
        "POST", constants.HUGGING_FACE_API_URL, headers=headers, data=data
    )

    try:
        response_content = json.loads(response.content.decode("utf-8"))
    except json.JSONDecodeError:
        raise CannotGenerateQuoteException("Unknown error from Hugging Face.")

    # Error case with error message
    if not response.ok:
        raise CannotGenerateQuoteException(
            response_content.get("error", "Unknown error from Hugging Face.")
        )

    text: str = response_content[0]["generated_text"]
    text = text.replace(prompt, "")

    return _cleanup_text(text)
