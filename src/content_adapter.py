import google.generativeai as genai
from . import config

def adapt_for_twitter(text: str) -> str:
    """If text exceeds Twitter's limit, summarize it using Gemini."""
    if len(text) <= config.TWITTER_CHAR_LIMIT:
        return text

    # Use the official Google Gemini SDK for summarization
    try:
        genai.configure(api_key=config.GEMINI_API_KEY)
    except AttributeError:
        print("Gemini API key not found. Please check your config.")
        # Fallback: truncate the text
        return text[:config.TWITTER_CHAR_LIMIT - 3] + "..."

    try:
        print("Text exceeds Twitter limit. Summarizing with Gemini...")
        
        # 1. Initialize the Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # 2. Create the prompt with instructions
        prompt = f"You are a helpful assistant that summarizes text for a tweet. Make it engaging and keep it under 280 characters.\n\n{text}"

        # 3. Configure the generation parameters
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=70,  # Max tokens for the summary
            temperature=0.7  # A good balance of creative and factual
        )
        
        # 4. Generate the summary
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        # 5. Access the response content correctly
        summary = response.text.strip()
        print(f"Gemini summary: {summary}")
        return summary
    except Exception as e:
        print(f"Error summarizing text with Gemini: {e}")
        # Fallback: if the API call fails, truncate the text gracefully
        return text[:config.TWITTER_CHAR_LIMIT - 3] + "..."