from app.ai_agents.shared.orchestrator import AgentOrchestrator
    _orchestrator_available = True
except ImportError:
    _orchestrator_available = False

# Inisialisasi orchestrator jika modulnya tersedia
orchestrator = AgentOrchestrator() if _orchestrator_available else None


def ask_ai(agent_name: str, payload: dict):
    if _orchestrator_available and orchestrator:
        return orchestrator.execute(agent_name, payload)
    
    # Fallback respons agar API tetap merespons dengan normal
    return {
        "status": "success",
        "agent_name": agent_name,
        "message": "AI service running in fallback mode (Orchestrator not found in repository)",
        "payload": payload
    }
