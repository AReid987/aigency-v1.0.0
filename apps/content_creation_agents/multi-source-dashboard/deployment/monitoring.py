#!/usr/bin/env python3
"""
Multi-Source Dashboard Monitoring and Health Check System
Monitors system health, performance, and provides real-time status updates
"""

import asyncio
import httpx
import json
import time
import psutil
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class HealthCheck:
    service_name: str
    status: str  # healthy, degraded, unhealthy
    response_time: float
    timestamp: str
    details: Dict[str, Any]
    error: Optional[str] = None

@dataclass
class SystemMetrics:
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    timestamp: str

class DashboardMonitor:
    def __init__(self, backend_url="http://localhost:8000", frontend_url="http://localhost:5173"):
        self.backend_url = backend_url
        self.frontend_url = frontend_url
        self.client = httpx.AsyncClient(timeout=10.0)
        self.monitoring_data = []
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('monitoring.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    async def check_backend_health(self) -> HealthCheck:
        """Check backend API health"""
        start_time = time.time()
        try:
            response = await self.client.get(f"{self.backend_url}/health")
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                return HealthCheck(
                    service_name="backend_api",
                    status="healthy",
                    response_time=response_time,
                    timestamp=datetime.now().isoformat(),
                    details=data
                )
            else:
                return HealthCheck(
                    service_name="backend_api",
                    status="unhealthy",
                    response_time=response_time,
                    timestamp=datetime.now().isoformat(),
                    details={"status_code": response.status_code},
                    error=f"HTTP {response.status_code}"
                )
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                service_name="backend_api",
                status="unhealthy",
                response_time=response_time,
                timestamp=datetime.now().isoformat(),
                details={},
                error=str(e)
            )

    async def check_database_health(self) -> HealthCheck:
        """Check database connectivity through API"""
        start_time = time.time()
        try:
            # Try to access an endpoint that requires database
            response = await self.client.get(f"{self.backend_url}/api/v1/sources/")
            response_time = time.time() - start_time
            
            if response.status_code in [200, 401]:  # 401 is okay, means DB is accessible but auth needed
                return HealthCheck(
                    service_name="database",
                    status="healthy",
                    response_time=response_time,
                    timestamp=datetime.now().isoformat(),
                    details={"connection": "active"}
                )
            else:
                return HealthCheck(
                    service_name="database",
                    status="degraded",
                    response_time=response_time,
                    timestamp=datetime.now().isoformat(),
                    details={"status_code": response.status_code},
                    error=f"HTTP {response.status_code}"
                )
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                service_name="database",
                status="unhealthy",
                response_time=response_time,
                timestamp=datetime.now().isoformat(),
                details={},
                error=str(e)
            )

    async def check_frontend_health(self) -> HealthCheck:
        """Check frontend availability"""
        start_time = time.time()
        try:
            response = await self.client.get(self.frontend_url)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                content_length = len(response.content)
                return HealthCheck(
                    service_name="frontend",
                    status="healthy",
                    response_time=response_time,
                    timestamp=datetime.now().isoformat(),
                    details={
                        "content_length": content_length,
                        "content_type": response.headers.get("content-type", "unknown")
                    }
                )
            else:
                return HealthCheck(
                    service_name="frontend",
                    status="unhealthy",
                    response_time=response_time,
                    timestamp=datetime.now().isoformat(),
                    details={"status_code": response.status_code},
                    error=f"HTTP {response.status_code}"
                )
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                service_name="frontend",
                status="unhealthy",
                response_time=response_time,
                timestamp=datetime.now().isoformat(),
                details={},
                error=str(e)
            )

    async def check_task_queue_health(self) -> HealthCheck:
        """Check Celery/Redis task queue health"""
        start_time = time.time()
        try:
            # Try to access Flower monitoring (if available)
            response = await self.client.get("http://localhost:5555/api/workers")
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                workers = response.json()
                active_workers = len([w for w in workers.values() if w.get('active')])
                return HealthCheck(
                    service_name="task_queue",
                    status="healthy",
                    response_time=response_time,
                    timestamp=datetime.now().isoformat(),
                    details={
                        "active_workers": active_workers,
                        "total_workers": len(workers)
                    }
                )
            else:
                return HealthCheck(
                    service_name="task_queue",
                    status="degraded",
                    response_time=response_time,
                    timestamp=datetime.now().isoformat(),
                    details={"flower_unavailable": True},
                    error="Flower monitoring not accessible"
                )
        except Exception as e:
            response_time = time.time() - start_time
            return HealthCheck(
                service_name="task_queue",
                status="unknown",
                response_time=response_time,
                timestamp=datetime.now().isoformat(),
                details={},
                error=str(e)
            )

    async def check_external_apis(self) -> List[HealthCheck]:
        """Check external API dependencies"""
        external_apis = [
            ("hacker_news", "https://hacker-news.firebaseio.com/v0/maxitem.json"),
            ("reddit", "https://www.reddit.com/r/programming/.json"),
            ("dev_to", "https://dev.to/api/articles?per_page=1"),
        ]
        
        checks = []
        
        for api_name, url in external_apis:
            start_time = time.time()
            try:
                headers = {"User-Agent": "MultiSourceDashboard/1.0"} if "reddit" in url else {}
                response = await self.client.get(url, headers=headers)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    checks.append(HealthCheck(
                        service_name=f"external_api_{api_name}",
                        status="healthy",
                        response_time=response_time,
                        timestamp=datetime.now().isoformat(),
                        details={"status_code": response.status_code}
                    ))
                else:
                    checks.append(HealthCheck(
                        service_name=f"external_api_{api_name}",
                        status="degraded",
                        response_time=response_time,
                        timestamp=datetime.now().isoformat(),
                        details={"status_code": response.status_code},
                        error=f"HTTP {response.status_code}"
                    ))
            except Exception as e:
                response_time = time.time() - start_time
                checks.append(HealthCheck(
                    service_name=f"external_api_{api_name}",
                    status="unhealthy",
                    response_time=response_time,
                    timestamp=datetime.now().isoformat(),
                    details={},
                    error=str(e)
                ))
        
        return checks

    def get_system_metrics(self) -> SystemMetrics:
        """Get system resource usage metrics"""
        return SystemMetrics(
            cpu_percent=psutil.cpu_percent(interval=1),
            memory_percent=psutil.virtual_memory().percent,
            disk_percent=psutil.disk_usage('/').percent,
            timestamp=datetime.now().isoformat()
        )

    async def run_comprehensive_health_check(self) -> Dict[str, Any]:
        """Run all health checks and return comprehensive status"""
        self.logger.info("Starting comprehensive health check...")
        
        # Run all health checks
        checks = []
        
        # Core services
        checks.append(await self.check_backend_health())
        checks.append(await self.check_database_health())
        checks.append(await self.check_frontend_health())
        checks.append(await self.check_task_queue_health())
        
        # External APIs
        external_checks = await self.check_external_apis()
        checks.extend(external_checks)
        
        # System metrics
        system_metrics = self.get_system_metrics()
        
        # Calculate overall health
        healthy_count = sum(1 for check in checks if check.status == "healthy")
        total_checks = len(checks)
        health_percentage = (healthy_count / total_checks) * 100 if total_checks > 0 else 0
        
        if health_percentage >= 90:
            overall_status = "healthy"
        elif health_percentage >= 70:
            overall_status = "degraded"
        else:
            overall_status = "unhealthy"
        
        # Compile results
        results = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": overall_status,
            "health_percentage": health_percentage,
            "system_metrics": asdict(system_metrics),
            "service_checks": [asdict(check) for check in checks],
            "summary": {
                "total_services": total_checks,
                "healthy_services": healthy_count,
                "degraded_services": sum(1 for check in checks if check.status == "degraded"),
                "unhealthy_services": sum(1 for check in checks if check.status == "unhealthy"),
                "unknown_services": sum(1 for check in checks if check.status == "unknown")
            }
        }
        
        # Log summary
        self.logger.info(f"Health check complete - Overall: {overall_status} ({health_percentage:.1f}%)")
        
        return results

    async def continuous_monitoring(self, interval_seconds=60, duration_minutes=None):
        """Run continuous monitoring"""
        self.logger.info(f"Starting continuous monitoring (interval: {interval_seconds}s)")
        
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes) if duration_minutes else None
        
        monitoring_data = []
        
        try:
            while True:
                if end_time and datetime.now() > end_time:
                    break
                
                # Run health check
                health_results = await self.run_comprehensive_health_check()
                monitoring_data.append(health_results)
                
                # Display current status
                self.display_status_summary(health_results)
                
                # Save monitoring data
                self.save_monitoring_data(monitoring_data)
                
                # Check for alerts
                self.check_alerts(health_results)
                
                # Wait for next check
                await asyncio.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            self.logger.info("Monitoring stopped by user")
        except Exception as e:
            self.logger.error(f"Monitoring error: {e}")
        
        self.logger.info("Continuous monitoring ended")
        return monitoring_data

    def display_status_summary(self, health_results: Dict[str, Any]):
        """Display current status summary"""
        timestamp = health_results["timestamp"]
        overall_status = health_results["overall_status"]
        health_percentage = health_results["health_percentage"]
        
        # Status emoji
        status_emoji = {
            "healthy": "🟢",
            "degraded": "🟡", 
            "unhealthy": "🔴"
        }
        
        print(f"\n{status_emoji.get(overall_status, '⚪')} {timestamp} - {overall_status.upper()} ({health_percentage:.1f}%)")
        
        # Show service statuses
        for check in health_results["service_checks"]:
            service_emoji = status_emoji.get(check["status"], "⚪")
            response_time = check["response_time"]
            service_name = check["service_name"].replace("_", " ").title()
            
            if check.get("error"):
                print(f"  {service_emoji} {service_name:20} - {response_time:.3f}s - ERROR: {check['error']}")
            else:
                print(f"  {service_emoji} {service_name:20} - {response_time:.3f}s")
        
        # Show system metrics
        metrics = health_results["system_metrics"]
        print(f"  📊 System Resources:")
        print(f"     CPU: {metrics['cpu_percent']:.1f}%")
        print(f"     Memory: {metrics['memory_percent']:.1f}%")
        print(f"     Disk: {metrics['disk_percent']:.1f}%")

    def check_alerts(self, health_results: Dict[str, Any]):
        """Check for alert conditions"""
        # Define alert thresholds
        alerts = []
        
        # Overall health alerts
        if health_results["health_percentage"] < 50:
            alerts.append("🚨 CRITICAL: System health below 50%")
        elif health_results["health_percentage"] < 80:
            alerts.append("⚠️ WARNING: System health below 80%")
        
        # System resource alerts
        metrics = health_results["system_metrics"]
        if metrics["cpu_percent"] > 90:
            alerts.append(f"🚨 HIGH CPU: {metrics['cpu_percent']:.1f}%")
        if metrics["memory_percent"] > 90:
            alerts.append(f"🚨 HIGH MEMORY: {metrics['memory_percent']:.1f}%")
        if metrics["disk_percent"] > 90:
            alerts.append(f"🚨 HIGH DISK: {metrics['disk_percent']:.1f}%")
        
        # Service-specific alerts
        for check in health_results["service_checks"]:
            if check["status"] == "unhealthy":
                service_name = check["service_name"].replace("_", " ").title()
                alerts.append(f"🔴 SERVICE DOWN: {service_name}")
            elif check["response_time"] > 5.0:  # Response time > 5 seconds
                service_name = check["service_name"].replace("_", " ").title()
                alerts.append(f"🐌 SLOW RESPONSE: {service_name} ({check['response_time']:.1f}s)")
        
        # Log alerts
        for alert in alerts:
            self.logger.warning(alert)
            print(f"ALERT: {alert}")

    def save_monitoring_data(self, data: List[Dict[str, Any]]):
        """Save monitoring data to file"""
        try:
            with open('monitoring_data.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save monitoring data: {e}")

    def generate_monitoring_report(self, data: List[Dict[str, Any]]) -> str:
        """Generate monitoring report"""
        if not data:
            return "No monitoring data available"
        
        # Calculate statistics
        total_checks = len(data)
        healthy_checks = sum(1 for d in data if d["overall_status"] == "healthy")
        uptime_percentage = (healthy_checks / total_checks) * 100 if total_checks > 0 else 0
        
        # Find average response times
        avg_response_times = {}
        for data_point in data:
            for check in data_point["service_checks"]:
                service = check["service_name"]
                if service not in avg_response_times:
                    avg_response_times[service] = []
                avg_response_times[service].append(check["response_time"])
        
        # Calculate averages
        for service in avg_response_times:
            avg_response_times[service] = sum(avg_response_times[service]) / len(avg_response_times[service])
        
        # Generate report
        report = f"""# Multi-Source Dashboard Monitoring Report

Generated: {datetime.now().isoformat()}
Monitoring Period: {data[0]['timestamp']} to {data[-1]['timestamp']}
Total Checks: {total_checks}

## Overall Health
- Uptime: {uptime_percentage:.1f}%
- Healthy Checks: {healthy_checks}/{total_checks}

## Average Response Times
"""
        
        for service, avg_time in sorted(avg_response_times.items()):
            service_name = service.replace("_", " ").title()
            report += f"- {service_name}: {avg_time:.3f}s\n"
        
        report += "\n## Recent Status\n"
        if data:
            latest = data[-1]
            report += f"- Overall Status: {latest['overall_status']}\n"
            report += f"- Health Percentage: {latest['health_percentage']:.1f}%\n"
        
        return report

    async def cleanup(self):
        """Cleanup resources"""
        await self.client.aclose()

# CLI Interface
async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Multi-Source Dashboard Monitoring")
    parser.add_argument("--backend-url", default="http://localhost:8000", help="Backend URL")
    parser.add_argument("--frontend-url", default="http://localhost:5173", help="Frontend URL")
    parser.add_argument("--mode", choices=["single", "continuous"], default="single", help="Monitoring mode")
    parser.add_argument("--interval", type=int, default=60, help="Check interval in seconds (continuous mode)")
    parser.add_argument("--duration", type=int, help="Duration in minutes (continuous mode)")
    parser.add_argument("--report", action="store_true", help="Generate report")
    
    args = parser.parse_args()
    
    monitor = DashboardMonitor(args.backend_url, args.frontend_url)
    
    try:
        if args.mode == "single":
            # Run single health check
            results = await monitor.run_comprehensive_health_check()
            monitor.display_status_summary(results)
            
            if args.report:
                report = monitor.generate_monitoring_report([results])
                with open('monitoring_report.md', 'w') as f:
                    f.write(report)
                print("\n📊 Report saved to monitoring_report.md")
                
        else:
            # Run continuous monitoring
            data = await monitor.continuous_monitoring(args.interval, args.duration)
            
            if args.report and data:
                report = monitor.generate_monitoring_report(data)
                with open('monitoring_report.md', 'w') as f:
                    f.write(report)
                print("\n📊 Report saved to monitoring_report.md")
                
    finally:
        await monitor.cleanup()

if __name__ == "__main__":
    try:
        import psutil
    except ImportError:
        print("❌ psutil not installed. Run: pip install psutil")
        exit(1)
        
    asyncio.run(main())