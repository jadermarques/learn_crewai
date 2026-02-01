import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	ScrapeWebsiteTool,
	EXASearchTool
)
# import the guardrail
from deep_research_coord.guardrails.guardrails import write_report_guardrail
# import custom tool
from deep_research_coord.tools.chart_generator_tool import ChartGeneratorTool
from deep_research_coord.utils import get_exa_api_key
# import the knowledge source
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource

# set the exa API key
os.environ["EXA_API_KEY"] = get_exa_api_key()

@CrewBase
class ParallelDeepResearchCrew:
    """ParallelDeepResearch crew"""

    # Define the agents
    @agent
    def research_planner(self) -> Agent:
        return Agent(
            config=self.agents_config["research_planner"],
            llm='gpt-4o',
            verbose=True
        )

    @agent
    def topic_researcher(self) -> Agent:

        return Agent(
            config=self.agents_config["topic_researcher"],
            # Define the tools 
            tools=[
                # add the EXASearchTool
				EXASearchTool(base_url=os.getenv("EXA_BASE_URL")),
                # add the web scraping tool
                ScrapeWebsiteTool()
            ],
            # set the llm for the task.
            llm='gpt-4o-mini',
            verbose=True,
            max_rpm=15,
            max_iter=5
        )
    
    @agent
    def fact_checker(self) -> Agent:
     
        return Agent(
            config=self.agents_config["fact_checker"],
            # Define the tools 
            tools=[
                # add the EXASearchTool
				EXASearchTool(base_url=os.getenv("EXA_BASE_URL")),
                # add the web scraping tool
                ScrapeWebsiteTool()
            ],
            llm='gpt-4o',
            verbose=True,
            max_rpm=15,
            max_iter=5
        )
    
    
    @agent
    def report_writer(self) -> Agent:
        
        return Agent(
            config=self.agents_config["report_writer"],
            llm='gpt-4o',
            # Add the instance of the custom ChartGeneratorTool
            tools=[ChartGeneratorTool()],
            verbose=True,
            max_rpm=15,
            max_iter=5
        )
    
    @task
    def create_research_plan(self) -> Task:
        return Task(
            config=self.tasks_config["create_research_plan"],
        )
    

    # Define the tasks
    @task
    def research_main_topics(self) -> Task:
        return Task(
            config=self.tasks_config["research_main_topics"],
            # set the execution to async so the research tasks run in parallel
            async_execution=False,
        )
    
    @task
    def research_secondary_topics(self) -> Task:
        return Task(
            config=self.tasks_config["research_secondary_topics"],
            
            ### START CODE HERE ###
            # set the execution to async so the research tasks run in parallel
            async_execution=False,
            ### END CODE HERE ###
        )
    
    @task
    def validate_main_topics(self) -> Task:
        return Task(
            config=self.tasks_config["validate_main_topics"],
        )
    
    @task
    def validate_secondary_topics(self) -> Task:
        return Task(
            config=self.tasks_config["validate_secondary_topics"],
        )
    
    @task
    def write_final_report(self) -> Task:
        return Task(
            config=self.tasks_config["write_final_report"],
            
        ### START CODE HERE ###
        # add the guardrail
        guardrails=[write_report_guardrail],
        # enable markdown output
        markdown_output=True,
        # set the output file name to "final_report.md"
        output_file="final_report.md"
        ### END CODE HERE ###
        )


    # Define the crew
    @crew
    def crew(self) -> Crew:
        """Creates the ParallelDeepResearchCrew crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            
            ### START CODE HERE ###
            # allow crew to use memory to store memories of it's execution
            memory=True,
            process=Process.sequential,
            tracing=False, # please, do not change this value
            verbose=True,
            knowledge_sources=[TextFileKnowledgeSource(
                file_paths=["user_preference.txt"]
            )]
        )
