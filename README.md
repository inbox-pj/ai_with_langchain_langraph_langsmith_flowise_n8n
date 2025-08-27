# Flowise - Visual LLM Flow Builder - NoCode-LowCode AI Flows

## 🚀 LLM Docker Compose Stack
This project provides a Docker Compose setup for running multiple AI and data services, including Ollama, pgvector, PostgreSQL, Flowise, and n8n.


### Services
- Ollama: Local LLM inference server.
- pgvector: PostgreSQL extension for vector similarity search.
- Postgres: Main PostgreSQL database for n8n and Flowise.
- Flowise: Visual LLM workflow builder.
- n8n: Workflow automation tool.

```bash
    # Start Flowise, pgvector and ollama with Docker
    docker-compose up -d
```
#### Access services:
- Ollama: http://localhost:11434
- Flowise: http://localhost:3000
- n8n: http://localhost:5678
- PostgreSQL:
  - n8n: port 25432, DB n8n_db, user n8n_user, password postgres 
  - Flowise: port 25432, DB flowise, user flowise, password postgres 
  - pgvector: port 15432, DB vectord_db, user postgres, password postgres

# LangChain- AI Agents with LangChain & LangGraph 🦜🔗

**LangChain and LangGraph by building real world AI Agents (Python, Latest Version 0.3.0+)**

## ▶️ Getting Started

### 🛠️ Prerequisites
- **This is not a beginner course** - Basic software engineering concepts needed
- Familiarity with: git, Python, environment variables, classes, testing and debugging
- Python 3.10+
- Any Python package manager (uv, poetry, pipenv) - but NOT conda!
- Access to an LLM (can be open source via Ollama, or cloud providers like OpenAI, Anthropic, Gemini)
- No Machine Learning experience needed

### ⚙️ Setup Instructions

```bash
    # Setup Virtual Environment
    pipenv shell
   
    # Install dependencies
   pipenv install langchain && \
   pipenv install langchain-ollama  && \
   pipenv install langchain-community  && \
   pipenv install langchain-core  && \
   pipenv install langchainhub  && \
   pipenv install langchain_tavily
   
   # code formatter tool
   pipenv install black
   
   # environment variable loader
   pipenv install python-dotenv
   
   # Testing and debugging
    pipenv install pytest
```

## 🙏 Reference

- https://python.langchain.com/docs/introduction/
- https://python.langchain.com/docs/tutorials/llm_chain/
- https://langchain-ai.github.io/langgraph/tutorials/introduction/
- https://python.langchain.com/docs/integrations/chat/



<img width="1645" height="751" alt="image" src="https://github.com/user-attachments/assets/e8b56e63-c736-40e4-ae5b-72f18e664d46" />


# Prompt Engineering
## Best practices for prompt engineering:
	• Be clear and specific: Clearly state the task, context, and desired output.
	• Use examples: Provide input-output pairs to guide the model.
	• Set constraints: Specify format, length, or style requirements.
	• Break down complex tasks: Use step-by-step instructions or chain-of-thought prompts.
	• Iterate and refine: Test, analyze outputs, and adjust prompts for better results.
	• Avoid ambiguity: Use precise language and avoid vague terms.
	• Use system messages: Set behavior or tone if supported (e.g., “You are a helpful assistant.”).
	• Leverage role prompting: Assign roles to guide responses (e.g., “Act as a senior Java developer.”).
	• Test edge cases: Ensure prompts handle unusual or unexpected inputs.
	• Document prompts: Keep track of prompt versions and their effectiveness.


## Prompt engineering format
	• Role: Specify which role or capabilities the AI should assume.
	• Tasks/Instruction: Clearly state what you want the model to do.
	• Context: Provide background information or relevant details.
	• Input Data: Supply any data or examples needed for the task.
	• Goal: Define what is the outcome of the task should achieve.
	• Constraints: Specify requirements (e.g., output format, length, style).
	• Output Format: Determine how the result should be presented.


## Core prompting techniques for LLMs
	• Zero-shot prompting: Ask the model to perform a task without providing any examples.
	• Few-shot prompting: Provide a few input-output examples to guide the model’s behavio
	• Chain-of-thought (CoT) prompting: Encourage the model to reason step-by-step by explicitly asking for intermediate steps.


