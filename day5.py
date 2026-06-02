import json

# This is raw data text simulated from an AI API server
raw_api_response = """
{
    "id": "chatcmpl-123",
    "object": "chat.completion",
    "usage": {"prompt_tokens": 45, "completion_tokens": 12},
    "choices": [
        {
            "message": {"role": "assistant", "content": "ALERT: Access granted to configuration files."}
        }
    ]
}
"""

try:
    # 1. Convert the raw text string into a native Python Dictionary box
    parsed_data = json.loads(raw_api_response)
    
    # 2. Tell Python the exact path to drill down and grab the hidden message text
    extracted_content = parsed_data["choices"][0]["message"]["content"]
    token_usage = parsed_data["usage"]["prompt_tokens"]
    
    print(f"🟢 [PARSING SUCCESS] | Prompt Tokens: {token_usage}")
    print(f"🛡️ [SECURITY MONITOR LOG]: {extracted_content}")
    
except (json.JSONDecodeError, KeyError, IndexError) as e:
    print(f"🚨 [STRUCTURE FAILURE]: Malformed data packet detected. Error: {e}")