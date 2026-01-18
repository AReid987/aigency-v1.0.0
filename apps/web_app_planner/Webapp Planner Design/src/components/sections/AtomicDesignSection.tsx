import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Card } from '@/components/ui/card';
import { Label } from '@/components/ui/label';

interface AtomicDesignData {
  colorPrimary: string;
  colorSecondary: string;
  colorAccent: string;
  neutralPalette: string;
  colorSuccess: string;
  colorError: string;
  colorWarning: string;
  colorInfo: string;
  fontHeading: string;
  fontBody: string;
  iconography: string;
  typeScale: string;
  colorScale: string;
  molecules: string;
  organisms: string;
  templates: string;
  pages: string;
}

interface AtomicDesignSectionProps {
  data: AtomicDesignData;
  onSave: (data: AtomicDesignData) => void;
}

const AtomicDesignSection: React.FC<AtomicDesignSectionProps> = ({ data, onSave }) => {
  const [formData, setFormData] = useState<AtomicDesignData>(data);

  const handleInputChange = (field: keyof AtomicDesignData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = () => {
    onSave(formData);
  };

  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-6">Develop Your Atomic Design System</h1>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
          An Atomic Design System helps you build UIs consistently and efficiently.
        </p>
      </div>

      <Card className="p-6">
        <h2 className="text-2xl font-semibold mb-4">A. Atoms: Core Brand & UI Elements</h2>
        
        <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-md mb-4">
          <Label className="text-lg font-semibold mb-2 block">Brand Color Palette</Label>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
            Define your primary, secondary, and accent colors using hex codes.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <Label htmlFor="colorPrimary">Primary Color</Label>
              <Input
                id="colorPrimary"
                value={formData.colorPrimary}
                onChange={(e) => handleInputChange('colorPrimary', e.target.value)}
                placeholder="#RRGGBB"
              />
            </div>
            <div>
              <Label htmlFor="colorSecondary">Secondary Color</Label>
              <Input
                id="colorSecondary"
                value={formData.colorSecondary}
                onChange={(e) => handleInputChange('colorSecondary', e.target.value)}
                placeholder="#RRGGBB"
              />
            </div>
            <div>
              <Label htmlFor="colorAccent">Accent Color</Label>
              <Input
                id="colorAccent"
                value={formData.colorAccent}
                onChange={(e) => handleInputChange('colorAccent', e.target.value)}
                placeholder="#RRGGBB"
              />
            </div>
          </div>
        </div>

        <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-md mb-4">
          <Label htmlFor="neutralPalette" className="text-lg font-semibold mb-2 block">
            Neutral Color Palette
          </Label>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
            Define grays, off-whites, and dark shades for backgrounds and text.
          </p>
          <Textarea
            id="neutralPalette"
            value={formData.neutralPalette}
            onChange={(e) => handleInputChange('neutralPalette', e.target.value)}
            placeholder="e.g., Light Gray: #F3F4F6, Medium Gray: #9CA3AF..."
            rows={3}
          />
        </div>

        <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-md mb-4">
          <Label className="text-lg font-semibold mb-2 block">Semantic Colors</Label>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
            Colors for success, error, warning, and information states.
          </p>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <Label htmlFor="colorSuccess">Success</Label>
              <Input
                id="colorSuccess"
                value={formData.colorSuccess}
                onChange={(e) => handleInputChange('colorSuccess', e.target.value)}
                placeholder="#RRGGBB"
              />
            </div>
            <div>
              <Label htmlFor="colorError">Error</Label>
              <Input
                id="colorError"
                value={formData.colorError}
                onChange={(e) => handleInputChange('colorError', e.target.value)}
                placeholder="#RRGGBB"
              />
            </div>
            <div>
              <Label htmlFor="colorWarning">Warning</Label>
              <Input
                id="colorWarning"
                value={formData.colorWarning}
                onChange={(e) => handleInputChange('colorWarning', e.target.value)}
                placeholder="#RRGGBB"
              />
            </div>
            <div>
              <Label htmlFor="colorInfo">Info</Label>
              <Input
                id="colorInfo"
                value={formData.colorInfo}
                onChange={(e) => handleInputChange('colorInfo', e.target.value)}
                placeholder="#RRGGBB"
              />
            </div>
          </div>
        </div>

        <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-md mb-4">
          <Label className="text-lg font-semibold mb-2 block">Typography</Label>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
            Choose font families that align with your brand personality.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label htmlFor="fontHeading">Heading Font Family</Label>
              <Input
                id="fontHeading"
                value={formData.fontHeading}
                onChange={(e) => handleInputChange('fontHeading', e.target.value)}
                placeholder="e.g., Montserrat"
              />
            </div>
            <div>
              <Label htmlFor="fontBody">Body Font Family</Label>
              <Input
                id="fontBody"
                value={formData.fontBody}
                onChange={(e) => handleInputChange('fontBody', e.target.value)}
                placeholder="e.g., Open Sans"
              />
            </div>
          </div>
        </div>
      </Card>

      <Card className="p-6">
        <h2 className="text-2xl font-semibold mb-4">B. Molecules: Simple UI Groups</h2>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
          Groups of atoms forming simple, reusable UI components.
        </p>
        <Textarea
          value={formData.molecules}
          onChange={(e) => handleInputChange('molecules', e.target.value)}
          placeholder="List key molecules, e.g., Search input with button, User avatar with name..."
          rows={4}
        />
      </Card>

      <Card className="p-6">
        <h2 className="text-2xl font-semibold mb-4">C. Organisms: Complex UI Sections</h2>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
          Complex UI components made up of groups of molecules and atoms.
        </p>
        <Textarea
          value={formData.organisms}
          onChange={(e) => handleInputChange('organisms', e.target.value)}
          placeholder="List key organisms, e.g., Header, Footer, Product Card..."
          rows={4}
        />
      </Card>

      <Button onClick={handleSave} className="bg-indigo-600 hover:bg-indigo-700">
        Save Atomic Design System
      </Button>
    </section>
  );
};

export default AtomicDesignSection;