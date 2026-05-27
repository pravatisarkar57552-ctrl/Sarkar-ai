import os
import sys
import subprocess
import webbrowser
from google import genai
from google.genai import types

# =====================================================================
# 🛠️ STEP 1: DEFINE SYSTEM AUTOMATION ACTIONS (The AI's Hands)
# =====================================================================

def open_application(app_name: str) -> str:
    """Opens common Windows desktop applications based on user request."""
    app_name = app_name.lower()
    try:
        if "chrome" in app_name:
            # Opens Google Chrome if installed in default path
            subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
            return "Successfully opened Google Chrome."
        elif "notepad" in app_name:
            subprocess.Popen("notepad.exe")
            return "Successfully opened Notepad."
        elif "calculator" in app_name or "calc" in app_name:
            subprocess.Popen("calc.exe")
            return "Successfully opened Calculator."
        else:
            return f"Application '{app_name}' is not registered in my system paths yet."
    except Exception as e:
        return f"Failed to open {app_name}. Error: {e}"

def launch_song(song_name: str) -> str:
    """Launches a music track by searching for it on YouTube."""
    try:
        # Format the query string safely for a browser URL search
        search_query = song_name.replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={search_query}"
        webbrowser.open(url)
        return f"Successfully opened YouTube search matrix for: '{song_name}'."
    except Exception as e:
        return f"Failed to launch song web matrix. Error: {e}"

# =====================================================================
# 🔐 STEP 2: MAINFRAME ENVIROMENT SETUP
# =====================================================================

def initialize_mainframe():
    """Securely fetches the API key from Windows Environment Variables."""
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("[-] System variable 'GEMINI_API_KEY' not found.")
        api_key = input("👉 Please enter your Gemini API Key to launch Sarkar AI: ").strip()
        if not api_key:
            print("[-] Access Denied. Mainframe shutting down.")
            sys.exit()

    try:
        return genai.Client(api_key=api_key)
    except Exception as e:
        print(f"[-] Critical Error initializing Client: {e}")
        sys.exit()

# =====================================================================
# 🚀 STEP 3: MAIN EXECUTION ENGINE
# =====================================================================

def main():
    print("=" * 50)
    print("         ⚡ SARKAR AI MAINFRAME ACTIVE ⚡         ")
    print("         [ Version 3.0 - Action Engine ]         ")
    print("=" * 50)
    
    client = initialize_mainframe()
    print("[+] Sarkar AI Mainframe successfully initialized! 🚀\n")
    
    system_instruction = (
        "You are Sarkar AI, an advanced terminal assistant built by Rajarshi Sarkar. "
        "You have the authority to interact with the host system using your provided tools. "
        "When the user requests to play a song or open a tool, use your tools immediately."
    )
    
    # Bundle your python functions into Gemini's tool inventory
    my_tools = [open_application, launch_song]

    try:
        # Passing tools to the chat configuration gives Gemini total control over them
        chat = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=my_tools,  # Gemini automatically decides when to call these functions
                temperature=0.4
            )
        )
    except Exception as e:
        print(f"[-] Failed to build chat matrix: {e}")
        return

    print("🤖 Sarkar AI: Systems fully loaded, Raju. (Type 'exit' to log out)\n")

    while True:
        try:
            user_input = input("👤 Raju: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'shutdown']:
                print("\n🤖 Sarkar AI: Signing off, sir. Matrix offline. 🕶️")
                break
                
            if not user_input:
                continue
                
            # Send message. The official SDK automatically detects if Gemini wants to call a function,
            # runs your python function locally, returns the result to Gemini, and prints the text response!
            response = chat.send_message(user_input)
            print(f"\n🤖 Sarkar AI: {response.text}\n")
            
        except KeyboardInterrupt:
            print("\n\n[!] Hard break detected. Closing mainframe cleanly.")
            break
        except Exception as e:
            print(f"\n[-] Communication error in stream: {e}\n")

if __name__ == "__main__":
    main()
