from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool, FileReadTool
from pydantic import BaseModel
import os
os.environ["SERPER_API_KEY"] = "2f405e5bfeba7f9d3a747170682d1a7ea5f57721"

class BlogPost(BaseModel):
    title: str
    content: str

@CrewBase
class BlogPostCrew():
    """Blog Post Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"    
    
    @agent
    def researcher(self) -> Agent:
        search_tool = SerperDevTool()
        model = LLM(model="ollama/llama3", temperature=0.2, base_url="http://localhost:11434")
        return Agent(
            config=self.agents_config["researcher"],
            tools=[search_tool],
            llm=model,
            verbose=True,
            allow_deligation=False,
            function_calling_llm=model
        )

    @agent
    def writer(self) -> Agent:
        model = LLM(model="ollama/llama3", temperature=0.7, base_url="http://localhost:11434")
        return Agent(
            config=self.agents_config["writer"],
            llm=model,
            verbose=True,
            allow_deligation=True
        )

    @task
    def research_topic(self) -> Task:
        return Task(
            config=self.tasks_config["research_topic"],
        )

    @task
    def generate_post(self) -> Task:
        return Task(
            config=self.tasks_config["generate_post"], 
            output_pydantic=BlogPost
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Blog Post Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )