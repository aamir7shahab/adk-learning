import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent

load_dotenv()

# Creating a new in-memory session service to store state
sesssion_service_stateful = InMemorySessionService()

initial_state = {
    "user_name": "Aamir Shahab",
    "user_preferences": """
        I like to play Football, Cricket, and Pool.
        My favorite food is Indian.
        My favorite TV show is Breaking Bad.
    """,
}

# Create a NEW Session
APP_NAME = "Aamir Bot"
USER_ID = "aamir_shahab"
SESSION_ID = str(uuid.uuid4())
stateful_session = sesssion_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)
print("Created New Session:")
print(f"\t Session ID: {SESSION_ID}")

# Creating new Runner
runner = Runner(
    agent=question_answering_agent,
    app_name=APP_NAME,
    session_service=sesssion_service_stateful,
)

# Create new message
new_message = types.Content(
    role="user", parts=[types.Part(text="What is Aamir's favorite sports?")]
)

for event in runner.run(
    user_id=USER_ID, session_id=SESSION_ID, new_message=new_message
):
    if event.is_final_response():
        if event.content and event.content.parts:
            print(f"Final Response: {event.content.parts[0].text}")

print("----- Sesion Event Expolaration -----")
session = sesssion_service_stateful.get_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
)

# Log final Session State
print("----- Final Session State -----")
for key, value in session.state.items():
    print(f"{key}: {value}")
