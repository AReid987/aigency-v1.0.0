# Rate Limiting & Compliance Strategy Guide

## 1. Rate Limiting Implementation Strategy

### Multi-API Rate Limit Management

#### Centralized Rate Limiter
```python
import asyncio
import time
from collections import defaultdict, deque
from typing import Dict, Optional
import aioredis

class RateLimiter:
    def __init__(self, redis_client: aioredis.Redis):
        self.redis = redis_client
        self.local_limits = defaultdict(lambda: defaultdict(deque))
    
    async def check_rate_limit(self, api_name: str, requests_per_minute: int) -> bool:
        """Check if request is within rate limit"""
        current_time = time.time()
        window_start = current_time - 60  # 1-minute window
        
        # Use Redis for distributed rate limiting
        key = f"rate_limit:{api_name}"
        pipe = self.redis.pipeline()
        
        # Remove old entries
        await pipe.zremrangebyscore(key, 0, window_start)
        # Count current requests
        await pipe.zcard(key)
        # Add current request
        await pipe.zadd(key, {str(current_time): current_time})
        # Set expiration
        await pipe.expire(key, 60)
        
        results = await pipe.execute()
        current_requests = results[1]
        
        return current_requests < requests_per_minute

    async def wait_for_rate_limit(self, api_name: str, requests_per_minute: int):
        """Wait until rate limit allows request"""
        while not await self.check_rate_limit(api_name, requests_per_minute):
            wait_time = 60 / requests_per_minute
            await asyncio.sleep(wait_time)

# API-specific rate limit configurations
API_RATE_LIMITS = {
    'hackernews': {'rpm': None, 'burst': 10},  # No official limit, be respectful
    'reddit': {'rpm': 100, 'burst': 5},
    'producthunt': {'rpm': 60, 'burst': 3},
    'gnews': {'rpm': 60, 'burst': 1},  # Depends on plan
    'newsapi': {'rpm': 1000, 'burst': 10},  # Depends on plan
    'wordpress': {'rpm': 120, 'burst': 5},  # Server dependent
    'ghost': {'rpm': 300, 'burst': 10},  # Generous limits
    'devto': {'rpm': 30, 'burst': 2}  # Strict limits
}
```

#### Intelligent Request Scheduling
```python
import heapq
from dataclasses import dataclass
from typing import Priority
import asyncio

@dataclass
class APIRequest:
    priority: int
    api_name: str
    request_func: callable
    args: tuple
    kwargs: dict
    created_at: float
    
    def __lt__(self, other):
        return self.priority < other.priority

class RequestScheduler:
    def __init__(self, rate_limiter: RateLimiter):
        self.rate_limiter = rate_limiter
        self.queue = []
        self.running = False
    
    async def schedule_request(self, api_name: str, request_func: callable, 
                             priority: int = 1, *args, **kwargs):
        """Schedule an API request with priority"""
        request = APIRequest(
            priority=priority,
            api_name=api_name,
            request_func=request_func,
            args=args,
            kwargs=kwargs,
            created_at=time.time()
        )
        
        heapq.heappush(self.queue, request)
        
        if not self.running:
            asyncio.create_task(self._process_queue())
    
    async def _process_queue(self):
        """Process queued requests respecting rate limits"""
        self.running = True
        
        while self.queue:
            request = heapq.heappop(self.queue)
            
            # Check rate limit for this API
            config = API_RATE_LIMITS.get(request.api_name, {'rpm': 60})
            if config['rpm']:
                await self.rate_limiter.wait_for_rate_limit(
                    request.api_name, config['rpm']
                )
            
            # Execute request
            try:
                result = await request.request_func(*request.args, **request.kwargs)
                # Handle result
            except Exception as e:
                # Handle error, possibly retry
                pass
            
            # Small delay between requests
            await asyncio.sleep(0.1)
        
        self.running = False
```

## 2. Platform-Specific Compliance Requirements

### Data Source APIs Compliance

#### Hacker News
- **Rate Limiting**: Self-imposed respectful usage
- **Terms of Service**: Public data, attribution recommended
- **Data Retention**: No specific restrictions
- **Commercial Use**: Allowed with proper attribution

```python
async def fetch_hackernews_respectfully():
    """Implement respectful fetching for Hacker News"""
    # Implement exponential backoff
    base_delay = 1
    max_delay = 60
    
    for attempt in range(3):
        try:
            response = await httpx.get(url, timeout=30)
            if response.status_code == 200:
                return response.json()
            
            # Exponential backoff on failure
            delay = min(base_delay * (2 ** attempt), max_delay)
            await asyncio.sleep(delay)
            
        except Exception:
            if attempt == 2:
                raise
            await asyncio.sleep(base_delay * (2 ** attempt))
```

#### Reddit API
- **Authentication**: OAuth2 required for 100 QPM
- **Rate Limiting**: Strict enforcement, 10 QPM without OAuth
- **Content Guidelines**: Respect subreddit rules
- **Data Usage**: Limited to platform terms

```python
class RedditAPIClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires_at = 0
    
    async def ensure_authenticated(self):
        """Ensure valid OAuth token"""
        if time.time() >= self.token_expires_at:
            await self._refresh_token()
    
    async def _refresh_token(self):
        """Refresh OAuth token"""
        auth = aiohttp.BasicAuth(self.client_id, self.client_secret)
        data = {
            'grant_type': 'client_credentials',
            'scope': 'read'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://www.reddit.com/api/v1/access_token',
                auth=auth,
                data=data,
                headers={'User-Agent': 'YourApp/1.0'}
            ) as response:
                token_data = await response.json()
                self.access_token = token_data['access_token']
                self.token_expires_at = time.time() + token_data['expires_in'] - 60
```

### Publishing APIs Compliance

#### WordPress
- **Self-hosted**: Full control over rate limits
- **WordPress.com**: Follows hosting provider limits
- **Content Policy**: Follow WordPress terms of service
- **Media Storage**: Respect storage limits

#### Ghost
- **Rate Limiting**: No official limits, but be respectful
- **Content Policy**: Follow Ghost terms of service
- **API Keys**: Secure storage required
- **Commercial Use**: Allowed with proper licensing

#### Dev.to
- **Rate Limiting**: Strict 30 requests per 30 seconds
- **Content Guidelines**: Must follow community guidelines
- **Spam Prevention**: Avoid duplicate or low-quality content
- **Attribution**: Proper attribution for republished content

```python
class DevToCompliantPublisher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.last_request_time = 0
        self.request_count = 0
        self.rate_limit_window = 30  # seconds
        self.rate_limit_requests = 30
    
    async def publish_article(self, article_data: dict):
        """Publish with rate limit compliance"""
        await self._wait_for_rate_limit()
        
        headers = {
            'api-key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        # Validate content guidelines
        if not self._validate_content(article_data):
            raise ValueError("Content doesn't meet Dev.to guidelines")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://dev.to/api/articles',
                headers=headers,
                json={'article': article_data}
            )
            
            # Handle rate limit headers
            self._update_rate_limit_info(response.headers)
            
            return response.json()
    
    def _validate_content(self, article_data: dict) -> bool:
        """Validate content meets platform guidelines"""
        # Check for minimum content length
        if len(article_data.get('body_markdown', '')) < 100:
            return False
        
        # Check for spam indicators
        if self._detect_spam_patterns(article_data):
            return False
        
        return True
```

## 3. Data Retention and Privacy

### GDPR Compliance Framework
```python
from datetime import datetime, timedelta
import logging

class DataRetentionManager:
    def __init__(self, db_connection):
        self.db = db_connection
        self.retention_policies = {
            'articles': timedelta(days=365),
            'user_data': timedelta(days=1095),  # 3 years
            'api_logs': timedelta(days=90),
            'error_logs': timedelta(days=365)
        }
    
    async def cleanup_expired_data(self):
        """Remove data beyond retention period"""
        for table, retention_period in self.retention_policies.items():
            cutoff_date = datetime.now() - retention_period
            
            # Soft delete with audit trail
            query = f"""
                UPDATE {table} 
                SET deleted_at = NOW(), 
                    deleted_reason = 'retention_policy'
                WHERE created_at < %s 
                AND deleted_at IS NULL
            """
            
            result = await self.db.execute(query, (cutoff_date,))
            logging.info(f"Marked {result.rowcount} records for deletion in {table}")
    
    async def anonymize_user_data(self, user_id: str):
        """Anonymize user data for GDPR compliance"""
        # Replace PII with anonymized values
        anonymized_data = {
            'email': f"anonymized_{hash(user_id)[:8]}@deleted.local",
            'name': f"Deleted User {hash(user_id)[:6]}",
            'ip_address': None,
            'user_agent': None
        }
        
        query = """
            UPDATE users 
            SET email = %s, name = %s, ip_address = %s, user_agent = %s,
                anonymized_at = NOW()
            WHERE id = %s
        """
        
        await self.db.execute(query, (*anonymized_data.values(), user_id))
```

### Privacy by Design Implementation
```python
class PrivacyComplianceLayer:
    def __init__(self):
        self.data_minimization_rules = {
            'hackernews': ['id', 'title', 'url', 'score', 'time'],
            'reddit': ['id', 'title', 'url', 'score', 'created_utc'],
            'producthunt': ['id', 'name', 'tagline', 'votes_count']
        }
    
    def filter_collected_data(self, source: str, raw_data: dict) -> dict:
        """Filter data to minimum necessary fields"""
        allowed_fields = self.data_minimization_rules.get(source, [])
        return {k: v for k, v in raw_data.items() if k in allowed_fields}
    
    def add_privacy_headers(self, response):
        """Add privacy-compliant headers"""
        response.headers.update({
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0'
        })
```

## 4. Monitoring and Alerting

### Rate Limit Monitoring
```python
import prometheus_client
from prometheus_client import Counter, Histogram, Gauge

# Metrics
api_requests_total = Counter('api_requests_total', 'Total API requests', ['api', 'status'])
api_request_duration = Histogram('api_request_duration_seconds', 'API request duration', ['api'])
rate_limit_remaining = Gauge('rate_limit_remaining', 'Remaining rate limit', ['api'])

class APIMetrics:
    @staticmethod
    def record_request(api_name: str, status: str, duration: float):
        api_requests_total.labels(api=api_name, status=status).inc()
        api_request_duration.labels(api=api_name).observe(duration)
    
    @staticmethod
    def update_rate_limit(api_name: str, remaining: int):
        rate_limit_remaining.labels(api=api_name).set(remaining)
```

### Compliance Monitoring Dashboard
```python
class ComplianceMonitor:
    def __init__(self):
        self.alerts = []
    
    async def check_compliance_status(self):
        """Regular compliance checks"""
        # Check rate limit compliance
        for api, config in API_RATE_LIMITS.items():
            usage = await self.get_api_usage(api)
            if usage > config['rpm'] * 0.9:  # 90% threshold
                await self.send_alert(f"High API usage for {api}: {usage}")
        
        # Check data retention compliance
        expired_data = await self.check_expired_data()
        if expired_data:
            await self.send_alert(f"Data retention cleanup needed: {expired_data}")
    
    async def send_alert(self, message: str):
        """Send compliance alert"""
        # Implementation for Slack, email, or monitoring system
        logging.warning(f"COMPLIANCE ALERT: {message}")
```

## 5. Implementation Checklist

### Setup Phase
- [ ] Implement centralized rate limiter with Redis
- [ ] Configure API-specific rate limits
- [ ] Set up request scheduling system
- [ ] Implement OAuth flows for required APIs

### Compliance Phase
- [ ] Review and document ToS for each platform
- [ ] Implement data minimization filters
- [ ] Set up data retention policies
- [ ] Configure privacy-compliant headers

### Monitoring Phase
- [ ] Set up Prometheus metrics
- [ ] Configure alerting thresholds
- [ ] Implement compliance dashboard
- [ ] Set up automated compliance checks

### Documentation Phase
- [ ] Document rate limiting strategies
- [ ] Create compliance runbooks
- [ ] Set up incident response procedures
- [ ] Regular compliance audits

This comprehensive approach ensures your multi-source dashboard remains compliant with all platform requirements while maintaining efficient and reliable operation.