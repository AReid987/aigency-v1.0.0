graph TD
    subgraph Client-Facing Layer
        U[User/Application] --> A[Kong API Gateway]
    end

    subgraph Core Gateway Services
        A --> B[Unified LLM API Service<br>(Portkey/LiteLLM)]
        B --> C[Intelligent Router Service<br>(Not Diamond/RouteLLM)]
        C --> D[Optimization Service<br>(OptiLLM)]
    end

    subgraph LLM Providers
        D --> E[External LLM Providers<br>(OpenAI, Anthropic, Groq, etc.)]
        E --> D
    end

    subgraph Management & Observability
        B --- F[Observability Services<br>(Logging, Metrics, Tracing)]
        C --- F
        D --- F
        F --> G[Analytics & Config Dashboard<br>(Next.js UI)]
    end

    subgraph Supporting Functions
        H[Prompt Management]
        I[Virtual Key Management]
    end

    G -- Configures --> H
    G -- Configures --> I
    H -- Applies to --> B
    I -- Applies to --> C

    style A fill:#D9E8F5,stroke:#3470AD,stroke-width:2px
    style B fill:#D9E8F5,stroke:#3470AD,stroke-width:2px
    style C fill:#D9E8F5,stroke:#3470AD,stroke-width:2px
    style D fill:#D9E8F5,stroke:#3470AD,stroke-width:2px
    style U fill:#F5E8D9,stroke:#AD7034,stroke-width:2px
    style E fill:#F5E8D9,stroke:#AD7034,stroke-width:2px
    style F fill:#E0F2F7,stroke:#2F8F9F,stroke-width:2px
    style G fill:#E0F2F7,stroke:#2F8F9F,stroke-width:2px
    style H fill:#E0F2F7,stroke:#2F8F9F,stroke-width:2px
    style I fill:#E0F2F7,stroke:#2F8F9F,stroke-width:2px
    style J fill:#E0F2F7,stroke:#2F8F9F,stroke-width:2px
    style K fill:#E0F2F7,stroke:#2F8F9F,stroke-width:2px