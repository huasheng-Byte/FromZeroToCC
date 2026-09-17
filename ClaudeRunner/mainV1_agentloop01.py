from anthropic import Anthropic
from dotenv import load_dotenv
import os
import subprocess

load_dotenv(override=True)
client=Anthropic(base_url=os.getenv("ANTHROPIC_BASE_URL"))
MODEL=os.environ["MODEL_ID"]

SYSTEM=f"You are a coding agent at {os.getcwd()}.Use bash to solve tasks.Act,don't explain."

TOOLS=[{
        "name":"bash",
        "description":"Run a shell command",
        "input_schema":{
            "type":"object",
            "properties":{"command":{"type":"string"}},
            "required":["command"]
        }
}]


def run_bash(command:str) ->str:
    dangerous=["rm -rf /","sudo","shutdown","reboot",">/dev/"]
    if any(d in command for d in dangerous):
        return "Error:Dangerous command blocked"

    try:
        r=subprocess.run(command,shell=True,cwd=os.getcwd()
                         ,capture_output=True,text=True,errors="replace",
                        timeout=120)
        out=(r.stdout+r.stderr).strip()
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error:Timeout(120s)"
    except (FileNotFoundError,OSError) as e:
        return f"Error:{e}"


def agent_loop(messages:list):
    while True:
        # 把整个账本发给模型
        response=client.messages.create(
            model=MODEL,system=SYSTEM,messages=messages,
            tools=TOOLS,max_tokens=8000,
        )

        # 把模型的回复记进账本
        messages.append({"role":"assistant","content":response.content})

        tool_calls=[
            block for block in response.content if block.type=="tool_use"
        ]

        if not tool_calls:
            return

        results=[]
        for block in tool_calls:
            print(f"{block.input['command']}")
            output=run_bash(block.input["command"])
            print(output[:200])
            results.append({
                "type":"tool_result",
                "tool_use_id":block.id,
                "content":output,
            })

        messages.append({"role" : "user","content": results})


if __name__=="__main__":
    print("s01:Agent Loop")
    print("Enter a question,press Enter to send.Type q to quit.\n")

    history=[]

    while True:
        try:
            query=input("agent>>")
        except (EOFError,KeyboardInterrupt):
            break
        if query.strip().lower() in ("q","exit",""):
            break
        history.append({"role":"user","content":query})
        agent_loop(history)

        for block in history[-1]["content"]:
            if getattr(block,"type",None)=="text":
                print(block.text)
        print()