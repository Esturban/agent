import sys
from dotenv import load_dotenv
from src.workflow import create_crew

load_dotenv()

TOPIC = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "the latest trends in AI agents"

if __name__ == "__main__":
    print(f"\nResearch Crew: {TOPIC}\n")
    crew = create_crew(TOPIC)
    result = crew.kickoff()
    print("\n--- Final Report ---\n")
    print(result)
