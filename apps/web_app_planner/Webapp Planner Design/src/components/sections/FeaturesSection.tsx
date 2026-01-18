import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { Label } from '@/components/ui/label';

interface Feature {
  id: string;
  name: string;
}

interface FeaturesSectionProps {
  data: Feature[];
  onSave: (data: Feature[]) => void;
}

const FeaturesSection: React.FC<FeaturesSectionProps> = ({ data, onSave }) => {
  const [features, setFeatures] = useState<Feature[]>(data);
  const [newFeatureName, setNewFeatureName] = useState('');

  const addFeature = () => {
    if (newFeatureName.trim()) {
      const feature: Feature = {
        id: crypto.randomUUID(),
        name: newFeatureName.trim()
      };
      const updatedFeatures = [...features, feature];
      setFeatures(updatedFeatures);
      onSave(updatedFeatures);
      setNewFeatureName('');
    }
  };

  const removeFeature = (id: string) => {
    const updatedFeatures = features.filter(feature => feature.id !== id);
    setFeatures(updatedFeatures);
    onSave(updatedFeatures);
  };

  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-6">List Core Features and Functionalities</h1>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
          Based on your goals and user stories, list the main features your app will offer.
        </p>
      </div>

      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Add New Feature</h2>
        <div className="flex gap-4 mb-4">
          <div className="flex-grow">
            <Label htmlFor="featureName">Feature Name</Label>
            <Input
              id="featureName"
              value={newFeatureName}
              onChange={(e) => setNewFeatureName(e.target.value)}
              placeholder="e.g., User Profile Management"
            />
          </div>
          <div className="flex-shrink-0 self-end">
            <Button onClick={addFeature} className="bg-indigo-600 hover:bg-indigo-700 h-10">
              Add Feature
            </Button>
          </div>
        </div>
      </Card>

      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Your Features</h2>
        <div className="space-y-3">
          {features.length === 0 ? (
            <p className="text-gray-500 dark:text-gray-400 italic">No features added yet.</p>
          ) : (
            features.map((feature) => (
              <div key={feature.id} className="bg-gray-50 dark:bg-gray-700 p-4 rounded-md border flex justify-between items-center">
                <span className="font-medium text-gray-800 dark:text-gray-200">
                  {feature.name}
                </span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => removeFeature(feature.id)}
                  className="text-red-500 hover:text-red-700"
                >
                  ✕
                </Button>
              </div>
            ))
          )}
        </div>
      </Card>
    </section>
  );
};

export default FeaturesSection;