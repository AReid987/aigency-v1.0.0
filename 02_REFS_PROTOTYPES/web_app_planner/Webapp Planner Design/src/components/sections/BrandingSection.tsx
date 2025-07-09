import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Card } from '@/components/ui/card';
import { Label } from '@/components/ui/label';

interface BrandingData {
  mission: string;
  values: string[];
  audience: string;
  personality: string;
  moodboard: string;
}

interface BrandingSectionProps {
  data: BrandingData;
  onSave: (data: BrandingData) => void;
}

const BrandingSection: React.FC<BrandingSectionProps> = ({ data, onSave }) => {
  const [formData, setFormData] = useState<BrandingData>(data);
  const [newValue, setNewValue] = useState('');

  const handleInputChange = (field: keyof BrandingData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const addValue = () => {
    if (newValue.trim()) {
      setFormData(prev => ({
        ...prev,
        values: [...prev.values, newValue.trim()]
      }));
      setNewValue('');
    }
  };

  const removeValue = (index: number) => {
    setFormData(prev => ({
      ...prev,
      values: prev.values.filter((_, i) => i !== index)
    }));
  };

  const handleSave = () => {
    onSave(formData);
  };

  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-6">Define Your Brand</h1>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
          Branding is the heart and soul of your application. It's how users perceive and connect with your product.
        </p>
      </div>

      <Card className="p-6">
        <Label htmlFor="mission" className="text-lg font-semibold mb-2 block">
          Mission Statement
        </Label>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
          What is the ultimate purpose of your app? What problem does it solve?
        </p>
        <Textarea
          id="mission"
          value={formData.mission}
          onChange={(e) => handleInputChange('mission', e.target.value)}
          placeholder="e.g., To empower small businesses with easy-to-use accounting tools."
          rows={3}
        />
      </Card>

      <Card className="p-6">
        <Label className="text-lg font-semibold mb-2 block">Core Values</Label>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
          What principles guide your app's development? List 3-5 key values.
        </p>
        <div className="space-y-2 mb-3">
          {formData.values.map((value, index) => (
            <div key={index} className="flex items-center justify-between bg-gray-50 dark:bg-gray-700 p-3 rounded-md">
              <span>{value}</span>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => removeValue(index)}
                className="text-red-500 hover:text-red-700"
              >
                ✕
              </Button>
            </div>
          ))}
        </div>
        <div className="flex gap-2">
          <Input
            value={newValue}
            onChange={(e) => setNewValue(e.target.value)}
            placeholder="e.g., Simplicity, Reliability"
            className="flex-grow"
          />
          <Button onClick={addValue} variant="outline">
            Add Value
          </Button>
        </div>
      </Card>

      <Card className="p-6">
        <Label htmlFor="audience" className="text-lg font-semibold mb-2 block">
          Target Audience
        </Label>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
          Describe your ideal user. Who are they and what are their needs?
        </p>
        <Textarea
          id="audience"
          value={formData.audience}
          onChange={(e) => handleInputChange('audience', e.target.value)}
          placeholder="e.g., Freelancers aged 25-45, comfortable with web apps"
          rows={4}
        />
      </Card>

      <Card className="p-6">
        <Label htmlFor="personality" className="text-lg font-semibold mb-2 block">
          Brand Personality & Voice
        </Label>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
          If your brand were a person, what would they be like?
        </p>
        <Textarea
          id="personality"
          value={formData.personality}
          onChange={(e) => handleInputChange('personality', e.target.value)}
          placeholder="e.g., Friendly, approachable, and empowering"
          rows={3}
        />
      </Card>

      <Card className="p-6">
        <Label htmlFor="moodboard" className="text-lg font-semibold mb-2 block">
          Moodboard Links/Notes
        </Label>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
          Collect visual inspiration (colors, imagery, typography).
        </p>
        <Textarea
          id="moodboard"
          value={formData.moodboard}
          onChange={(e) => handleInputChange('moodboard', e.target.value)}
          placeholder="e.g., Pinterest board: [link], Clean minimalist aesthetic"
          rows={4}
        />
      </Card>

      <Button onClick={handleSave} className="bg-indigo-600 hover:bg-indigo-700">
        Save Branding
      </Button>
    </section>
  );
};

export default BrandingSection;