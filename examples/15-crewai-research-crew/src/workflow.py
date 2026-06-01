from crewai import Agent, Crew, Task
from src.tools import web_search


def create_crew(topic: str) -> Crew:
    researcher = Agent(
        role="Researcher",
        goal=f"Find accurate, recent information about: {topic}",
        backstory="A thorough researcher who identifies reliable sources and extracts key facts.",
        tools=[web_search],
        verbose=True,
    )

    writer = Agent(
        role="Writer",
        goal="Turn the researcher's findings into a clear, structured report",
        backstory="A concise technical writer who makes complex research readable.",
        verbose=True,
    )

    research_task = Task(
        description=f"Research '{topic}'. Gather 5–7 key facts with source references.",
        expected_output="A numbered list of key findings, each with a brief source note.",
        agent=researcher,
    )

    write_task = Task(
        description="Using the research findings, write a 200-word report: intro, key points, conclusion.",
        expected_output="A structured 200-word report with clearly labelled sections.",
        agent=writer,
        context=[research_task],
    )

    return Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        verbose=True,
    )
