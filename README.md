# LangChain Course

A hands-on LangChain project exploring different agent patterns using OpenAI and Tavily Search.

---

## Project Structure

```
langchain-course/
├── main.py            # Simple agent — plain text output (create_agent, LangChain 1.x)
├── search-agent.py    # Structured output agent — typed Pydantic response with sources
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

### `main.py` — Simple Agent (Plain Text Output)

Uses the **`create_agent`** API introduced in **LangChain 1.x** — the current standard, replacing the old `AgentExecutor` pattern.

> **Note:** `AgentExecutor` and `create_tool_calling_agent` were removed in LangChain 1.x. `create_agent` is now the unified entry point for all agent types.

**How it works:**

```
create_agent(model=llm, tools=tools)
        ↓
agent.invoke({"messages": [HumanMessage(...)]})
        ↓
result["messages"][-1].content  →  plain text answer
```

**Key characteristics:**
- Uses the **message-based interface** (`HumanMessage`) — consistent with the rest of the LangChain/LangGraph ecosystem.
- No prompt template needed — the agent handles tool descriptions internally.
- Output is a **plain string** extracted from the last message in the response.
- Agent is scoped **inside `main()`** — clean, no global state, easy to test.
- Uses `gpt-4o-mini` — cost-efficient and widely available.

**When to use:**
- Getting started with LangChain 1.x agents.
- Freeform conversational answers where plain text output is sufficient.
- Lightweight scripts that don't need structured/typed responses.

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
| Agent API | `create_agent` (LangChain 1.x) | `create_agent` with `response_format` |
| Prompt | Implicit (handled internally) | Implicit (handled internally) |
| Input format | `{"messages": [HumanMessage(...)]}` | `{"messages": HumanMessage(...)}` |
| Output type | Plain string (last message content) | Pydantic model (`answer` + `sources`) |
| Model | `gpt-4o-mini` | `gpt-5` |
| Agent scope | Inside function (clean) | Module-level global |
| Boilerplate | Minimal | Minimal + Pydantic schemas |
| Best for | Simple queries, learning | Production, APIs, structured output |

---

## Why Two Different Approaches?

Both files now use the **same `create_agent` API** (LangChain 1.x). The difference is purely about **output shape**:

| Reason | Explanation |
|---|---|
| **Output format** | `main.py` returns a plain string — simple and fast. `search-agent.py` returns a typed Pydantic object with `answer` + `sources`. |
| **Use case** | `main.py` is for quick queries where text output is enough. `search-agent.py` is for applications that need structured, validated, parseable data. |
| **Complexity** | `main.py` has zero schema overhead. `search-agent.py` requires defining Pydantic models but gives you type safety and source citations in return. |

### LangChain API Migration History

```
LangChain <1.x   →   create_tool_calling_agent + AgentExecutor  (removed)
LangChain 1.x    →   create_agent (unified API, LangGraph-backed)
```

---

## Recommendation

**Use `search-agent.py`'s pattern for production** — structured output with typed sources is far more useful when building real applications (no string parsing, type safety, includes citations).

**Use `main.py`'s pattern when plain text output is enough** — minimal setup, uses the current LangChain 1.x API, great for scripts and quick prototypes.

> **Note:** Two known improvements for `search-agent.py`:
> 1. Move the agent initialization inside `main()` to avoid global state.
> 2. Consider `gpt-4o` as a fallback if `gpt-5` is not available on your API plan.
