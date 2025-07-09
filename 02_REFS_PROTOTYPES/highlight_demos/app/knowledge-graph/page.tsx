'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import dynamic from 'next/dynamic';
import KnowledgeGraphFallback from '@/components/knowledge-graph-fallback';

// Dynamically import the 3D component to avoid SSR issues
const KnowledgeGraph3D = dynamic(() => import('@/components/knowledge-graph-3d'), {
  ssr: false,
  loading: () => (
    <div className="flex items-center justify-center h-full">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
        <p className="text-gray-600 dark:text-gray-300">Loading 3D Knowledge Graph...</p>
      </div>
    </div>
  )
});
import type { GraphData } from '@/components/knowledge-graph-3d';
import {
  generateKnowledgeGraphData,
  generateSimpleKnowledgeGraph,
  generateKnowledgeGraphFromSystem
} from '@/lib/knowledge-graph-data';
import { mockData } from '@/lib/api-client';

export default function KnowledgeGraphPage() {
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [dataSource, setDataSource] = useState<'sample' | 'simple' | 'system'>('sample');
  const [isLoading, setIsLoading] = useState(false);
  const [use3D, setUse3D] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load initial data
  useEffect(() => {
    loadGraphData(dataSource);
  }, [dataSource]);

  const loadGraphData = async (source: 'sample' | 'simple' | 'system') => {
    setIsLoading(true);
    setError(null);

    try {
      let data: GraphData;

      switch (source) {
        case 'simple':
          data = generateSimpleKnowledgeGraph();
          break;
        case 'system':
          // In a real app, you'd fetch this from your API
          data = generateKnowledgeGraphFromSystem(
            mockData.users,
            mockData.agents,
            [], // documents
            mockData.knowledgeBases
          );
          break;
        case 'sample':
        default:
          data = generateKnowledgeGraphData();
          break;
      }

      setGraphData(data);
    } catch (error) {
      console.error('Error loading graph data:', error);
      setError(error instanceof Error ? error.message : 'Failed to load graph data');
      setUse3D(false); // Fall back to 2D on error
    } finally {
      setIsLoading(false);
    }
  };

  const handleDataSourceChange = (source: 'sample' | 'simple' | 'system') => {
    setDataSource(source);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <div className="p-8 pb-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              3D Knowledge Graph Visualization
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-300 mb-6">
              Explore knowledge relationships in an interactive 3D space
            </p>

            {/* Data Source Controls */}
            <div className="flex justify-center gap-4 mb-6">
              <Button
                variant={dataSource === 'simple' ? 'default' : 'outline'}
                onClick={() => handleDataSourceChange('simple')}
                disabled={isLoading}
              >
                Simple Graph
              </Button>
              <Button
                variant={dataSource === 'sample' ? 'default' : 'outline'}
                onClick={() => handleDataSourceChange('sample')}
                disabled={isLoading}
              >
                AI Knowledge Graph
              </Button>
              <Button
                variant={dataSource === 'system' ? 'default' : 'outline'}
                onClick={() => handleDataSourceChange('system')}
                disabled={isLoading}
              >
                System Data
              </Button>
            </div>

            {/* 3D/2D Toggle */}
            <div className="flex justify-center gap-2 mt-4">
              <Button
                variant={use3D ? 'default' : 'outline'}
                onClick={() => setUse3D(true)}
                disabled={isLoading}
              >
                3D View
              </Button>
              <Button
                variant={!use3D ? 'default' : 'outline'}
                onClick={() => setUse3D(false)}
                disabled={isLoading}
              >
                2D View
              </Button>
            </div>
          </div>

          {/* Error Display */}
          {error && (
            <div className="mb-6">
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium">3D Rendering Error</h3>
                    <div className="mt-2 text-sm">
                      <p>{error}</p>
                      <p className="mt-1">Switched to 2D view automatically.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Graph Statistics */}
          {graphData && (
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">Total Nodes</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{graphData.nodes.length}</div>
                  <div className="text-xs text-gray-500 mt-1">
                    Concepts, Entities, Documents, Agents, Users
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">Connections</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{graphData.edges.length}</div>
                  <div className="text-xs text-gray-500 mt-1">
                    Relationships between entities
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">Node Types</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {new Set(graphData.nodes.map(n => n.type)).size}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">
                    Different entity categories
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">Data Source</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-lg font-semibold capitalize">{dataSource}</div>
                  <div className="text-xs text-gray-500 mt-1">
                    Current visualization data
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </div>

      {/* 3D Graph Visualization */}
      <div className="px-8 pb-8">
        <div className="max-w-7xl mx-auto">
          <Card className="overflow-hidden">
            <CardContent className="p-0">
              <div style={{ height: '700px', width: '100%' }}>
                {isLoading ? (
                  <div className="flex items-center justify-center h-full">
                    <div className="text-center">
                      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
                      <p className="text-gray-600 dark:text-gray-300">Loading knowledge graph...</p>
                    </div>
                  </div>
                ) : graphData ? (
                  use3D ? (
                    <KnowledgeGraph3D data={graphData} />
                  ) : (
                    <KnowledgeGraphFallback data={graphData} />
                  )
                ) : (
                  <div className="flex items-center justify-center h-full">
                    <p className="text-gray-600 dark:text-gray-300">No data available</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Information Panel */}
      <div className="px-8 pb-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Features */}
            <Card>
              <CardHeader>
                <CardTitle>3D Visualization Features</CardTitle>
                <CardDescription>
                  Interactive features available in the knowledge graph
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                  <div>
                    <p className="font-medium">Interactive Navigation</p>
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      Orbit, zoom, and pan around the 3D space
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                  <div>
                    <p className="font-medium">Node Selection</p>
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      Click nodes to view detailed information
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-purple-500 rounded-full mt-2"></div>
                  <div>
                    <p className="font-medium">Dynamic Layouts</p>
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      Switch between sphere, cube, random, and force-directed layouts
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-orange-500 rounded-full mt-2"></div>
                  <div>
                    <p className="font-medium">Hover Effects</p>
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      Smooth animations and visual feedback on interaction
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-red-500 rounded-full mt-2"></div>
                  <div>
                    <p className="font-medium">Connection Visualization</p>
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      Color-coded edges showing different relationship types
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Controls Guide */}
            <Card>
              <CardHeader>
                <CardTitle>How to Use</CardTitle>
                <CardDescription>
                  Guide to navigating the 3D knowledge graph
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <h4 className="font-medium mb-2">Mouse Controls</h4>
                  <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-300">
                    <li>• <strong>Left Click + Drag:</strong> Rotate the view</li>
                    <li>• <strong>Right Click + Drag:</strong> Pan the view</li>
                    <li>• <strong>Scroll Wheel:</strong> Zoom in/out</li>
                    <li>• <strong>Click Node:</strong> Select and view details</li>
                    <li>• <strong>Hover Node:</strong> Highlight and preview</li>
                  </ul>
                </div>

                <div>
                  <h4 className="font-medium mb-2">Layout Options</h4>
                  <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-300">
                    <li>• <strong>Sphere:</strong> Nodes arranged on sphere surface</li>
                    <li>• <strong>Cube:</strong> 3D grid arrangement</li>
                    <li>• <strong>Random:</strong> Scattered positioning</li>
                    <li>• <strong>Force:</strong> Physics-based layout</li>
                  </ul>
                </div>

                <div>
                  <h4 className="font-medium mb-2">Visual Legend</h4>
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                      <span>Concepts</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                      <span>Entities</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                      <span>Documents</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
                      <span>Agents</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
                      <span>Users</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
