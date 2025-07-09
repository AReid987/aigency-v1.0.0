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
        <p className="description mb-6">
          Branding is the heart and soul of your application. It's how users perceive and connect with your product.
        </p>
      </div>

      <div className="card">
        <Label htmlFor="mission" className="text-lg font-semibold mb-2 block">
          Mission Statement
        </Label>
        <p className="description">
          What is the ultimate purpose of your app? What problem does it solve?
        </p>
        <Textarea
          id="mission"
          value={formData.mission}
          onChange={(e) => handleInputChange('mission', e.target.value)}
          placeholder="e.g., To empower small businesses with easy-to-use accounting tools."
          rows={3}
          className="rounded-lg"
        />
      </div>

      <div className="card">
        <Label className="text-lg font-semibold mb-2 block">Core Values</Label>
        <p className="description">
          What principles guide your app's development? List 3-5 key values.
        </p>
        <div className="space-y-2 mb-3">
          {formData.values.map((value, index) => (
            <div key={index} className="list-item flex items-center justify-between">
              <span>{value}</span>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => removeValue(index)}
                className="text-red-500 hover:text-red-700 rounded-lg"
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
            className="flex-grow rounded-lg"
          />
          <Button onClick={addValue} variant="outline" className="rounded-lg">
            Add Value
          </Button>
        </div>
      </div>

      <div className="card">
        <Label htmlFor="audience" className="text-lg font-semibold mb-2 block">
          Target Audience
        </Label>
        <p className="description">
          Describe your ideal user. Who are they and what are their needs?
        </p>
        <Textarea
          id="audience"
          value={formData.audience}
          onChange={(e) => handleInputChange('audience', e.target.value)}
          placeholder="e.g., Freelancers aged 25-45, comfortable with web apps"
          rows={4}
          className="rounded-lg"
        />
      </div>

      <Button onClick={handleSave} className="rounded-lg">
        Save Branding
      </Button>
    </section>
  );
};

export default BrandingSection;