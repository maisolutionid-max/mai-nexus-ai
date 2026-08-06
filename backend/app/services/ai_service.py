from app.ai_agents.orchestrator import AIOrchestrator

orchestrator = AIOrchestrator()

async def ask_ai(payload: dict):
    return await orchestrator.run(payload)
