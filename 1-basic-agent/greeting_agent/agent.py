from google.adk.agents import Agent

root_agent = Agent(
    name="greeting_user",
    model="gemini-2.5-flash",
    description="Greeting agent",
    instruction="""
    You are a helful assitant that greets the user. 
    Aks for the user's name and greet them by name.
    """,
)