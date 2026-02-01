# DeepResearchCoord Crew

Welcome to the DeepResearchCoord Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/deep_research_coord/config/agents.yaml` to define your agents
- Modify `src/deep_research_coord/config/tasks.yaml` to define your tasks
- Modify `src/deep_research_coord/crew.py` to add your own logic, tools and specific args
- Modify `src/deep_research_coord/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the deep_research_coord Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Estrutura do Projeto e Componentes

Este projeto utiliza o framework CrewAI para coordenar uma equipe de agentes de IA autônomos que realizam pesquisas profundas e geram relatórios detalhados. Abaixo, detalhamos como cada componente funciona:

### Agentes
O crew é composto por 4 agentes especializados, definidos em `src/deep_research_coord/config/agents.yaml`:

1.  **Planejador de Pesquisa (`research_planner`)**
    *   **Função:** Estrategista de pesquisa.
    *   **Objetivo:** Analisa a consulta do usuário e a decompõe em tópicos principais (essenciais) e secundários (contexto/apoio). Cria o roteiro para a investigação.

2.  **Pesquisador de Tópicos (`topic_researcher`)**
    *   **Função:** Investigador online.
    *   **Objetivo:** Realiza a busca ativa de informações na internet para os tópicos definidos.
    *   **Ferramentas:** Utiliza `EXASearchTool` para buscar e `ScrapeWebsiteTool` para extrair conteúdo de páginas.

3.  **Verificador de Fatos (`fact_checker`)**
    *   **Função:** Controle de qualidade (QA).
    *   **Objetivo:** Revisa os dados coletados, cruza informações para evitar alucinações, verifica a credibilidade das fontes e garante a precisão dos fatos.

4.  **Redator de Relatórios (`report_writer`)**
    *   **Função:** Escritor técnico e sintetizador.
    *   **Objetivo:** Compila todas as informações validadas em um relatório final coerente, estruturado e com citações.
    *   **Ferramentas:** Possui uma ferramenta personalizada `ChartGeneratorTool` para criar gráficos visuais.

### Tarefas (Tasks)
O fluxo de trabalho é sequencial e lógico, definido em `src/deep_research_coord/config/tasks.yaml`:

1.  **`create_research_plan`**: O Planejador quebra a dúvida do usuário em um plano estruturado.
2.  **`research_main_topics`** e **`research_secondary_topics`**: O Pesquisador coleta dados para cada grupo de tópicos.
3.  **`validate_main_topics`** e **`validate_secondary_topics`**: O Verificador de Fatos audita as informações coletadas.
4.  **`write_final_report`**: O Redator gera o arquivo final em Markdown (`final_report.md`), aplicando guardrails de segurança e incorporando gráficos.

### Memória e Conhecimento (Memory & Knowledge)
*   **Memória:** O projeto está configurado com `memory=True`, permitindo que o crew armazene e recupere memórias de execuções passadas (Short-term, Long-term, Entity Memory) para melhorar a continuidade e contexto.
*   **Knowledge Source:** O crew utiliza uma fonte de conhecimento baseada em arquivo de texto (`user_preference.txt`), permitindo que as preferências do usuário influenciem a execução da pesquisa.

### Ferramentas e Configurações Adicionais
*   **Guardrails:** O projeto implementa guardrails (`write_report_guardrail`) na tarefa de escrita para garantir a qualidade e segurança do output.
*   **Charts:** Geração de gráficos automatizada via `ChartGeneratorTool`, salvando plots em `deep_research_crew/plots/`.

## Support

For support, questions, or feedback regarding the DeepResearchCoord Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
