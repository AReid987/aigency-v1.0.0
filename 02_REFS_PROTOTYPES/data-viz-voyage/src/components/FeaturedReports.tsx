
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { FileText, Download, Share, Calendar } from "lucide-react";

const reports = [
  {
    id: 1,
    title: "Q4 2024 Market Analysis: Technology Sector Deep Dive",
    description: "Comprehensive analysis of technology market trends, emerging opportunities, and competitive landscape for the fourth quarter of 2024.",
    author: "Dr. Sarah Chen",
    date: "2024-12-15",
    category: "Technology",
    status: "Latest",
    pages: 47,
    downloads: 1234,
  },
  {
    id: 2,
    title: "Consumer Behavior Study: Post-Pandemic Shopping Patterns",
    description: "In-depth research on how consumer purchasing decisions and shopping behaviors have evolved in the post-pandemic era.",
    author: "Prof. Michael Rodriguez",
    date: "2024-11-28",
    category: "Consumer Research",
    status: "Popular",
    pages: 32,
    downloads: 892,
  },
];

export function FeaturedReports() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-headline-medium">Featured Reports</h2>
          <p className="text-body-medium text-muted-foreground mt-1">
            Latest market research and analysis documents
          </p>
        </div>
        <Button variant="outline" className="flex items-center gap-2">
          <FileText className="w-4 h-4" />
          View All Reports
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {reports.map((report) => (
          <Card key={report.id} className="hover:shadow-md transition-shadow">
            <CardHeader className="pb-4">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <Badge 
                      variant={report.status === "Latest" ? "default" : "secondary"}
                      className="text-label-small"
                    >
                      {report.status}
                    </Badge>
                    <Badge variant="outline" className="text-label-small">
                      {report.category}
                    </Badge>
                  </div>
                  <CardTitle className="text-title-large leading-snug">
                    {report.title}
                  </CardTitle>
                </div>
                <FileText className="w-6 h-6 text-muted-foreground flex-shrink-0" />
              </div>
              <CardDescription className="text-body-medium text-muted-foreground leading-relaxed">
                {report.description}
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between text-body-small text-muted-foreground">
                  <div className="flex items-center gap-4">
                    <span>By {report.author}</span>
                    <div className="flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {new Date(report.date).toLocaleDateString()}
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <span>{report.pages} pages</span>
                    <span>{report.downloads} downloads</span>
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  <Button size="sm" className="flex items-center gap-2">
                    <FileText className="w-4 h-4" />
                    Read Report
                  </Button>
                  <Button variant="outline" size="sm" className="flex items-center gap-2">
                    <Download className="w-4 h-4" />
                    Download
                  </Button>
                  <Button variant="ghost" size="sm" className="flex items-center gap-2">
                    <Share className="w-4 h-4" />
                    Share
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
