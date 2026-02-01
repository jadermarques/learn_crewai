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

USER_QUERY = "Como agentes de IA podem melhorar o planejamento urbano e a infraestrutura de cidades inteligentes?"


# set the OpenAI model (gpt-4o-mini)
# set the OpenAI model (gpt-4o-mini)
os.environ["MODEL"] = "gpt-4o-mini"
# set up the OpenAI API key 
# os.environ["OPENAI_API_KEY"] = get_openai_api_key()
# set the EXA API key
# os.environ["EXA_API_KEY"] = get_exa_api_key()


def run():
    """
    Run the crew.
    """
    # escreva sua consulta no valor "user_query"
    inputs = { 
        "user_query": USER_QUERY
    }

    try:
        DeepReserchAdvanced().crew().kickoff(inputs=inputs)
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
