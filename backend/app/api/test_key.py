import os
from dotenv import load_dotenv
import openai # Use the openai library

load_dotenv() # Load variables from .env

api_key_from_env = os.getenv("OPENAI_API_KEY")

print(f"--- Attempting to use API Key from .env ---")
print(f"Value read: '{api_key_from_env}'") # This will show you what's actually loaded

if not api_key_from_env:
    print("\nERROR: OPENAI_API_KEY was NOT found in your environment variables or .env file.")
    print("Ensure your .env file is in the same directory as this script and contains: OPENAI_API_KEY='sk-...'")
else:
    print(f"Key length: {len(api_key_from_env)}")
    if not api_key_from_env.startswith("sk-"):
         print("WARNING: The loaded key does not start with 'sk-'. This is unusual for an OpenAI API secret key.")
    try:
        print("\nAttempting to initialize OpenAI client and make a simple API call (list models)...")
        client = openai.OpenAI(api_key=api_key_from_env)
        client.models.list() # This is a basic, low-cost call to check authentication
        print("\nSUCCESS! The API key is valid and the connection to OpenAI works.")
        print(f"Value read: '{api_key_from_env}'")
    except openai.AuthenticationError as e:
        print(f"\nAUTHENTICATION FAILED: {str(e)}")
        print("This means the API key string that was sent to OpenAI was rejected by them.")
        print("1. Double-check the 'Value read' above against the key on the OpenAI dashboard. Are they IDENTICAL (no typos, no extra spaces, not truncated)?")
        print("2. If they are identical, consider generating a brand NEW API key from the OpenAI dashboard and using that new key in your .env file.")
        print("3. Check your OpenAI account for any billing issues or usage restrictions.")
    except Exception as e:
        print(f"\nAn UNEXPECTED ERROR occurred: {str(e)}")

print(f"--- End of test ---")