import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

interface DataPoint {
  id: string;
  name: string;
  type: string;
  description: string;
}

interface DataPointsSectionProps {
  data: DataPoint[];
  onSave: (data: DataPoint[]) => void;
}

const DataPointsSection: React.FC<DataPointsSectionProps> = ({ data, onSave }) => {
  const [dataPoints, setDataPoints] = useState<DataPoint[]>(data);
  const [newDataPoint, setNewDataPoint] = useState({
    name: '',
    type: 'String',
    description: ''
  });

  const dataTypes = ['String', 'Number', 'Boolean', 'Array', 'Object', 'Timestamp'];

  const addDataPoint = () => {
    if (newDataPoint.name.trim()) {
      const dataPoint: DataPoint = {
        id: crypto.randomUUID(),
        name: newDataPoint.name.trim(),
        type: newDataPoint.type,
        description: newDataPoint.description.trim()
      };
      const updatedDataPoints = [...dataPoints, dataPoint];
      setDataPoints(updatedDataPoints);
      onSave(updatedDataPoints);
      setNewDataPoint({ name: '', type: 'String', description: '' });
    }
  };

  const removeDataPoint = (id: string) => {
    const updatedDataPoints = dataPoints.filter(dp => dp.id !== id);
    setDataPoints(updatedDataPoints);
    onSave(updatedDataPoints);
  };

  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-6">Identify Key Data Points</h1>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
          What information will your app need to store and manage? List the key pieces of data.
        </p>
      </div>

      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Add New Data Point</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <Label htmlFor="dataPointName">Data Point Name</Label>
            <Input
              id="dataPointName"
              value={newDataPoint.name}
              onChange={(e) => setNewDataPoint(prev => ({ ...prev, name: e.target.value }))}
              placeholder="e.g., UserEmail"
            />
          </div>
          <div>
            <Label htmlFor="dataPointType">Data Type</Label>
            <Select
              value={newDataPoint.type}
              onValueChange={(value) => setNewDataPoint(prev => ({ ...prev, type: value }))}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {dataTypes.map((type) => (
                  <SelectItem key={type} value={type}>
                    {type}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="dataPointDescription">Description/Purpose</Label>
            <Input
              id="dataPointDescription"
              value={newDataPoint.description}
              onChange={(e) => setNewDataPoint(prev => ({ ...prev, description: e.target.value }))}
              placeholder="e.g., Stores user's email for login"
            />
          </div>
        </div>
        <Button onClick={addDataPoint} className="bg-indigo-600 hover:bg-indigo-700">
          Add Data Point
        </Button>
      </Card>

      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Your Data Points</h2>
        <div className="space-y-3">
          {dataPoints.length === 0 ? (
            <p className="text-gray-500 dark:text-gray-400 italic">No data points added yet.</p>
          ) : (
            dataPoints.map((dataPoint) => (
              <div key={dataPoint.id} className="bg-gray-50 dark:bg-gray-700 p-4 rounded-md border">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h3 className="font-semibold text-indigo-700 dark:text-indigo-400 mb-1">
                      {dataPoint.name}
                      <span className="ml-2 text-xs bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-300 px-2 py-0.5 rounded-full">
                        {dataPoint.type}
                      </span>
                    </h3>
                    {dataPoint.description && (
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {dataPoint.description}
                      </p>
                    )}
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => removeDataPoint(dataPoint.id)}
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

export default DataPointsSection;