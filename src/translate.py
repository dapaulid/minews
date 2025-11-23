import ai
import utils

def translate_briefing(briefing: str, target_language: str) -> str:
    prompt = utils.load_file("prompts/article-translator.md")
    prompt = prompt.format_map({"target_language": target_language})
    prompt += f"\n{briefing}\n"
    translation = ai.exec(prompt, f"translate briefing to {target_language}")
    return translation
