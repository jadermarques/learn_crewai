#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from deep_reserch_advanced.crew import DeepReserchAdvanced

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Este arquivo principal destina-se a ser uma forma de você executar sua
# equipe localmente, portanto, evite adicionar lógica desnecessária a este arquivo.

import os

# Substitua pelas entradas que você deseja testar; ele interpolará automaticamente
# as informações de tarefas e agentes.

USER_QUERY = "Qual o futuro dos agentes de IA?"


os.environ["MODEL"] = "gpt-4o-mini"



def run():
    """
    Run the crew.
    """
    print("## Iniciando a execução da Crew...")
    # escreva sua consulta no valor "user_query"
    inputs = { 
        "user_query": USER_QUERY
    }

    try:
        crew_instance = DeepReserchAdvanced().crew()
        print(f"## Objeto Crew criado. Agentes: {len(crew_instance.agents)}, Tarefas: {len(crew_instance.tasks)}")
        result = crew_instance.kickoff(inputs=inputs)
        print("########################\n## Resultado Final:\n########################\n")

        # Exibe resultados
        # Acessando a saída da crew
        print(f"Raw Output: {result.raw}")
        if result.json_dict:
            print(f"JSON Output: {json.dumps(result.json_dict, indent=2)}")
        if result.pydantic:
            print(f"Pydantic Output: {result.pydantic}")
        print(f"Tasks Output: {result.tasks_output}")
        print(f"Token Usage: {result.token_usage}")        
        print("########################\n## Resultado Final:\n########################\n")
        print(crew_instance.usage_metrics)


        # Salva o relatório final em um arquivo markdown local
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

        
    except Exception as e:
        raise RuntimeError(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    # escreva sua consulta no valor "user_query"
    inputs = { 
        "user_query": USER_QUERY
    }
    try:
        DeepReserchAdvanced().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise RuntimeError(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        DeepReserchAdvanced().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise RuntimeError(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    # escreva sua consulta no valor "user_query"
    inputs = { 
        "user_query": USER_QUERY
    }

    try:
        DeepReserchAdvanced().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise RuntimeError(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise ValueError("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "user_query": ""
    }

    try:
        result = DeepReserchAdvanced().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise RuntimeError(f"An error occurred while running the crew with trigger: {e}")

if __name__ == "__main__":
    run()
