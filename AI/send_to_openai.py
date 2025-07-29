
# TODO: Import your libaries
import asyncio
from secrets import API_KEY
from openai import OpenAI
import base64


client = OpenAI(api_key = API_KEY)

import asyncio

from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

openai = AsyncOpenAI(api_key = API_KEY)


def encode_image(image_path):
    with open(image_path, "rb") as image_F:
        return base64.b64encode(image_F.read()).decode('utf-8')

image_path = "otter.png"
base64_image = encode_image(image_path)

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "what's in this image? And answer if possible"},
            {
                "type": "input_image",
                "image_url": f"data:image/png;base64,{base64_image}",
            },
        ],
    }],
)

#print(response.output_text)


strInput = response.output_text

async def main() -> None:
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=strInput,
        instructions="Speak in a clandestine and professional voice. Like a operator speaking to spy agent",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

if __name__ == "__main__":
    asyncio.run(main())

'''

# Image encoding, code provided
def encode_image(image_path):
    with open(image_path, "rb") as image_F:
        return base64.b64encode(image_F.read()).decode('utf-8')

image_path = "7_9.png"
base64_image = encode_image(image_path)

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "what's in this image?"},
            {
                "type": "input_image",
                "image_url": f"data:image/png;base64,{base64_image}",
            },
        ],
    }],
)

print(response.output_text)

'''
response = client.responses.create(
    model="gpt-4.1-mini",
    input="Generate an image of a spy watch that has sonic sensor, camera and more",
    tools=[{"type": "image_generation"}],
)
'''
# Save the image to a file
image_data = [
    output.result
    for output in response.output
    if output.type == "image_generation_call"
]
    
if image_data:
    image_base64 = image_data[0]
    with open("otter.png", "wb") as f:
        f.write(base64.b64decode(image_base64))
# TODO: Maybe you need a key?

'''


# TODO: Sending a request and getting a response



# TODO: How do we make things audible?
    


# TODO: Can we put everything together?

