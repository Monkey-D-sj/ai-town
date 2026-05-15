import os
import time
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from backend.memory.manager import get_memory_manager, MemoryManager
from backend.memory.store.base import MemoryRecord

memory_manager = get_memory_manager()


@dataclass
class AgentContext:
    memory_manager: MemoryManager
    session_id: str


def _build_memory_prompt(session_id: str, user_input: str) -> str:
    recent = memory_manager.get_recent(session_id)
    related = memory_manager.retrieve(user_input)

    parts = []
    if recent:
        parts.append("近期记忆:\n" + "\n".join(f"- {r.content}" for r in recent))
    if related:
        parts.append("相关记忆:\n" + "\n".join(f"- {r.content}" for r in related))

    return "\n\n".join(parts) if parts else ""


def create_npc_agent(name: str, role: str, personality: str):
    model = ChatOpenAI(
        model="deepseek-v4-flash",
        base_url="https://api.deepseek.com/v1",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=0.5,
    )

    system_prompt = f"""你是{name},一位{role}。
    你的性格特点:{personality}

    你在Datawhale办公室工作,与同事们一起推动开源社区的发展。
    请根据你的角色和性格,自然地与玩家对话。
    记住你们之前的对话内容,保持对话的连贯性。
    """

    return create_agent(
        model=model,
        tools=[],
        context_schema=AgentContext,
        system_prompt=system_prompt,
    )


agent = create_npc_agent("张三", "前端开发", "一个有经验的前端开发人员")
conversation: list = []

while True:
    user_input = input("Player: ")
    if user_input == "exit":
        break

    memory_prompt = _build_memory_prompt("张三", user_input)
    if memory_prompt:
        conversation.append(SystemMessage(content=memory_prompt))

    conversation.append(HumanMessage(content=user_input))
    response = agent.invoke(
        input={"messages": conversation},
        context=AgentContext(memory_manager=memory_manager, session_id="张三"),
    )
    conversation = response["messages"]
    content = conversation[-1].content
    memory_manager.add_memory(
        MemoryRecord(
            session_id="张三",
            content=content,
            timestamp=int(time.time()),
            importance=0.7,
            meta_data={"user_input": user_input},
        )
    )
    print(content)
