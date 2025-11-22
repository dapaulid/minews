from openrouter import OpenRouter
import utils
from timeit import default_timer as timer

from dataclasses import dataclass

@dataclass
class UsageStats:
    input_tokens: int = 0
    output_tokens: int = 0
    reasoning_tokens: int = 0
    requests: int = 0
    duration: float = 0.0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens + self.reasoning_tokens
    @property
    def bandwidth(self) -> float:
        return self.total_tokens / self.duration if self.duration > 0 else 0.0

total_usage = UsageStats()

def exec(prompt: str, description: str) -> str:
    print(f"Executing AI prompt: {description}...")
    start_time = timer()
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
    elapsed = timer() - start_time
    assert len(response.choices) == 1, f"Expected single response, got {len(response.choices)}"
    # record usage stats
    usage = UsageStats()
    usage.reasoning_tokens = int(response.usage.completion_tokens_details.reasoning_tokens)        
    usage.input_tokens = int(response.usage.prompt_tokens)
    usage.output_tokens = int(response.usage.completion_tokens) - usage.reasoning_tokens
    usage.requests = 1
    usage.duration = elapsed
    assert usage.total_tokens == response.usage.total_tokens, f"Token count mismatch: Expected {usage.total_tokens}, got {response.usage.total_tokens}"
    # update global stats
    total_usage.input_tokens += usage.input_tokens
    total_usage.output_tokens += usage.output_tokens
    total_usage.reasoning_tokens += usage.reasoning_tokens
    total_usage.requests += usage.requests
    total_usage.duration += usage.duration
    # done
    print(f"  done, took {usage.total_tokens} tokens and {usage.duration:.3f} seconds ({usage.bandwidth:.2f} tokens/s)")
    return response.choices[0].message.content

def print_usage():
    print("AI Usage Stats")
    print(f"  requests         : {total_usage.requests}")
    print(f"  input tokens     : {total_usage.input_tokens}")
    print(f"  output tokens    : {total_usage.output_tokens}")
    print(f"  reasoning tokens : {total_usage.reasoning_tokens}")
    print(f"  total tokens     : {total_usage.total_tokens}")
    print(f"  total duration   : {total_usage.duration:.0f} seconds")
    print(f"  bandwidth        : {total_usage.bandwidth:.2f} tokens/s")