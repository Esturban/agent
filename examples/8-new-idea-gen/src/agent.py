# agent.py - Core agent logic for parsing and idea generation

import json
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from .models import AgentState, ParsedContent,  IdeaOutput, IdeaConcept

def parser_agent(state: AgentState, parser_llm, tools) -> dict:
    """Phase 1: Parse the free-for-dev list"""

    # Get the free-for-dev URL from the initial state or use default
    free_dev_url = "https://raw.githubusercontent.com/ripienaar/free-for-dev/refs/heads/master/README.md"

    # Parse the free-for-dev list
    parse_tool = tools[0]  # parse_free_dev_list tool
    parsed_result = parse_tool.invoke(free_dev_url)

    parsed_data = json.loads(parsed_result)
    if "error" in parsed_data:
        return {"error": parsed_data["error"]}

    parsed_content = ParsedContent(**parsed_data)

    return {
        "parsed_content": parsed_content
    }

def idea_generation_agent(state: AgentState, idea_llm, tools=None) -> dict:
    """Phase 2: Generate simple product ideas from free tools"""

    parsed_content = state.get("parsed_content")

    if not parsed_content:
        return {"error": "Missing parsed content"}

    # Get sample of actual tools for the prompt
    sample_tools = parsed_content.tools 
    tools_sample = "\n".join([f"- {tool.name} ({tool.category})" for tool in sample_tools])

    categories_text = ", ".join(parsed_content.categories) 

    system_prompt = f"""You have access to {len(parsed_content.tools)} free developer tools across these categories: {categories_text}.

    Here are some examples of the actual tools available:
    {tools_sample}

    Generate 5-10 simple product ideas that combine 2-3 of these ACTUAL free tools to solve real developer problems.
    Use the REAL tool names from the list above in your target_tools array.
    Keep it practical - these should be things a solo developer could build in a weekend."""

    idea_prompt = f"""
    Based on {len(parsed_content.tools)} ACTUAL free tools from the list above, generate simple product ideas.

    You MUST use the actual tool names from the parsed list in your target_tools arrays.
    For example, use "Google Colab", "CloudFront", "DynamoDB", etc. - not generic names.

    Available tools summary:
    {parsed_content.summary}

    Generate practical ideas that:
    - Use 2-3 ACTUAL free tools from the parsed list
    - Solve actual developer pain points
    - Can be built quickly (weekend project level)
    - Have monetization potential

    Return a JSON array of idea objects with:
    - title: Short, catchy name
    - description: What problem it solves and how
    - target_tools: 2-3 ACTUAL tool names from the parsed list
    - value_proposition: Who it helps and why it's valuable to them
    - effort_level: "low", "medium", or "high"
    - reasoning: a single 1-2 sentence plain-text explanation of WHY these specific tools are useful together for implementing this idea. Keep it concise and human-readable, but useful. 
    - implementation_complexity: "simple", "moderate", or "complex"
    """

    messages = [
        SystemMessage(system_prompt),
        HumanMessage(idea_prompt)
    ]

    response = idea_llm.invoke(messages)
    raw_response = getattr(response, "content", str(response)).strip()

    # Debug: print what we got from the LLM
    print(f"🤖 LLM Response length: {len(raw_response)} chars")

    # Try multiple strategies to extract JSON from the raw LLM response.
    # 1) Try to parse the whole response as JSON
    # 2) Try to find a ```json``` fenced block
    # 3) Try to find the first top-level JSON array or object by braces
    import re

    def try_load_json(text: str):
        try:
            return json.loads(text)
        except Exception:
            return None

    ideas_data = try_load_json(raw_response)

    if ideas_data is None:
        # Look for fenced ```json``` blocks first
        json_block_match = re.search(r'```json\s*(\[.*?\]|\{.*?\})\s*```', raw_response, re.DOTALL)
        if json_block_match:
            json_content = json_block_match.group(1)
            print(f"📝 Found JSON code fence: {len(json_content)} chars")
            ideas_data = try_load_json(json_content)

    if ideas_data is None:
        # Fallback: try to locate the first JSON array/object by searching for outermost brackets
        brace_match = re.search(r'(?s)(\[.*\]|\{.*\})', raw_response)
        if brace_match:
            json_guess = brace_match.group(1)
            print(f"🔎 Found JSON-like substring: {len(json_guess)} chars — attempting to parse")
            ideas_data = try_load_json(json_guess)

    if ideas_data is None:
        print("❌ Failed to extract/parse JSON from LLM response")
        print(f"🤖 LLM Response: {raw_response}")
        return {"error": "No valid JSON found in LLM response"}

    ideas = []
    for idea_data in ideas_data:
        if isinstance(idea_data, dict):
            idea_concept = IdeaConcept(**idea_data)

            # Simple confidence calculation
            confidence = 0.8  # Basic confidence for now

            # Extract LLM-provided reasoning if present, ensure it's a short string (<=2 sentences)
            raw_reasoning = ''
            try:
                raw_reasoning = idea_data.get('reasoning', '') if isinstance(idea_data, dict) else ''
            except Exception:
                raw_reasoning = ''

            reasoning = str(raw_reasoning or '').strip()
            # enforce <= 2 sentences
            import re
            sentences = [s.strip() for s in re.split(r'[.!?]+', reasoning) if s.strip()]
            if len(sentences) > 2:
                reasoning = '. '.join(sentences[:2]) + '.'
            # fallback if empty
            if not reasoning:
                reasoning = f"Simple idea using {len(idea_concept.target_tools)} free tools to solve developer problems."

            next_steps = [
                "Pick the tools and understand their APIs",
                "Build a basic prototype",
                "Test if it actually helps developers",
                "Figure out how to monetize it"
            ]

            ideas.append(IdeaOutput(
                idea_concept=idea_concept,
                confidence=confidence,
                reasoning=reasoning,
                next_steps=next_steps
            ))

    return {
        "parsed_content": parsed_content,
        "ideas": ideas
    }

