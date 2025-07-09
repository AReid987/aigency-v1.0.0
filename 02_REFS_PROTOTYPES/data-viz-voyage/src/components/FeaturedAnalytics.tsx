
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from "recharts";

const marketData = [
  { month: "Jan", revenue: 4000, growth: 24 },
  { month: "Feb", revenue: 3000, growth: 13 },
  { month: "Mar", revenue: 2000, growth: -11 },
  { month: "Apr", revenue: 2780, growth: 39 },
  { month: "May", revenue: 1890, growth: -14 },
  { month: "Jun", revenue: 2390, growth: 26 },
];

const trendData = [
  { quarter: "Q1", adoption: 65, satisfaction: 78 },
  { quarter: "Q2", adoption: 72, satisfaction: 82 },
  { quarter: "Q3", adoption: 78, satisfaction: 85 },
  { quarter: "Q4", adoption: 84, satisfaction: 89 },
];

export function FeaturedAnalytics() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <Card className="col-span-1">
        <CardHeader className="pb-4">
          <div className="flex items-center justify-between">
            <CardTitle className="text-headline-small">Market Revenue Trends</CardTitle>
            <Badge variant="secondary" className="text-label-small">
              6M Data
            </Badge>
          </div>
          <CardDescription className="text-body-medium text-muted-foreground">
            Monthly revenue performance and growth analysis
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={marketData}>
              <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
              <XAxis 
                dataKey="month" 
                className="text-body-small"
                tick={{ fontSize: 12 }}
              />
              <YAxis 
                className="text-body-small"
                tick={{ fontSize: 12 }}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: 'hsl(var(--card))',
                  border: '1px solid hsl(var(--border))',
                  borderRadius: '8px',
                  fontSize: '14px'
                }}
              />
              <Bar dataKey="revenue" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card className="col-span-1">
        <CardHeader className="pb-4">
          <div className="flex items-center justify-between">
            <CardTitle className="text-headline-small">Quarterly Trends</CardTitle>
            <Badge variant="outline" className="text-label-small">
              Live Data
            </Badge>
          </div>
          <CardDescription className="text-body-medium text-muted-foreground">
            Product adoption and customer satisfaction metrics
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
              <XAxis 
                dataKey="quarter" 
                className="text-body-small"
                tick={{ fontSize: 12 }}
              />
              <YAxis 
                className="text-body-small"
                tick={{ fontSize: 12 }}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: 'hsl(var(--card))',
                  border: '1px solid hsl(var(--border))',
                  borderRadius: '8px',
                  fontSize: '14px'
                }}
              />
              <Line 
                type="monotone" 
                dataKey="adoption" 
                stroke="hsl(var(--primary))" 
                strokeWidth={3}
                dot={{ fill: 'hsl(var(--primary))', strokeWidth: 2, r: 4 }}
              />
              <Line 
                type="monotone" 
                dataKey="satisfaction" 
                stroke="hsl(var(--accent-foreground))" 
                strokeWidth={3}
                dot={{ fill: 'hsl(var(--accent-foreground))', strokeWidth: 2, r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}
