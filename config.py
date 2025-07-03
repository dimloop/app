import os
from dotenv import load_dotenv
from langchain_openai       import ChatOpenAI
from langchain_anthropic    import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_llm(
    provider: str = "openai",
    model: str | None = None,
    temperature: float = 0.2,
):
    provider = provider.lower()

    if provider == "openai":
        return ChatOpenAI(
            model=model or "gpt-4o",
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY"),
        )

    if provider == "claude":
        return ChatAnthropic(
            model=model or "claude-3-5-sonnet-latest",
            temperature=temperature,
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )

    if provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=model or "gemini-1.5-pro",
            temperature=temperature,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )

    raise ValueError(f"Unknown provider: {provider}")

