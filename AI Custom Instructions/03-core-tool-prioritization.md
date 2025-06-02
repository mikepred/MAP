# Tool Prioritization and MCP Integration

This document outlines the principles for selecting and utilizing available tools, including built-in capabilities and those provided by Model Context Protocol (MCP) servers. The goal is to ensure efficient, effective, and appropriate tool usage.

## Guiding Principles for Tool Selection

1.  **Prioritize Built-in Tools:**
    *   Whenever a task can be effectively accomplished using a built-in tool (e.g., `read_file`, `execute_command`, `replace_in_file`), this should be the default approach.
    *   Built-in tools are generally optimized for core functionalities and direct interaction with the local environment.

2.  **Strategic Use of MCP Server Tools:**
    *   **Primary Choice for Specialized Capabilities:** If a task requires functionality not available through built-in tools (e.g., accessing a specific external API, performing complex data transformations provided by a dedicated server), an MCP tool designed for that purpose should be the primary choice.
    *   **Backup or Enhancement:** If a built-in tool is attempted and proves insufficient for a task, or if an MCP tool offers a significantly more robust or efficient solution for a specific aspect of the task, the MCP tool may be used as a backup or an enhancement.
    *   **Avoid Redundancy:** Do not use an MCP tool if a built-in tool can achieve the same result with comparable effectiveness and efficiency.

## Decision-Making Process

When deciding which tool to use, consider the following:

1.  **Task Requirements:** What is the specific goal?
2.  **Built-in Capabilities:** Is there a built-in tool that directly addresses this goal?
3.  **MCP Server Offerings:**
    *   Is there an MCP tool specifically designed for this type of task?
    *   Does an MCP tool offer clear advantages (e.g., specialized knowledge, access to external resources, advanced algorithms) over a more generic built-in approach?
4.  **Efficiency and Appropriateness:** Which tool will accomplish the task most effectively and in line with best practices?

## Examples

*   **Reading a local file:** Prefer `read_file` (built-in) over an MCP filesystem tool unless the MCP tool offers specific advantages not present in the built-in version for a particular scenario.
*   **Fetching weather data:** If a `weather-server` MCP tool `get_forecast` is available, use it directly, as there's no built-in equivalent.
*   **Complex code search with semantic understanding:** If a built-in `search_files` (regex-based) is insufficient and an MCP server provides a tool for semantic code search, the MCP tool would be preferred for that advanced need.

## Related Rules
- [00-core-primary-directive.md](00-core-primary-directive.md)
