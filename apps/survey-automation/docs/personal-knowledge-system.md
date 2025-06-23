# Personal Knowledge System for Survey Agent

## 🎯 Objective
Enable the agent to answer surveys authentically as YOU by:
1. **Personal Data Storage** - Demographics, preferences, history
2. **Knowledge Graph** - Semantic relationships and context
3. **Fine-tuning Data** - Examples of how you answer questions
4. **Contextual Reasoning** - Understanding question intent and appropriate responses

## 🗄️ Architecture: PocketBase + Kuzu

### **PocketBase** (Personal Data Store)
- Lightweight, self-hosted database
- Built-in admin UI for data management
- Real-time subscriptions
- File storage for documents/images
- Perfect for personal profile data

### **Kuzu** (Knowledge Graph)
- High-performance graph database
- Semantic relationships
- Contextual reasoning
- Query optimization
- Ideal for understanding question context

## 📊 Data Schema Design

### Personal Profile (PocketBase)
```javascript
// Demographics Collection
{
  id: "demographics",
  age: 30,
  location: "New York, NY",
  occupation: "Software Engineer",
  income_range: "$75k-$100k",
  education: "Bachelor's Degree",
  marital_status: "Single",
  household_size: 1
}

// Preferences Collection
{
  id: "preferences",
  favorite_brands: ["Apple", "Nike", "Starbucks"],
  shopping_frequency: "Weekly",
  preferred_channels: ["Online", "Mobile App"],
  interests: ["Technology", "Fitness", "Travel"],
  values: ["Innovation", "Quality", "Sustainability"]
}

// Survey History Collection
{
  id: "survey_responses",
  question: "How often do you shop online?",
  answer: "2-3 times per week",
  context: "E-commerce survey",
  reasoning: "I prefer online for convenience and selection",
  timestamp: "2024-01-15"
}
```

### Knowledge Graph (Kuzu)
```cypher
// Nodes
CREATE (p:Person {name: "Antonio Reid", age: 30})
CREATE (l:Location {name: "New York", type: "City"})
CREATE (o:Occupation {title: "Software Engineer", industry: "Technology"})
CREATE (i:Interest {name: "Technology", category: "Professional"})

// Relationships
CREATE (p)-[:LIVES_IN]->(l)
CREATE (p)-[:WORKS_AS]->(o)
CREATE (p)-[:INTERESTED_IN]->(i)
CREATE (i)-[:INFLUENCES]->(shopping_behavior)
```

## 🛠️ Implementation

### 1. PocketBase Setup
```bash
# Install PocketBase
cd apps/survey-automation
wget https://github.com/pocketbase/pocketbase/releases/download/v0.20.0/pocketbase_0.20.0_darwin_amd64.zip
unzip pocketbase_0.20.0_darwin_amd64.zip
chmod +x pocketbase

# Start PocketBase
./pocketbase serve --http=127.0.0.1:8090
```

### 2. Kuzu Integration
```bash
# Install Kuzu Python client
pdm add kuzu
```

### 3. Personal Knowledge Manager
```python
# apps/survey-automation/app/personal_knowledge.py
import kuzu
import requests
from typing import Dict, List, Any, Optional

class PersonalKnowledgeManager:
    def __init__(self):
        self.pocketbase_url = "http://127.0.0.1:8090"
        self.kuzu_db = kuzu.Database("./knowledge_graph")
        self.conn = kuzu.Connection(self.kuzu_db)
        
    async def get_demographic_answer(self, question: str) -> str:
        """Get demographic answer based on personal profile"""
        # Query PocketBase for demographic data
        response = requests.get(f"{self.pocketbase_url}/api/collections/demographics/records")
        profile = response.json()['items'][0]
        
        # Map question to profile field
        question_mapping = {
            "age": profile['age'],
            "location": profile['location'],
            "occupation": profile['occupation'],
            "income": profile['income_range']
        }
        
        # Use semantic matching for question understanding
        return self._match_question_to_answer(question, question_mapping)
    
    async def get_preference_answer(self, question: str, options: List[str]) -> str:
        """Get preference-based answer using knowledge graph"""
        # Query knowledge graph for contextual understanding
        query = f"""
        MATCH (p:Person)-[:INTERESTED_IN]->(i:Interest)
        WHERE i.category CONTAINS '{self._extract_category(question)}'
        RETURN i.name, i.influence_score
        """
        
        result = self.conn.execute(query)
        interests = [record for record in result]
        
        # Select best matching option based on interests
        return self._select_best_option(options, interests)
    
    async def get_contextual_answer(self, question: str, context: str) -> str:
        """Generate contextual answer using historical responses"""
        # Find similar questions from history
        similar_responses = await self._find_similar_responses(question, context)
        
        if similar_responses:
            # Use pattern from similar responses
            return self._generate_consistent_answer(question, similar_responses)
        else:
            # Generate new answer based on profile
            return await self._generate_profile_based_answer(question, context)
    
    async def learn_from_response(self, question: str, answer: str, context: str):
        """Learn from new responses to improve future answers"""
        # Store in PocketBase
        response_data = {
            "question": question,
            "answer": answer,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        
        requests.post(
            f"{self.pocketbase_url}/api/collections/survey_responses/records",
            json=response_data
        )
        
        # Update knowledge graph relationships
        await self._update_knowledge_graph(question, answer, context)
```

## 🎯 Survey Answer Generation

### Question Type Classification
```python
class SurveyAnswerGenerator:
    def __init__(self, knowledge_manager: PersonalKnowledgeManager):
        self.km = knowledge_manager
        
    async def answer_question(self, question: str, question_type: str, options: List[str] = None) -> str:
        """Generate authentic answer based on question type"""
        
        if question_type == "demographic":
            return await self.km.get_demographic_answer(question)
            
        elif question_type == "preference":
            return await self.km.get_preference_answer(question, options)
            
        elif question_type == "opinion":
            return await self.km.get_contextual_answer(question, "opinion")
            
        elif question_type == "behavioral":
            return await self.km.get_contextual_answer(question, "behavior")
            
        elif question_type == "open_ended":
            return await self._generate_open_ended_response(question)
    
    async def _generate_open_ended_response(self, question: str) -> str:
        """Generate authentic open-ended responses"""
        # Get personality traits and communication style
        style = await self.km.get_communication_style()
        context = await self.km.get_relevant_context(question)
        
        # Generate response that matches your voice and perspective
        return self._compose_authentic_response(question, style, context)
```

## 🔧 Integration with Survey Agent

### Enhanced Agent with Personal Knowledge
```python
# Update apps/survey-automation/app/agent.py
from .personal_knowledge import PersonalKnowledgeManager, SurveyAnswerGenerator

class EnhancedSurveyAgent:
    def __init__(self):
        self.knowledge_manager = PersonalKnowledgeManager()
        self.answer_generator = SurveyAnswerGenerator(self.knowledge_manager)
        
    async def fill_survey_authentically(self, survey_questions: List[Dict]) -> Dict:
        """Fill survey with authentic personal responses"""
        responses = {}
        
        for question in survey_questions:
            # Classify question type
            q_type = self._classify_question(question['text'])
            
            # Generate authentic answer
            answer = await self.answer_generator.answer_question(
                question['text'], 
                q_type, 
                question.get('options')
            )
            
            responses[question['id']] = answer
            
            # Learn from this interaction
            await self.knowledge_manager.learn_from_response(
                question['text'], 
                answer, 
                survey_questions.get('context', 'survey')
            )
        
        return responses
```

## 📝 Data Seeding Interface

### Admin Interface for Personal Data
```python
# apps/survey-automation/app/admin_interface.py
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

@app.get("/admin/profile")
async def profile_form(request: Request):
    """Personal profile management interface"""
    return templates.TemplateResponse("profile_form.html", {"request": request})

@app.post("/admin/profile")
async def update_profile(
    age: int = Form(...),
    location: str = Form(...),
    occupation: str = Form(...),
    interests: str = Form(...)
):
    """Update personal profile data"""
    # Update PocketBase
    # Update knowledge graph
    return {"status": "updated"}

@app.get("/admin/training")
async def training_interface(request: Request):
    """Interface for training the agent with example responses"""
    return templates.TemplateResponse("training_form.html", {"request": request})
```

## 🚀 Implementation Priority

### Phase 1: Basic Personal Data (This Week)
1. Set up PocketBase with personal profile
2. Create basic demographic answer mapping
3. Implement simple preference matching

### Phase 2: Knowledge Graph (Next Week)
1. Set up Kuzu database
2. Create semantic relationships
3. Implement contextual reasoning

### Phase 3: Learning System (Following Week)
1. Response pattern learning
2. Consistency checking
3. Continuous improvement

This system will enable your agent to authentically represent YOU in surveys, maintaining consistency while adapting to different contexts and question types.
