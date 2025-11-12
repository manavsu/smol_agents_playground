#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "fastmcp",
#     "smolagents[litellm,mcp,toolkit,transformers]",
# ]
# ///
"""FastMCP server that wraps a Smolagents CodeAgent for Codex MCP clients."""

from fastmcp import FastMCP
from smolagents import CodeAgent, LiteLLMModel, WebSearchTool
import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)


def build_agent(allowed_python_imports) -> CodeAgent:
    model = LiteLLMModel(
        model_id="gpt-5-mini",
        api_base=config["base_url"],
        api_key=config["api_key"],
    )

    return CodeAgent(
        model=model,
        tools=[WebSearchTool()],
        additional_authorized_imports=["requests", "bs4"] + allowed_python_imports,
        stream_outputs=True,
    )


mcp = FastMCP("smol_agent")


@mcp.tool(
    name="run_smol_agent",
    description="smol_agent is an agent that thinks in code, ideal for data analysis, automations, caclucations and doing task in a discrete way.",
)
def run_smol_agent(prompt: str, allowed_python_imports: list[str]) -> str:
    agent = build_agent(allowed_python_imports)
    return str(agent.run(prompt))


if __name__ == "__main__":
    mcp.run(transport="stdio")
