
'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Loader2 } from 'lucide-react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

interface NewProjectModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (projectName: string) => void;
  isLoading: boolean;
}

const NewProjectModal: React.FC<NewProjectModalProps> = ({ isOpen, onClose, onSubmit, isLoading }): JSX.Element => {
  const [projectName, setProjectName] = useState('');

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (projectName.trim()) {
      onSubmit(projectName);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px] bg-[#1F1F1F] text-white border-gray-600">
        <DialogHeader>
          <DialogTitle className="text-white">Start New Project</DialogTitle>
          <DialogDescription className="text-gray-400">
            Give your new project a name.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <label htmlFor="projectName" className="text-right text-gray-300">
              Project Name
            </label>
            <Input
              id="projectName"
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              className="col-span-3 bg-[#141313] text-white border-gray-600"
              disabled={isLoading}
            />
          </div>
        </form>
        <DialogFooter>
          <Button variant="outline" onClick={onClose} disabled={isLoading} className="bg-gray-700 text-white border-gray-600 hover:bg-gray-600">
            Cancel
          </Button>
          <Button type="submit" onClick={handleSubmit} disabled={isLoading} className="bg-[#615EFF] text-white hover:bg-[#4E4AFF]">
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Creating...
              </>
            ) : (
              'Create Project'
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default NewProjectModal;
