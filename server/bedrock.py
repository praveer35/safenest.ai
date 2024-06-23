import boto3
import json
from xml.dom.minidom import parseString
from botocore.exceptions import ClientError

MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"
IMAGE_NAME = "baby.png"

bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")

with open(IMAGE_NAME, "rb") as f:
    image = f.read()

ml_prompt = ml_prompt = """
    For each hazard, provide a rating from 1 (lowest) to 10 (highest) to indicate the level of risk to the baby in the picture.\n
    For the rationale, you will explain why you give the rate of each factor and how dangerous the factors are on the subject baby IF AND ONLY IF you gave it a rating of 7 or above. If all ratings are below 7, simply state None.\n
    Output format:
    {
        choking: <integer>,
        electrical_shock: <integer>,
        hard_falling: <integer>,
        suffocation: <integer>,
        sharp_objects: <integer>,
        rationale: <string>
    }"""

messages = [
    {
        "role": "user",
        "content": [
            {"image": {"format": "png", "source": {"bytes": image}}},
            {"text": ml_prompt},
        ],
    }
]

response = bedrock_runtime.converse(
    modelId=MODEL_ID,
    messages=messages,
)
response_text = response["output"]["message"]["content"][0]["text"]
print(response_text)