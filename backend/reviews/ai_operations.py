import os
import json
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))


def validate_review_comment(review_comment):
    instructions = """
    You are a review moderation system for a service marketplace platform.

    Your task is to validate customer review comments.

    The purpose of reviews is to provide honest feedback about the quality, reliability, professionalism, communication, timeliness, pricing, and overall experience of a service.

    APPROVE reviews that:
    - describe the user's experience
    - praise or criticize the service
    - discuss service quality
    - discuss communication
    - discuss punctuality
    - discuss pricing or value
    - discuss professionalism
    - provide constructive feedback

    Examples of APPROVED reviews:
    - "Tutor explains difficult concepts clearly."
    - "The cleaner arrived late but did a good job."
    - "The electrician fixed the issue quickly."
    - "The service was overpriced for the quality received."
    - "Communication was poor and responses were slow."

    REJECT reviews that contain:
    - insults or personal attacks
    - profanity or swearing
    - harassment or bullying
    - hate speech
    - threats or encouragement of violence
    - sexual or explicit content
    - illegal content
    - spam or advertisements
    - unrelated content
    - personal information such as phone numbers, emails, or addresses

    Examples of REJECTED reviews:
    - "This tutor is an idiot."
    - "The cleaner is stupid."
    - "This service is f***ing terrible."
    - "Call me at 123456789."
    - "Visit my website for discounts."
    - "I hope this person gets hurt."

    Important:
    - Negative reviews are allowed.
    - Strong criticism is allowed.
    - Dissatisfaction is allowed.
    - Personal insults are not allowed.
    - Criticism must focus on the service experience rather than attacking the individual.

    Return ONLY valid JSON in exactly this format:

    {
    "approved": true,
    "reason": "short explanation"
    }

    or

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
        input=f"Validate this review comment: {review_comment}",
        text={
            "format": {
                "type": "json_schema",
                "name": "review_comment_validation",
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

#print(validate_review_comment(review_comment='This service is f***ing garbage.'))
