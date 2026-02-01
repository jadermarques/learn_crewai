#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from deep_research_01.crew import DeepResearch01

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Este arquivo principal destina-se a ser uma forma de você executar sua
# equipe localmente, portanto, evite adicionar lógica desnecessária a este arquivo.

# Substitua pelas entradas que você deseja testar; ele interpolará automaticamente
# as informações de tarefas e agentes.

def run():
    """
    Run the crew.
    """
    inputs = {
        'user_query': 'Oportunidade de Consultor de IA',
        'current_year': str(datetime.now().year)
    }

    try:
        DeepResearch01().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise RuntimeError(f"An error occurred while running the crew: {e}") from e


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'user_query': 'Oportunidade de Consultor de IA',
        'current_year': str(datetime.now().year)
    }
    try:
        DeepResearch01().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise RuntimeError(f"An error occurred while training the crew: {e}") from e

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        DeepResearch01().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise RuntimeError(f"An error occurred while replaying the crew: {e}") from e

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'user_query': 'Oportunidade de Consultor de IA',
        'current_year': str(datetime.now().year)
    }

    try:
        DeepResearch01().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise RuntimeError(f"An error occurred while testing the crew: {e}") from e

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
        "user_query": "",
        "current_year": ""
    }

    try:
        result = DeepResearch01().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise RuntimeError(f"An error occurred while running the crew with trigger: {e}") from e
