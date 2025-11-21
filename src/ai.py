from openrouter import OpenRouter
import utils

def exec(prompt: str) -> str:
    with OpenRouter(
        api_key=utils.getenv("OPENROUTER_API_KEY")
    ) as client:
        response = client.chat.send(
            #model="openai/gpt-oss-120b",
            #model="openai/gpt-oss-20b",
            #model="minimax/minimax-m2",
            model="x-ai/grok-4.1-fast:free",
            messages=[
                {"role": "user", "content": prompt},
            ]
        )
        assert len(response.choices) == 1
        print(response.usage)
        return response.choices[0].message.content