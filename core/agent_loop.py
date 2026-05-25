import json
from core.router import ask_kokai_core
from research.web import web_search
from core.audio_engine import render_standalone_audio
from core.video_engine import render_standalone_video

AVAILABLE_TOOLS = {
    "web_search": web_search,
    "render_audio": render_standalone_audio,
    "render_video": render_standalone_video
}

async def run_autonomous_kokai_loop(user_query: str, max_steps: int = 5) -> str:
    history = [
        f"[SYSTEM]: Available tools: {list(AVAILABLE_TOOLS.keys())}. "
        f"You must solve the user query step-by-step. If you need a tool, output exactly: "
        f"TOOL_CALL: {{\"name\": \"tool_name\", \"args\": {{\"arg_key\": \"value\"}}}}\n"
        f"If you have the final complete answer, output exactly: FINAL_ANSWER: [your response]"
    ]
    
    current_prompt = f"{user_query}"
    
    for step in range(max_steps):
        execution_context = "\n".join(history) + f"\n\n[USER]: {current_prompt}"
        ai_message = await ask_kokai_core(execution_context, strategy="logic_code")

        if "TOOL_CALL:" in ai_message:
            try:
                tool_json_str = ai_message.split("TOOL_CALL:")[1].strip()
                tool_data = json.loads(tool_json_str)
                tool_name = tool_data["name"]
                tool_args = tool_data["args"]

                if tool_name in AVAILABLE_TOOLS:
                    if tool_name == "web_search":
                        tool_result = await AVAILABLE_TOOLS[tool_name](**tool_args)
                    else:
                        tool_result = await AVAILABLE_TOOLS[tool_name](**tool_args) if asyncio.iscoroutinefunction(AVAILABLE_TOOLS[tool_name]) else AVAILABLE_TOOLS[tool_name](**tool_args)

                    history.append(f"[TOOL_RESULT from {tool_name}]: {tool_result}")
                else:
                    history.append(f"[SYSTEM_ERROR]: Tool '{tool_name}' does not exist.")
            except Exception as e:
                history.append(f"[SYSTEM_ERROR]: Failed to parse payload: {e}")
                
        elif "FINAL_ANSWER:" in ai_message:
            return ai_message.split("FINAL_ANSWER:")[1].strip()
        else:
            return ai_message

    return "[AGENT ALERT]: Iteration limit exceeded."
