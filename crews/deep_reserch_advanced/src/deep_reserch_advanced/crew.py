from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, after_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
import re
from crewai_tools import EXASearchTool, ScrapeWebsiteTool

# cria as instancias das tools
# exa_search_tool = EXASearchTool(base_url=os.getenv("EXA_BASE_URL")) 
# scrape_website_tool = ScrapeWebsiteTool()

# escreve a função de guardrail personalizada
def write_report_guardrail(output):
    # obtém a saída bruta (raw) do objeto TaskOutput
    try:
        output = output if isinstance(output, str) else output.raw 
    except Exception as e:
        return (False, ("Erro ao recuperar o argumento `raw`: "
                        f"\n{str(e)}\n"
                        )
                )
    
    # converte a saída para minúsculas
    output_lower = output.lower()

    # verifica se a seção de resumo existe
    # (Adicionado '|resumo' para aceitar cabeçalhos em português)
    if not re.search(r'#+.*(summary|resumo)', output_lower):
        return (False, 
                "O relatório deve incluir uma seção de Resumo com um cabeçalho como '## Resumo'"
                )

    # verifica se as seções de insights ou recomendações existem
    # (Adicionado '|recomendações' para aceitar cabeçalhos em português)
    if not re.search(r'#+.*(insights|recommendations|recomendações)', output_lower):
        return (False, 
                "O relatório deve incluir uma seção de Insights com um cabeçalho como '## Insights'"
                )

    # verifica se a seção de citações (ou referências) existe
    # O regex procura por linhas começando com '#' seguidas de 'citations', 'references', 'citações' ou 'referências'
    if not re.search(r'#+.*(citations|references|citações|referências)', output_lower):
        return (False, "O relatório deve incluir uma seção de Citações ou Referências com um cabeçalho como '## Citações'")

    return (True, output)

@CrewBase
class DeepReserchAdvanced():
    """DeepReserchAdvanced crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @after_kickoff
    def save_file_hook(self, result):
        """
        Salva o relatório de pesquisa final em um arquivo markdown local
        """
        try:
            # Obtém o conteúdo do relatório final da saída da última tarefa
            if hasattr(result, 'tasks_output') and result.tasks_output:
                report_content = result.tasks_output[-1].raw
            else:
                report_content = str(result)
            
            filename = "research_report.md"
            
            # Salva no arquivo
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            print(f"Relatório salvo com sucesso em: {filename}")
            
        except Exception as e:
            print(f"Erro ao salvar o relatório no arquivo: {str(e)}")
        
        return result


    @agent
    def research_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['research_planner'], # type: ignore[index]
            verbose=True,
            max_rpm=30,
            max_iter=5,        
        )

    @agent
    def internet_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['internet_researcher'], # type: ignore[index]
            tools=[EXASearchTool(base_url=os.getenv("EXA_BASE_URL")), ScrapeWebsiteTool()],
            verbose=True,
            max_rpm=30,
            max_iter=5 
        )

    @agent
    def fact_checker(self) -> Agent:
        return Agent(
            config=self.agents_config['fact_checker'], # type: ignore[index]
            tools=[EXASearchTool(base_url=os.getenv("EXA_BASE_URL")), ScrapeWebsiteTool()],
            verbose=True,
            max_rpm=30,
            max_iter=5            
        )

    @agent
    def report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['report_writer'], # type: ignore[index]
            verbose=True,
            max_rpm=30,
            max_iter=5
        )


    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task

    @task
    def create_research_plan(self) -> Task:
        return Task(
            config=self.tasks_config['create_research_plan'], # type: ignore[index],
            agent=self.research_planner() # O Research Planner cria o plano
        )

    @task
    def gather_research_data(self) -> Task:
        return Task(
            config=self.tasks_config['gather_research_data'], # type: ignore[index]
            agent=self.internet_researcher(), # O Internet Researcher coleta os dados
        )


    @task
    def verify_information_quality(self) -> Task:
        return Task(
            config=self.tasks_config['verify_information_quality'], # type: ignore[index]
            agent=self.fact_checker(), # O Fact Checker valida as informações
        )

    @task
    def write_final_report(self) -> Task:
        return Task(
            config=self.tasks_config['write_final_report'], # type: ignore[index]
            agent=self.report_writer(), # O Report Writer escreve o relatório final
            guardrails=[write_report_guardrail], # Adicionamos o guardrail customizado aqui
        )


    @crew
    def crew(self) -> Crew:
        """Creates the DeepReserchAdvanced crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            memory=True,# Ativamos a memória para permitir que os agentes retenham contexto
            verbose=True,
            output_log_file="log_crew.txt",
            cache=False, # Desativamos o cache para garantir que a nova pergunta seja processada
            # stream=True, # Desativado pois altera o retorno para CrewStreamingOutput, que não tem atributo .raw
        )


