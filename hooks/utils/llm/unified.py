#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "openai",
#     "anthropic",
#     "python-dotenv",
# ]
# ///

import os
import sys
from dotenv import load_dotenv


def prompt_llm_openai(prompt_text, model=None, max_tokens=1000, temperature=None):
    """
    OpenAI LLM prompting method.
    
    Args:
        prompt_text (str): The prompt to send to the model
        model (str): Model to use (default: from env or gpt-4o)
        max_tokens (int): Maximum tokens in response
        temperature (float): Temperature for generation
    
    Returns:
        str: The model's response text, or None if error
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    
    # Use model from env or default to gpt-4o
    if model is None:
        model = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")
    
    try:
        from openai import OpenAI
        
        # Support custom API base for OpenAI-compatible services
        api_base = os.getenv("OPENAI_API_BASE")
        if api_base:
            client = OpenAI(api_key=api_key, base_url=api_base)
        else:
            client = OpenAI(api_key=api_key)
        
        # Set temperature based on model
        if temperature is None:
            temperature = 1.0 if "gpt-5" in model else 0.7
        
        # Use different parameter name for GPT-5 models
        if "gpt-5" in model:
            # GPT-5-nano requires at least 1000 max_completion_tokens
            gpt5_max_tokens = max(max_tokens, 1000)
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt_text}],
                max_completion_tokens=gpt5_max_tokens,
                temperature=temperature,
            )
        else:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt_text}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        if os.getenv("DEBUG"):
            print(f"OpenAI error: {e}", file=sys.stderr)
        return None


def prompt_llm_anthropic(prompt_text, model="claude-3-5-haiku-20241022", max_tokens=1000, temperature=0.7):
    """
    Anthropic LLM prompting method.
    
    Args:
        prompt_text (str): The prompt to send to the model
        model (str): Model to use (default: claude-3-5-haiku)
        max_tokens (int): Maximum tokens in response
        temperature (float): Temperature for generation
    
    Returns:
        str: The model's response text, or None if error
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    
    try:
        import anthropic
        
        client = anthropic.Anthropic(api_key=api_key)
        
        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt_text}],
        )
        
        return message.content[0].text.strip()
    
    except Exception as e:
        if os.getenv("DEBUG"):
            print(f"Anthropic error: {e}", file=sys.stderr)
        return None


def prompt_llm(prompt_text, max_tokens=1000, temperature=None, prefer_openai=True):
    """
    Unified LLM prompting with fallback.
    Tries OpenAI first (with gpt-5-nano), falls back to Anthropic.
    
    Args:
        prompt_text (str): The prompt to send to the model
        max_tokens (int): Maximum tokens in response
        temperature (float): Temperature for generation
        prefer_openai (bool): If True, try OpenAI first; if False, try Anthropic first
    
    Returns:
        str: The model's response text, or None if both fail
    """
    load_dotenv()
    
    if prefer_openai:
        # Try OpenAI first (uses model from env or defaults to gpt-4o)
        response = prompt_llm_openai(prompt_text, 
                                    max_tokens=max_tokens, temperature=temperature)
        if response:
            return response
        
        # Fall back to Anthropic
        response = prompt_llm_anthropic(prompt_text, 
                                       max_tokens=max_tokens, temperature=temperature)
        if response:
            return response
    else:
        # Try Anthropic first
        response = prompt_llm_anthropic(prompt_text, 
                                       max_tokens=max_tokens, temperature=temperature)
        if response:
            return response
        
        # Fall back to OpenAI (uses model from env or defaults to gpt-4o)
        response = prompt_llm_openai(prompt_text,
                                    max_tokens=max_tokens, temperature=temperature)
        if response:
            return response
    
    return None


def generate_completion_message():
    """
    Generate a completion message using unified LLM with fallback.
    
    Returns:
        str: A natural language completion message, or None if error
    """
    engineer_name = os.getenv("ENGINEER_NAME", "").strip()
    
    if engineer_name:
        name_instruction = f"Sometimes (about 30% of the time) include the engineer's name '{engineer_name}' in a natural way."
        examples = f"""Examples of the style: 
- Standard: "Work complete!", "All done!", "Task finished!", "Ready for your next move!"
- Personalized: "{engineer_name}, all set!", "Ready for you, {engineer_name}!", "Complete, {engineer_name}!", "{engineer_name}, we're done!" """
    else:
        name_instruction = ""
        examples = """Examples of the style: "Work complete!", "All done!", "Task finished!", "Ready for your next move!" """
    
    prompt = f"""Generate a short, friendly completion message for when an AI coding assistant finishes a task. 

Requirements:
- Keep it under 10 words
- Make it positive and future focused
- Use natural, conversational language
- Focus on completion/readiness
- Do NOT include quotes, formatting, or explanations
- Return ONLY the completion message text
{name_instruction}

{examples}

Generate ONE completion message:"""
    
    response = prompt_llm(prompt)
    
    # Clean up response - remove quotes and extra formatting
    if response:
        response = response.strip().strip('"').strip("'").strip()
        # Take first line if multiple lines
        response = response.split("\n")[0].strip()
    
    return response


def main():
    """Command line interface for testing."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--completion":
            message = generate_completion_message()
            if message:
                print(message)
            else:
                print("Error generating completion message")
        elif sys.argv[1] == "--test":
            # Test both APIs
            print("Testing LLM APIs...")
            load_dotenv()
            
            if os.getenv("OPENAI_API_KEY"):
                model = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")
                response = prompt_llm_openai("Say 'OpenAI works!'")
                if response:
                    print(f"✓ OpenAI ({model}): {response}")
                else:
                    print("✗ OpenAI failed")
            else:
                print("- OpenAI: No API key")
            
            if os.getenv("ANTHROPIC_API_KEY"):
                response = prompt_llm_anthropic("Say 'Anthropic works!'")
                if response:
                    print(f"✓ Anthropic: {response}")
                else:
                    print("✗ Anthropic failed")
            else:
                print("- Anthropic: No API key")
            
            # Test unified with fallback
            response = prompt_llm("Say 'Unified LLM works!'")
            if response:
                print(f"✓ Unified (with fallback): {response}")
            else:
                print("✗ No LLM available")
        else:
            prompt_text = " ".join(sys.argv[1:])
            response = prompt_llm(prompt_text)
            if response:
                print(response)
            else:
                print("Error: No LLM API available or both failed")
    else:
        print("Usage: ./unified.py 'your prompt here' or ./unified.py --completion or ./unified.py --test")


if __name__ == "__main__":
    main()