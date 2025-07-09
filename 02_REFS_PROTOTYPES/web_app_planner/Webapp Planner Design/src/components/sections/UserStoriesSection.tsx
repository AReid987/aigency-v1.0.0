import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { Label } from '@/components/ui/label';

interface UserStory {
  id: string;
  userType: string;
  action: string;
  benefit: string;
}

interface UserStoriesSectionProps {
  data: UserStory[];
  onSave: (data: UserStory[]) => void;
}

const UserStoriesSection: React.FC<UserStoriesSectionProps> = ({ data, onSave }) => {
  const [stories, setStories] = useState<UserStory[]>(data);
  const [newStory, setNewStory] = useState({ userType: '', action: '', benefit: '' });

  const addStory = () => {
    if (newStory.userType && newStory.action && newStory.benefit) {
      const story: UserStory = {
        id: crypto.randomUUID(),
        ...newStory
      };
      const updatedStories = [...stories, story];
      setStories(updatedStories);
      onSave(updatedStories);
      setNewStory({ userType: '', action: '', benefit: '' });
    }
  };

  const removeStory = (id: string) => {
    const updatedStories = stories.filter(story => story.id !== id);
    setStories(updatedStories);
    onSave(updatedStories);
  };

  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold mb-6">Identify Key User Stories</h1>
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
          Translate your goals into user-centric actions. User stories help you understand features from the user's perspective.
        </p>
      </div>

      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Add New User Story</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <Label htmlFor="userType">As a...</Label>
            <Input
              id="userType"
              value={newStory.userType}
              onChange={(e) => setNewStory(prev => ({ ...prev, userType: e.target.value }))}
              placeholder="e.g., new user"
            />
          </div>
          <div>
            <Label htmlFor="action">I want to...</Label>
            <Input
              id="action"
              value={newStory.action}
              onChange={(e) => setNewStory(prev => ({ ...prev, action: e.target.value }))}
              placeholder="e.g., create an account"
            />
          </div>
          <div>
            <Label htmlFor="benefit">So that...</Label>
            <Input
              id="benefit"
              value={newStory.benefit}
              onChange={(e) => setNewStory(prev => ({ ...prev, benefit: e.target.value }))}
              placeholder="e.g., I can save my preferences"
            />
          </div>
        </div>
        <Button onClick={addStory} className="bg-indigo-600 hover:bg-indigo-700">
          Add User Story
        </Button>
      </Card>

      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Your User Stories</h2>
        <div className="space-y-3">
          {stories.length === 0 ? (
            <p className="text-gray-500 dark:text-gray-400 italic">No user stories added yet.</p>
          ) : (
            stories.map((story) => (
              <div key={story.id} className="bg-gray-50 dark:bg-gray-700 p-4 rounded-md border">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <p className="font-medium text-gray-800 dark:text-gray-200">
                      <strong>As a</strong> {story.userType}
                    </p>
                    <p className="text-gray-700 dark:text-gray-300">
                      <strong>I want to</strong> {story.action}
                    </p>
                    <p className="text-gray-600 dark:text-gray-400">
                      <strong>So that</strong> {story.benefit}
                    </p>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => removeStory(story.id)}
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

export default UserStoriesSection;