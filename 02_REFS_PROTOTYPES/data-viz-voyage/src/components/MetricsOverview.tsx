
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingUp, TrendingDown, FileText, Users, BarChart, Calendar } from "lucide-react";

const metrics = [
  {
    title: "Total Reports",
    value: "47",
    change: "+12%",
    trend: "up",
    icon: FileText,
    description: "Published this quarter",
  },
  {
    title: "Active Users",
    value: "2,847",
    change: "+18%",
    trend: "up",
    icon: Users,
    description: "Monthly active readers",
  },
  {
    title: "Analytics Views",
    value: "15,392",
    change: "-3%",
    trend: "down",
    icon: BarChart,
    description: "Data visualizations accessed",
  },
  {
    title: "Research Projects",
    value: "23",
    change: "+7%",
    trend: "up",
    icon: Calendar,
    description: "Currently in progress",
  },
];

export function MetricsOverview() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {metrics.map((metric, index) => (
        <Card key={index} className="hover:shadow-md transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-title-small text-muted-foreground font-medium">
              {metric.title}
            </CardTitle>
            <metric.icon className="h-5 w-5 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="text-display-small font-bold text-foreground">
                {metric.value}
              </div>
              <div className="flex items-center space-x-2">
                <div className={`flex items-center space-x-1 text-body-small ${
                  metric.trend === "up" ? "text-green-600" : "text-red-600"
                }`}>
                  {metric.trend === "up" ? (
                    <TrendingUp className="h-3 w-3" />
                  ) : (
                    <TrendingDown className="h-3 w-3" />
                  )}
                  <span className="font-medium">{metric.change}</span>
                </div>
                <span className="text-body-small text-muted-foreground">
                  from last month
                </span>
              </div>
              <p className="text-body-small text-muted-foreground">
                {metric.description}
              </p>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
