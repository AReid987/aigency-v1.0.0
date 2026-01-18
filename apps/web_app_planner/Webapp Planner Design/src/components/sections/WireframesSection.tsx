import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Card } from '@/components/ui/card';
import { Label } from '@/components/ui/label';

interface Wireframe {
  id: string;
  screenName: string;
  keyElements: string;
  interactions: string;
}

interface WireframesSectionProps {
  data: Wireframe[];
  onSave: (data: Wireframe[]) => void;
}

const WireframesSection: React.FC<WireframesSectionProps> = ({ data, onSave }) => {
  const [wireframes, setWireframes] = useState<Wireframe[]>(data);
  const [newWireframe, setNewWireframe] = useState({
    screenName: '',
    keyElements: '',
    interactions: ''
  });

  const addWireframe = () => {
    if (newWireframe.screenName.trim()) {
      const wireframe: Wireframe = {
        id: crypto.randomUUID(),
        screenName: newWireframe.screenName.trim(),
        keyElements: newWireframe.keyElements.trim(),
        interactions: newWireframe.interactions.trim()
      };
      const updatedWireframes = [...wireframes, wireframe];
      setWireframes(updatedWireframes);
      onSave(updatedWireframes);
      setNewWireframe({ screenName: '', keyElements: '', interactions: '' });
    }
  };

  const removeWireframe = (id: string) => {
    const updatedWireframes = wireframes.filter(wireframe => wireframe.id !== id);
    setWireframes(updatedWireframes);
    onSave(updatedWireframes);
  };

  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-6">Describe Basic Wireframes/Mockups</h1>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
          Sketch out the basic structure and layout of your app's main screens. Focus on functionality and flow.
        </p>
      </div>

      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Add Screen Description</h2>
        <div className="space-y-4 mb-4">
          <div>
            <Label htmlFor="screenName">Screen Name/Purpose</Label>
            <Input
              id="screenName"
              value={newWireframe.screenName}
              onChange={(e) => setNewWireframe(prev => ({ ...prev, screenName: e.target.value }))}
              placeholder="e.g., Home Page - Display featured events"
            />
          </div>
          <div>
            <Label htmlFor="keyElements">Key Elements (list them)</Label>
            <Textarea
              id="keyElements"
              value={newWireframe.keyElements}
              onChange={(e) => setNewWireframe(prev => ({ ...prev, keyElements: e.target.value }))}
              placeholder="e.g., Navigation bar, Search input, Event cards, Footer"
              rows={3}
            />
          </div>
          <div>
            <Label htmlFor="interactions">User Interactions/Flow</Label>
            <Textarea
              id="interactions"
              value={newWireframe.interactions}
              onChange={(e) => setNewWireframe(prev => ({ ...prev, interactions: e.target.value }))}
              placeholder="e.g., User clicks on event card > navigates to Event Detail Screen"
              rows={3}
            />
          </div>
        </div>
        <Button onClick={addWireframe} className="bg-indigo-600 hover:bg-indigo-700">
          Add Screen Description
        </Button>
      </Card>

      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Your Screen Descriptions</h2>
        <div className="space-y-3">
          {wireframes.length === 0 ? (
            <p className="text-gray-500 dark:text-gray-400 italic">No screen descriptions added yet.</p>
          ) : (
            wireframes.map((wireframe) => (
              <div key={wireframe.id} className="bg-gray-50 dark:bg-gray-700 p-4 rounded-md border">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h3 className="font-semibold text-indigo-700 dark:text-indigo-400 mb-2">
                      {wireframe.screenName}
                    </h3>
                    {wireframe.keyElements && (
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                        <strong>Elements:</strong> {wireframe.keyElements}
                      </p>
                    )}
                    {wireframe.interactions && (
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        <strong>Interactions:</strong> {wireframe.interactions}
                      </p>
                    )}
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => removeWireframe(wireframe.id)}
                    className="text-red-500 hover:text-red-700 ml-2"
                  >
                    ✕
                  </Button>
                </div>
              </div>
            ))
          )}
        </div>
      </Card>
    </section>
  );
};

export default WireframesSection;