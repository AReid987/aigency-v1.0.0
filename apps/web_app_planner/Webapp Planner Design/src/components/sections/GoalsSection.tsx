import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card } from '@/components/ui/card';
import { Label } from '@/components/ui/label';

interface GoalsData {
  problem: string;
  audience: string;
  mvp: string;
  outcomes: string;
}

interface GoalsSectionProps {
  data: GoalsData;
  onSave: (data: GoalsData) => void;
}

const GoalsSection: React.FC<GoalsSectionProps> = ({ data, onSave }) => {
  const [formData, setFormData] = useState<GoalsData>(data);

  const handleInputChange = (field: keyof GoalsData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = () => {
    onSave(formData);
  };

  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-6">Define Clear Goals and Objectives</h1>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
          With your brand in mind, clearly define what your app aims to achieve.
        </p>
      </div>

      <Card className="p-6">
        <Label htmlFor="problem" className="text-sm font-medium mb-2 block">
          What problem is the app solving?
        </Label>
        <Textarea
          id="problem"
          value={formData.problem}
          onChange={(e) => handleInputChange('problem', e.target.value)}
          placeholder="e.g., Helping users find local events easily."
          rows={3}
        />
      </Card>

      <Card className="p-6">
        <Label htmlFor="audience" className="text-sm font-medium mb-2 block">
          Who is the target audience? (Refine from Branding)
        </Label>
        <Textarea
          id="audience"
          value={formData.audience}
          onChange={(e) => handleInputChange('audience', e.target.value)}
          placeholder="e.g., Young adults aged 18-30 interested in local activities."
          rows={3}
        />
      </Card>

      <Card className="p-6">
        <Label htmlFor="mvp" className="text-sm font-medium mb-2 block">
          What are the core functionalities (MVP)?
        </Label>
        <Textarea
          id="mvp"
          value={formData.mvp}
          onChange={(e) => handleInputChange('mvp', e.target.value)}
          placeholder="e.g., Event search, event details view, user registration."
          rows={3}
        />
      </Card>

      <Card className="p-6">
        <Label htmlFor="outcomes" className="text-sm font-medium mb-2 block">
          What are the desired outcomes?
        </Label>
        <Textarea
          id="outcomes"
          value={formData.outcomes}
          onChange={(e) => handleInputChange('outcomes', e.target.value)}
          placeholder="e.g., Increased user engagement, 1000 sign-ups in first 3 months."
          rows={3}
        />
      </Card>

      <Button onClick={handleSave} className="bg-indigo-600 hover:bg-indigo-700">
        Save Goals
      </Button>
    </section>
  );
};

export default GoalsSection;