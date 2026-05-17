# LangChain Course

A hands-on LangChain project exploring different agent patterns using OpenAI and Tavily Search.

---

## Project Structure

```
langchain-course/
├── main.py            # Classic tool-calling agent (AgentExecutor pattern)
├── search-agent.py    # Modern structured-output agent (create_agent pattern)
├── pyproject.toml     # Dependencies
└── README.md
```

---

## Environment Setup

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
```

Install dependencies:

```bash
uv sync
```

---

## Agent Implementations

### `main.py` — Classic Tool-Calling Agent

Uses the **`create_tool_calling_agent` + `AgentExecutor`** pattern — the stable, widely-documented LangChain API.

**How it works:**

```
ChatPromptTemplate (system + human + scratchpad)
        ↓
create_tool_calling_agent(llm, tools, prompt)
        ↓
AgentExecutor.invoke({"input": "..."})
        ↓
{"output": "plain text answer"}
```

**Key characteristics:**
- You manually define the **system prompt**, the user message slot (`{input}`), and the **agent scratchpad** — the memory slot where tool call/result history is stored between reasoning steps.
- `AgentExecutor` drives the reasoning loop: LLM decides to call a tool → tool runs → result is fed back → LLM reasons again → repeats until it returns a final answer.
- Output is a **plain string** inside `result["output"]`.
- Agent is scoped **inside `main()`** — clean, no global state, easy to test.
- Uses `gpt-4o-mini` — cost-efficient and widely available.

**When to use:**
- Learning LangChain agent concepts.
- When you need full control over the prompt.
- Freeform conversational answers where plain text is fine.

---

### `search-agent.py` — Structured Output Agent

Uses the **`create_agent` + `response_format`** pattern — a newer, higher-level API built on LangGraph internals.

**How it works:**

```
Pydantic models: AgentResponse { answer, sources[] }
        ↓
create_agent(model=llm, tools=tools, response_format=AgentResponse)
        ↓
agent.invoke({"messages": HumanMessage(...)})
        ↓
AgentResponse(answer="...", sources=[Source(url="..."), ...])
```

**Key characteristics:**
- Uses **Pydantic schemas** (`AgentResponse`, `Source`) to enforce typed, structured output. The LLM is instructed to return JSON matching the schema automatically.
- No explicit prompt template needed — the framework injects tool descriptions and the response schema internally.
- Returns a **typed object** with `answer` (string) and `sources` (list of URLs) — ideal for downstream processing, REST APIs, or UI rendering.
- Agent is currently initialized at **module level** (global) — simple for scripts but should be moved inside a function for production use.
- Uses `gpt-5` — powerful but check availability on your API plan.

**When to use:**
- Production applications where structured, parseable output is required.
- When you need to return sources alongside answers.
- Building APIs or UIs that consume agent results.

---

## Side-by-Side Comparison

| Aspect | `main.py` | `search-agent.py` |
|---|---|---|
| Agent API | `create_tool_calling_agent` + `AgentExecutor` | `create_agent` with `response_format` |
| Prompt | Explicit `ChatPromptTemplate` | Implicit (handled internally) |
| Output type | Plain string | Pydantic model (`answer` + `sources`) |
| Model | `gpt-4o-mini` | `gpt-5` |
| Agent scope | Inside function (clean) | Module-level global |
| Boilerplate | More explicit | Less boilerplate |
| Best for | Learning, flexible prompting | Production, structured output |

---

## Why Two Different Approaches?

| Reason | Explanation |
|---|---|
| **LangChain evolution** | `create_tool_calling_agent` + `AgentExecutor` is the **legacy stable API**. `create_agent` with `response_format` is the **newer high-level API** built on LangGraph. |
| **Use case** | `main.py` is better for freeform conversational answers. `search-agent.py` is better when you need predictable, parseable output. |
| **Explicitness vs convenience** | `main.py` gives full control over the prompt. `search-agent.py` trades control for less boilerplate. |

---

## Recommendation

**Use `search-agent.py`'s pattern for production** — structured output with typed sources is far more useful when building real applications (no string parsing, type safety, includes citations).

**Use `main.py`'s pattern for learning and custom prompting** — it's explicit, easy to debug, and matches most LangChain tutorials and documentation.

> **Note:** Two known improvements for `search-agent.py`:
> 1. Move the agent initialization inside `main()` to avoid global state.
> 2. Consider `gpt-4o` as a fallback if `gpt-5` is not available on your API plan.
