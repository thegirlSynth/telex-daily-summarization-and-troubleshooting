from typing import List
from groq import Groq
from app.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def call_ai(prompt: str) -> str:
    """Calls Groq API to generate responses based on the given prompt."""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are an AI assistant."}, {"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error processing AI request: {str(e)}"

async def summarize_messages(messages: List[str]) -> tuple[str, str]:
    """Generates a structured summary of messages and identifies potential issues."""
    message_text = "\n".join(messages)
    prompt = f"""
    You are a conversation summarizer for a work channel. Your job is to generate a structured summary of the discussions.

    Format your response as follows:

    **📝 Daily Summary:**
    (Provide a clear, concise, human-readable summary of the key points from the messages.)

    **🛠️ Suggestions/Quick Fixes:**
    (If any issues or technical challenges are detected, provide solutions or recommendations.)

    Messages to summarize:
    {message_text}
    """

    raw_response = call_ai(prompt)
    response = raw_response.replace("**", "")

    # Attempt to split response into "Summary" and "Suggestions/Quick Fixes"
    if "**Suggestions/Quick Fixes:**" in response:
        summary, suggestions = response.split("**Suggestions/Quick Fixes:**")
    else:
        summary, suggestions = response, "No issues detected today! 😊"

    return summary.strip(), suggestions.strip()

async def generate_troubleshooting(issue_description: str) -> str:
    """Generates structured troubleshooting steps for identified issues."""
    prompt = f"""
    You are an AI assistant providing troubleshooting steps for issues in a team discussion.

    **Instructions:**
    - Organize troubleshooting steps under numbered issues.
    - Each issue should have a short title (e.g., '1. The Possibility of Making $100,000 in 40 Weeks').
    - Use bullet points (a, b, c) to provide structured, actionable advice.
    - Ensure responses are practical and easy to follow.

    **Issue to address:**
    {issue_description}

    Format your response as follows:

    **Troubleshooting Steps:**
    1. **[Issue Title]**
       a) [Step 1]
       b) [Step 2]
       c) [Step 3]

    2. **[Next Issue Title]**
       a) [Step 1]
       b) [Step 2]

    Provide troubleshooting only if issues exist; otherwise, state: 'No issues requiring troubleshooting today!'
    """

    raw_response = call_ai(prompt)

    raw_response = raw_response.replace("**", "")

    return raw_response
