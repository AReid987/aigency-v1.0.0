import pytest
from ai_orchestrator import AIOrchestrator

@pytest.fixture
def orchestrator():
    return AIOrchestrator()

def test_end_to_end(orchestrator):
    # Test happy path
    response = orchestrator.process("Explain quantum computing")
    assert isinstance(response, dict)
    assert "content" in response

def test_error_handling(orchestrator):
    # Test fallback behavior
    with pytest.raises(Exception):
        orchestrator.process("")  # Empty prompt should trigger fallbacks

def test_optimization(orchestrator):
    # Verify OptiLLM tuning
    response1 = orchestrator.process("Short weather forecast")
    response2 = orchestrator.process("Short weather forecast") 
    assert response1["params"] == response2["params"]  # Consistency check