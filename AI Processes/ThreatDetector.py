import boto3
from botocore.exceptions import ClientError

MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"

IMAGE_NAME = "AI Processes/image0.jpg"

bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")

with open(IMAGE_NAME, "rb") as f:
    image = f.read()

user_message = "Is this baby in danger? Give a danger level between 1-5. Output in JSON."

messages = [
    {
        "role": "user",
        "content": [
            {"image": {"format": "png", "source": {"bytes": image}}},
            {"text": user_message},
        ],
    }
]

response = bedrock_runtime.converse(
    modelId=MODEL_ID,
    messages=messages,
)
response_text = response["output"]["message"]["content"][0]["text"]
print(response_text)