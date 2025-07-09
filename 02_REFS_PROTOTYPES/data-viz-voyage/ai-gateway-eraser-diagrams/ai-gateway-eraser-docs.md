# XPRT

# LLM Gateway Architecture Guide
## 1. **Portkey**
### **Strengths**:
- Unified API for multiple LLMs, built-in observability, and cost tracking.
### **Use Case**:
- Best for managing multiple LLM providers (OpenAI, Anthropic, etc.) with a single interface.
- **Integration**: Can act as the primary gateway for all LLM calls.
## 2. **Not Diamond**
### **Strengths**:
- Focused on routing requests to the most cost-effective or performant model.
### **Use Case**:
- Ideal for optimizing cost/performance trade-offs dynamically.
### **Integration**:
- Can sit on top of Portkey for advanced routing logic.
## 3. **RouteLLM**
### **Strengths**:
- Lightweight, open-source routing for LLMs.
### **Use Case**:
- Good for custom routing logic if you want full control.
### **Integration**:
- Can replace Not Diamond if you prefer open-source.
## 4. **LiteLLM**
### **Strengths**:
- Unified API for 100+ LLMs, including OpenAI, Hugging Face, and custom models.
### **Use Case**:
- Best for flexibility and supporting a wide range of models.
### **Integration**:
- Can replace Portkey if you need broader model support.
## 5. **Kong**
### **Strengths**:
- Enterprise-grade API gateway with advanced traffic management.
### **Use Case**:
- Best for large-scale deployments needing security, rate limiting, and observability.
### **Integration**:
- Can act as the outer layer for managing all API traffic (including LLM calls).
## 6. **OptiLLM**
### **Strengths**:
- Focused on optimizing LLM performance and cost.
### **Use Case**:
- Best for fine-tuning model selection and parameters.
### **Integration**:
- Can complement Not Diamond or RouteLLM for optimization.
---

## **How They Work Together**
### **Proposed Architecture**
1. **Kong** (Outer Layer):
    - Manages API traffic, security, and rate limiting.
    - Routes requests to the appropriate internal services.
2. **Portkey/LiteLLM** (Primary Gateway):
    - Unified interface for all LLM calls.
    - Handles provider-specific API keys and configurations.
3. **Not Diamond/RouteLLM** (Routing Layer):
    - Dynamically routes requests to the best model based on cost/performance.
    - Can be integrated with Portkey/LiteLLM.
4. **OptiLLM** (Optimization Layer):
    - Fine-tunes model selection and parameters for specific tasks.
    - Works alongside Not Diamond/RouteLLM.
---

## **Implementation Recommendations**
### **Step 1: Start with Portkey or LiteLLM**
- Use **Portkey** if you want built-in observability and cost tracking.
- Use **LiteLLM** if you need support for a wider range of models.
### **Step 2: Add Not Diamond or RouteLLM**
- Use **Not Diamond** for pre-built cost/performance optimization.
- Use **RouteLLM** if you want full control over routing logic.
### **Step 3: Integrate OptiLLM**
- Use OptiLLM for fine-tuning model selection and parameters.
### **Step 4: Deploy with Kong**
- Use Kong as the outer layer for API management, security, and observability.
---

## **Example Implementation**
### **Portkey + Not Diamond + Kong**
1. **Portkey**: Unified API for LLM calls.
2. **Not Diamond**: Routes requests to the best model based on cost/performance.
3. **Kong**: Manages API traffic and security.
### **LiteLLM + RouteLLM + OptiLLM**
1. **LiteLLM**: Unified API for 100+ models.
2. **RouteLLM**: Custom routing logic for model selection.
3. **OptiLLM**: Fine-tunes model parameters.
```python
from typing import Literal
import openrouter
import groq
import anthropic

ModelProvider = Literal["openrouter", "groq", "anthropic", "ollama"]

class AIModelGateway:
    def __init__(self, provider: ModelProvider = "openrouter"):
        self.provider = provider
        self.clients = {
            "openrouter": openrouter.Client,
            "groq": groq.Client,
            "anthropic": anthropic.Client,
            "ollama": lambda: NotImplementedError("Ollama not implemented")
        }
        
    def analyze(self, content: str, model: str = None, **kwargs):
        """Unified analysis interface"""
        if self.provider == "openrouter":
            return self._analyze_openrouter(content, model, **kwargs)
        elif self.provider == "groq":
            return self._analyze_groq(content, model, **kwargs)
        # ... other providers
        
    def _analyze_openrouter(self, content: str, model: str = "gemini-pro", **kwargs):
        return openrouter.complete(
            model=model,
            prompt=f"Analyze this content: {content}",
            **kwargs
        )
        
    def _analyze_groq(self, content: str, model: str = "mixtral-8x7b", **kwargs):
        return groq.complete(
            model=model,
            prompt=f"Analyze: {content}",
            **kwargs
        )
        
    def switch_provider(self, new_provider: ModelProvider):
        self.provider = n
```
## **1. Using Portkey and LiteLLM Together**
### **Approach**
- **Portkey** as the primary gateway for observability, cost tracking, and unified API management.
- **LiteLLM** as the underlying library for broader model support (e.g., Hugging Face, custom models).
### **Implementation**
1. **Portkey** handles API requests and forwards them to **LiteLLM**.
2. **LiteLLM** processes the request using the appropriate model.
3. **Portkey** tracks the response and provides observability.
### **Example**
```python
from portkey import Portkey
from litellm import completion

portkey = Portkey(api_key="your_portkey_key")

def unified_llm_call(prompt, model="gpt-4"):
    # Portkey tracks the request
    with portkey.trace():
        # LiteLLM processes the request
        response = completion(model=model, messages=[{"role": "user", "content": prompt}])
    return response
```
---

## **2. Using RouteLLM and Not Diamond Together**
### **Approach**
- **Not Diamond** for high-level cost/performance optimization.
- **RouteLLM** for custom routing logic (e.g., fallback models, retries).
### **Implementation**
1. **Not Diamond** selects the best model based on cost/performance.
2. **RouteLLM** handles the actual routing and fallback logic.
### **Example**
```python
from notdiamond import NotDiamond
from routellm import RouteLLM

not_diamond = NotDiamond(api_key="your_notdiamond_key")
route_llm = RouteLLM()

def optimized_llm_call(prompt):
    # Not Diamond selects the best model
    model = not_diamond.select_model(prompt)
    
    # RouteLLM handles the routing
    response = route_llm.route(model=model, prompt=prompt)
    return response
```
---

## **3. Integrating OptiLLM**
### **Example**
```python
from optillm import OptiLLM
optillm = OptiLLM()
def fine_tuned_llm_call(prompt):
    # OptiLLM fine-tunes the model selection
    model, params = optillm.optimize(prompt)
    
    # Use Portkey/LiteLLM or RouteLLM/Not Diamond to make the call
    response = unified_llm_call(prompt, model=model)
    return response
```
---

## **Kong vs Kuma**
Both **Kong** and **Kuma** are excellent API management tools, but they serve different use cases:

### **Kong**
- **Best For**: Enterprise-grade API management.
- **Features**: Advanced traffic management, security, observability.
- **Use Case**: Large-scale deployments needing robust API management.
### **Kuma**
- **Best For**: Service mesh and microservices.
- **Features**: Traffic routing, security, and observability for microservices.
- **Use Case**: Kubernetes-based microservices architectures.
### **Recommendation**
- Use **Kong** for API management (e.g., LLM gateway).
- Use **Kuma** if you're building a microservices architecture.
---

## **Proposed Implementation Plan**
### **Phase 1: Portkey + LiteLLM**
1. Set up **Portkey** as the primary gateway.
2. Integrate **LiteLLM** for broader model support.
### **Phase 2: RouteLLM + Not Diamond**
1. Add **Not Diamond** for cost/performance optimization.
2. Use **RouteLLM** for custom routing logic.
### **Phase 3: OptiLLM**
1. Integrate **OptiLLM** for fine-tuning model selection.
### **Phase 4: Kong**
1. Deploy the system with **Kong** for API management.


