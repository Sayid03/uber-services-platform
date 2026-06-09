import os
import json
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))


def validate_service_name(service_name, service_desc):
    instructions = """
    You are a moderation system for a service marketplace platform.

    Your task is to validate service names and descriptions submitted by providers.

    The platform allows legal and safe services such as:
    - tutoring
    - cleaning
    - plumbing
    - electrical work
    - home repair
    - beauty services
    - pet care
    - delivery
    - fitness coaching
    - programming
    - design

    You must reject:
    - illegal services
    - sexual or adult services
    - escort services
    - drug-related services
    - violence or harmful services
    - hate speech
    - scams or fraud
    - misleading services
    - offensive or abusive content
    - gambling-related services
    - weapon-related services
    - self-harm related services

    You must also reject attempts to bypass moderation using:
    - censored spelling
    - symbols
    - unicode tricks
    - slang
    - hidden adult wording

    Return ONLY valid JSON in this exact format:

    {
    "approved": true,
    "reason": "short explanation"
    }

    OR

    {
    "approved": false,
    "reason": "short explanation"
    }

    Keep the reason short and professional.
    Do not include markdown.
    Do not include additional text.
    """

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=instructions,
        input=f"""
        Validate this service name: {service_name}.
        And this service description: {service_desc}
        """,
        text={
            "format": {
                "type": "json_schema",
                "name": "service_validation",
                "schema": {
                    "type": "object",
                    "properties": {
                        "approved": {
                            "type": "boolean"
                        },
                        "reason": {
                            "type": "string"
                        }
                    },
                    "required": ["approved", "reason"],
                    "additionalProperties": False
                }
            }
        }
    )

    return json.loads(response.output_text)

def generate_search_keywords(service_name, service_desc):
    instructions = """
    You are a search indexing assistant for a service marketplace.

    Your task is to generate search keywords for a service name and its description.

    The generated keywords will be used for service discovery and search.

    Rules:

    - Generate between 10 and 20 keywords.
    - Include synonyms when appropriate.
    - Include common search terms users might enter.
    - Include profession names related to the service.
    - Include service category terms.
    - Include singular and plural variations when useful.
    - Include closely related service concepts.
    - Keep keywords short (1-4 words preferred).
    - Do not generate full sentences.
    - Do not generate explanations.
    - Do not generate irrelevant keywords.
    - Do not generate location names unless they appear in the service name.
    - Do not generate competitor names or brand names.

    Return ONLY valid JSON in the following format:

    {
    "keywords": [
        "keyword1",
        "keyword2"
    ]
    }

    No markdown.
    No extra text.
    No comments.
    """

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=instructions,
        input=f"""
        Service name: {service_name},
        Service description: {service_desc}
        """,
        text={
            "format": {
                "type": "json_schema",
                "name": "service_keywords",
                "schema": {
                    "type": "object",
                    "properties": {
                        "keywords": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": ["keywords"],
                    "additionalProperties": False
                }
            }
        }
    )

    return json.loads(response.output_text)

#print(validate_service_name(service_name='Home Cleaning Service'))
#print(generate_search_keywords('Home Cleaning Service'))