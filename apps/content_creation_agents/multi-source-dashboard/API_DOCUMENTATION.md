# Multi-Source Dashboard API Documentation

## Overview

The Multi-Source Dashboard API is a RESTful service built with FastAPI that provides content aggregation, processing, and publishing capabilities. This documentation covers all available endpoints, authentication, rate limiting, and integration examples.

## Base URL

- **Production**: `https://yourdomain.com/api/v1`
- **Development**: `http://localhost:8000/api/v1`
- **Interactive Docs**: `https://yourdomain.com/docs`
- **OpenAPI Schema**: `https://yourdomain.com/openapi.json`

## Authentication

### JWT Bearer Token Authentication

The API uses JWT (JSON Web Token) bearer tokens for authentication.

```bash
# Get access token
curl -X POST "https://yourdomain.com/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your_email@example.com&password=your_password"

# Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### Using the Token

Include the token in the Authorization header:

```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  "https://yourdomain.com/api/v1/users/me"
```

## Rate Limiting

- **General API**: 100 requests per minute per IP
- **Authentication endpoints**: 10 requests per minute per IP
- **Data collection endpoints**: 50 requests per minute per authenticated user

Rate limit information is included in response headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## API Endpoints

### Authentication

#### POST /auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "secure_password",
  "full_name": "John Doe"
}
```

**Response (201):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-01T12:00:00Z"
}
```

#### POST /auth/login
Authenticate user and receive access token.

**Request Body (form-data):**
```
username: user@example.com
password: secure_password
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### User Management

#### GET /users/me
Get current user profile.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-01T12:00:00Z",
  "last_login": "2024-01-01T12:00:00Z"
}
```

#### PUT /users/me
Update current user profile.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "full_name": "John Smith",
  "bio": "Content creator and tech enthusiast"
}
```

### Data Sources

#### GET /sources/
List available data sources.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "hackernews",
    "display_name": "Hacker News",
    "description": "Technology news and discussions",
    "is_active": true,
    "requires_auth": false,
    "rate_limit": {
      "requests_per_minute": 60,
      "requests_per_hour": 3600
    },
    "supported_content_types": ["story", "comment"],
    "configuration_schema": {
      "story_type": {
        "type": "string",
        "enum": ["topstories", "newstories", "beststories"],
        "default": "topstories"
      },
      "limit": {
        "type": "integer",
        "minimum": 1,
        "maximum": 100,
        "default": 30
      }
    }
  }
]
```

#### GET /sources/{source_id}
Get specific data source details.

**Path Parameters:**
- `source_id` (integer): Source identifier

**Response (200):**
```json
{
  "id": 1,
  "name": "hackernews",
  "display_name": "Hacker News",
  "description": "Technology news and discussions",
  "is_active": true,
  "requires_auth": false,
  "configuration_schema": {...},
  "usage_stats": {
    "requests_today": 150,
    "content_collected_today": 45,
    "average_response_time": 0.85
  }
}
```

#### POST /sources/{source_id}/test
Test data source configuration.

**Path Parameters:**
- `source_id` (integer): Source identifier

**Request Body:**
```json
{
  "configuration": {
    "story_type": "topstories",
    "limit": 10,
    "min_score": 50
  }
}
```

**Response (200):**
```json
{
  "status": "success",
  "test_results": {
    "connection_time": 0.45,
    "sample_content_count": 10,
    "configuration_valid": true
  },
  "sample_content": [
    {
      "title": "Sample Story Title",
      "url": "https://example.com/story",
      "score": 150,
      "comments_count": 25
    }
  ]
}
```

### Content Collection Runs

#### GET /runs/
List user's content collection runs.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `status` (optional): Filter by status (`draft`, `active`, `paused`, `completed`, `failed`)
- `limit` (optional): Number of results (default: 20)
- `offset` (optional): Pagination offset (default: 0)

**Response (200):**
```json
{
  "items": [
    {
      "id": 1,
      "name": "Daily Tech News",
      "description": "Automated collection of technology news",
      "status": "active",
      "frequency": "daily",
      "created_at": "2024-01-01T12:00:00Z",
      "last_run": "2024-01-02T12:00:00Z",
      "next_run": "2024-01-03T12:00:00Z",
      "filters": {
        "keywords": ["python", "javascript", "ai"],
        "min_score": 50,
        "max_age_hours": 24
      },
      "stats": {
        "total_content_collected": 156,
        "content_published": 23,
        "average_score": 78.5
      }
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

#### POST /runs/
Create a new content collection run.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "name": "Tech News Collection",
  "description": "Daily collection of programming and tech content",
  "frequency": "daily",
  "sources": [
    {
      "source_id": 1,
      "configuration": {
        "story_type": "topstories",
        "limit": 50
      }
    }
  ],
  "filters": {
    "keywords": ["python", "javascript", "react"],
    "exclude_keywords": ["spam", "clickbait"],
    "min_score": 25,
    "max_age_hours": 24,
    "content_types": ["story"]
  },
  "demographics_config": {
    "target_audience": "developers",
    "experience_level": "intermediate",
    "interests": ["web_development", "machine_learning"]
  },
  "publishing_config": {
    "auto_publish": false,
    "max_posts_per_day": 5,
    "review_required": true,
    "platforms": []
  }
}
```

**Response (201):**
```json
{
  "id": 2,
  "name": "Tech News Collection",
  "description": "Daily collection of programming and tech content",
  "status": "draft",
  "frequency": "daily",
  "created_at": "2024-01-01T12:00:00Z",
  "user_id": 1
}
```

#### GET /runs/{run_id}
Get specific run details.

**Path Parameters:**
- `run_id` (integer): Run identifier

**Response (200):**
```json
{
  "id": 1,
  "name": "Daily Tech News",
  "description": "Automated collection of technology news",
  "status": "active",
  "frequency": "daily",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-02T08:30:00Z",
  "last_run": "2024-01-02T12:00:00Z",
  "next_run": "2024-01-03T12:00:00Z",
  "sources": [...],
  "filters": {...},
  "demographics_config": {...},
  "publishing_config": {...},
  "execution_history": [
    {
      "started_at": "2024-01-02T12:00:00Z",
      "completed_at": "2024-01-02T12:05:30Z",
      "status": "completed",
      "content_collected": 15,
      "errors": []
    }
  ]
}
```

#### PUT /runs/{run_id}
Update run configuration or status.

**Path Parameters:**
- `run_id` (integer): Run identifier

**Request Body:**
```json
{
  "status": "active",
  "filters": {
    "keywords": ["python", "javascript", "ai", "blockchain"],
    "min_score": 30
  }
}
```

#### DELETE /runs/{run_id}
Delete a content collection run.

**Path Parameters:**
- `run_id` (integer): Run identifier

**Response (204):** No content

#### POST /runs/{run_id}/start
Manually start a run execution.

**Path Parameters:**
- `run_id` (integer): Run identifier

**Response (200):**
```json
{
  "message": "Run started successfully",
  "execution_id": "exec_12345",
  "estimated_completion": "2024-01-01T12:05:00Z"
}
```

#### POST /runs/{run_id}/pause
Pause an active run.

**Path Parameters:**
- `run_id` (integer): Run identifier

**Response (200):**
```json
{
  "message": "Run paused successfully",
  "status": "paused"
}
```

### Content Management

#### GET /content/
List collected content items.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `status` (optional): Filter by status (`pending_review`, `approved`, `rejected`, `published`)
- `source` (optional): Filter by source name
- `run_id` (optional): Filter by run ID
- `search` (optional): Search in title and content
- `limit` (optional): Number of results (default: 20)
- `offset` (optional): Pagination offset (default: 0)

**Response (200):**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Revolutionary AI Breakthrough in Natural Language Processing",
      "content": "Researchers have developed a new approach...",
      "url": "https://example.com/ai-breakthrough",
      "author": "Dr. Jane Smith",
      "source": "hackernews",
      "score": 245,
      "comments_count": 67,
      "content_type": "story",
      "status": "pending_review",
      "sentiment": "positive",
      "tags": ["ai", "nlp", "research"],
      "collected_at": "2024-01-01T12:00:00Z",
      "published_at": null,
      "run_id": 1,
      "metadata": {
        "reading_time": 5,
        "word_count": 850,
        "external_links": 3
      }
    }
  ],
  "total": 156,
  "limit": 20,
  "offset": 0,
  "filters_applied": {
    "status": "pending_review"
  }
}
```

#### GET /content/{content_id}
Get specific content item details.

**Path Parameters:**
- `content_id` (integer): Content identifier

**Response (200):**
```json
{
  "id": 1,
  "title": "Revolutionary AI Breakthrough in Natural Language Processing",
  "content": "Full content text here...",
  "url": "https://example.com/ai-breakthrough",
  "author": "Dr. Jane Smith",
  "source": "hackernews",
  "score": 245,
  "comments_count": 67,
  "content_type": "story",
  "status": "pending_review",
  "sentiment": "positive",
  "tags": ["ai", "nlp", "research"],
  "collected_at": "2024-01-01T12:00:00Z",
  "run_id": 1,
  "related_content": [
    {
      "id": 2,
      "title": "Related Article Title",
      "similarity_score": 0.85
    }
  ],
  "processing_history": [
    {
      "stage": "collection",
      "completed_at": "2024-01-01T12:00:30Z",
      "status": "success"
    },
    {
      "stage": "sentiment_analysis",
      "completed_at": "2024-01-01T12:01:15Z",
      "status": "success",
      "result": "positive"
    }
  ]
}
```

#### PUT /content/{content_id}/approve
Approve content for publishing.

**Path Parameters:**
- `content_id` (integer): Content identifier

**Request Body (optional):**
```json
{
  "notes": "Great content, approved for publishing",
  "tags": ["featured", "trending"]
}
```

**Response (200):**
```json
{
  "message": "Content approved successfully",
  "status": "approved",
  "approved_at": "2024-01-01T12:30:00Z"
}
```

#### PUT /content/{content_id}/reject
Reject content.

**Path Parameters:**
- `content_id` (integer): Content identifier

**Request Body:**
```json
{
  "reason": "duplicate_content",
  "notes": "Similar content was already published"
}
```

**Response (200):**
```json
{
  "message": "Content rejected",
  "status": "rejected",
  "rejected_at": "2024-01-01T12:30:00Z"
}
```

#### POST /content/{content_id}/publish
Publish content to configured platforms.

**Path Parameters:**
- `content_id` (integer): Content identifier

**Request Body:**
```json
{
  "blog_config_ids": [1, 2],
  "schedule_time": "2024-01-01T15:00:00Z",
  "custom_title": "Custom Title for Publishing",
  "custom_tags": ["custom", "publishing"]
}
```

**Response (202):**
```json
{
  "message": "Publishing job queued",
  "job_id": "pub_12345",
  "scheduled_for": "2024-01-01T15:00:00Z",
  "platforms": ["devto", "wordpress"]
}
```

### Blog Platform Configuration

#### GET /blog-configs/
List user's blog platform configurations.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "My Dev.to Blog",
    "platform": "devto",
    "is_active": true,
    "created_at": "2024-01-01T12:00:00Z",
    "last_used": "2024-01-02T10:30:00Z",
    "stats": {
      "posts_published": 15,
      "success_rate": 98.5,
      "last_error": null
    },
    "settings": {
      "auto_publish": false,
      "default_tags": ["tech", "programming"]
    }
  }
]
```

#### POST /blog-configs/
Add new blog platform configuration.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "name": "My WordPress Blog",
  "platform": "wordpress",
  "settings": {
    "url": "https://myblog.wordpress.com",
    "username": "myusername",
    "application_password": "app_password_here",
    "default_category": "Technology",
    "auto_publish": false
  }
}
```

**Response (201):**
```json
{
  "id": 2,
  "name": "My WordPress Blog",
  "platform": "wordpress",
  "is_active": true,
  "created_at": "2024-01-01T12:00:00Z"
}
```

#### PUT /blog-configs/{config_id}
Update blog configuration.

**Path Parameters:**
- `config_id` (integer): Configuration identifier

**Request Body:**
```json
{
  "is_active": false,
  "settings": {
    "auto_publish": true,
    "default_tags": ["tech", "ai", "programming"]
  }
}
```

#### DELETE /blog-configs/{config_id}
Delete blog configuration.

**Path Parameters:**
- `config_id` (integer): Configuration identifier

**Response (204):** No content

#### POST /blog-configs/{config_id}/test
Test blog platform connection.

**Path Parameters:**
- `config_id` (integer): Configuration identifier

**Response (200):**
```json
{
  "status": "success",
  "connection_time": 0.85,
  "platform_info": {
    "blog_title": "My WordPress Blog",
    "total_posts": 156,
    "last_post_date": "2024-01-01T10:00:00Z"
  }
}
```

### Demographics and Targeting

#### GET /demographics/
List available demographic profiles.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Tech Professionals",
    "description": "Software developers and tech industry professionals",
    "criteria": {
      "interests": ["programming", "technology", "software"],
      "experience_level": "intermediate_to_advanced",
      "age_range": "25-45",
      "engagement_patterns": ["high_technical_content", "discussion_oriented"]
    },
    "content_preferences": {
      "content_types": ["tutorial", "news", "analysis"],
      "minimum_depth": "intermediate",
      "preferred_length": "medium_to_long"
    }
  }
]
```

### Analytics and Dashboard

#### GET /dashboard/stats
Get dashboard statistics.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "runs": {
    "total": 5,
    "active": 3,
    "completed_today": 2
  },
  "content": {
    "total_collected": 1250,
    "pending_review": 45,
    "published_today": 8,
    "total_published": 234
  },
  "sources": {
    "configured": 3,
    "active": 2,
    "avg_response_time": 0.65
  },
  "publishing": {
    "platforms_configured": 2,
    "success_rate": 97.8,
    "posts_this_month": 67
  },
  "performance": {
    "collection_rate": "15.3 items/hour",
    "processing_time": "2.1 seconds avg",
    "uptime": "99.9%"
  }
}
```

## Error Handling

### Standard Error Response

All errors follow this format:

```json
{
  "detail": "Error description",
  "error_code": "SPECIFIC_ERROR_CODE",
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "req_12345"
}
```

### HTTP Status Codes

- **200**: Success
- **201**: Created
- **202**: Accepted (async operation)
- **204**: No Content
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **422**: Validation Error
- **429**: Rate Limited
- **500**: Internal Server Error

### Common Error Codes

- `INVALID_CREDENTIALS`: Authentication failed
- `TOKEN_EXPIRED`: JWT token has expired
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `RESOURCE_NOT_FOUND`: Requested resource doesn't exist
- `VALIDATION_ERROR`: Request data validation failed
- `SOURCE_UNAVAILABLE`: External data source is down
- `PUBLISHING_FAILED`: Content publishing failed
- `INSUFFICIENT_PERMISSIONS`: User lacks required permissions

## Client Examples

### Python

```python
import requests

class DashboardAPI:
    def __init__(self, base_url, email, password):
        self.base_url = base_url
        self.token = self._authenticate(email, password)
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    def _authenticate(self, email, password):
        response = requests.post(
            f"{self.base_url}/auth/login",
            data={"username": email, "password": password}
        )
        return response.json()["access_token"]
    
    def get_runs(self):
        response = requests.get(
            f"{self.base_url}/runs/",
            headers=self.headers
        )
        return response.json()
    
    def create_run(self, run_data):
        response = requests.post(
            f"{self.base_url}/runs/",
            json=run_data,
            headers=self.headers
        )
        return response.json()

# Usage
api = DashboardAPI("https://yourdomain.com/api/v1", "user@example.com", "password")
runs = api.get_runs()
```

### JavaScript

```javascript
class DashboardAPI {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
        this.token = null;
    }
    
    async authenticate(email, password) {
        const response = await fetch(`${this.baseUrl}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                username: email,
                password: password
            })
        });
        
        const data = await response.json();
        this.token = data.access_token;
        return this.token;
    }
    
    async getRuns() {
        const response = await fetch(`${this.baseUrl}/runs/`, {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        return response.json();
    }
    
    async createRun(runData) {
        const response = await fetch(`${this.baseUrl}/runs/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(runData)
        });
        return response.json();
    }
}

// Usage
const api = new DashboardAPI('https://yourdomain.com/api/v1');
await api.authenticate('user@example.com', 'password');
const runs = await api.getRuns();
```

### cURL Examples

```bash
# Authenticate
TOKEN=$(curl -X POST "https://yourdomain.com/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password" \
  | jq -r '.access_token')

# Get runs
curl -H "Authorization: Bearer $TOKEN" \
  "https://yourdomain.com/api/v1/runs/"

# Create run
curl -X POST "https://yourdomain.com/api/v1/runs/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "API Test Run",
    "frequency": "daily",
    "sources": [{"source_id": 1, "configuration": {"limit": 10}}]
  }'
```

## Webhooks

### Webhook Events

The API can send webhooks for important events:

- `run.completed`: Content collection run finished
- `content.approved`: Content was approved for publishing
- `content.published`: Content was successfully published
- `content.failed`: Content publishing failed
- `source.error`: Data source error occurred

### Webhook Configuration

```json
{
  "url": "https://your-app.com/webhooks/dashboard",
  "events": ["content.published", "run.completed"],
  "secret": "your_webhook_secret"
}
```

### Webhook Payload Example

```json
{
  "event": "content.published",
  "timestamp": "2024-01-01T12:00:00Z",
  "data": {
    "content_id": 123,
    "title": "Published Article Title",
    "platform": "devto",
    "published_url": "https://dev.to/user/article-slug",
    "run_id": 45
  },
  "signature": "sha256=..."
}
```

## API Versioning

- Current version: `v1`
- Version is specified in URL: `/api/v1/`
- Breaking changes will result in new version
- Previous versions supported for 12 months

For complete, interactive API documentation with examples and testing capabilities, visit: `https://yourdomain.com/docs`