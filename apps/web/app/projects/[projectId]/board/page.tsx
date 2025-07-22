'use client';

import React, { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { motion } from 'framer-motion';
import {
  DndContext,
  closestCorners,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
} from '@dnd-kit/core';
import {
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
  useSortable,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

interface Story {
  id: string;
  title: string;
  status: string;
  epic_id: string;
  epic_title: string;
}

interface Epic {
  id: string;
  title: string;
  stories: Story[];
}

interface Column {
  name: string;
  stories: Story[];
}

interface SortableItemProps {
  story: Story;
}

const SortableItem: React.FC<SortableItemProps> = ({ story }) => {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({ id: story.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    zIndex: isDragging ? 10 : 0,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <motion.div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className="bg-[#2A2A2A] p-3 rounded-md shadow-sm cursor-grab mb-2"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2 }}
    >
      <p className="font-normal">{story.title}</p>
    </motion.div>
  );
};

interface ColumnProps {
  column: Column;
  epics: Epic[];
}

const KanbanColumn: React.FC<ColumnProps> = ({ column, epics }) => {
  return (
    <motion.div
      key={column.name}
      className="flex-shrink-0 w-80 bg-[#1F1F1F] rounded-lg shadow-md p-4"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <h2 className="text-xl font-semibold mb-4 border-b border-gray-700 pb-2">{column.name}</h2>
      <SortableContext items={column.stories.map(story => story.id)} strategy={verticalListSortingStrategy}>
        <div className="space-y-3">
          {epics.map((epic) => (
            <div key={epic.id}>
              <h3 className="text-lg font-medium text-gray-400 mb-2">{epic.title}</h3>
              {column.stories
                .filter(story => story.epic_id === epic.id)
                .map((story) => (
                  <SortableItem key={story.id} story={story} />
                ))}
            </div>
          ))}
        </div>
      </SortableContext>
    </motion.div>
  );
};

const KanbanBoardPage: React.FC = () => {
  const params = useParams();
  const projectId = params.projectId as string;
  const [epics, setEpics] = useState<Epic[]>([]);
  const [columns, setColumns] = useState<Column[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  useEffect(() => {
    const fetchBoardData = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/projects/${projectId}/board`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        setEpics(data.epics);

        const fetchedColumns: Column[] = [
          { name: "To Do", stories: data.columns["To Do"] || [] },
          { name: "In Progress", stories: data.columns["In Progress"] || [] },
          { name: "Done", stories: data.columns["Done"] || [] },
        ];
        setColumns(fetchedColumns);

      } catch (e: any) {
        setError(e.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchBoardData();
  }, [projectId]);

  const handleDragEnd = async (event: DragEndEvent) => {
    const { active, over } = event;

    if (!over) return;

    const activeStoryId = active.id as string;
    const newColumnName = over.id as string; // Assuming column ID is its name

    // Find the story that was dragged
    let draggedStory: Story | undefined;
    setColumns(prevColumns => {
      const newCols = prevColumns.map(col => {
        const storyIndex = col.stories.findIndex(s => s.id === activeStoryId);
        if (storyIndex > -1) {
          draggedStory = col.stories[storyIndex];
          const updatedStories = [...col.stories];
          updatedStories.splice(storyIndex, 1);
          return { ...col, stories: updatedStories };
        }
        return col;
      });

      // Add the story to the new column
      if (draggedStory) {
        return newCols.map(col => {
          if (col.name === newColumnName) {
            return { ...col, stories: [...col.stories, { ...draggedStory!, status: newColumnName }] };
          }
          return col;
        });
      }
      return newCols;
    });

    if (draggedStory && draggedStory.status !== newColumnName) {
      try {
        const response = await fetch(`http://localhost:8000/api/stories/${activeStoryId}/status`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ new_status: newColumnName }),
        });

        if (!response.ok) {
          // If API call fails, revert the UI change
          console.error("Failed to update story status on backend.");
          // Re-fetch data to revert to actual state or implement more sophisticated rollback
          const fetchBoardData = async () => {
            try {
              const response = await fetch(`http://localhost:8000/api/projects/${projectId}/board`);
              if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
              }
              const data = await response.json();
              setEpics(data.epics);
              const fetchedColumns: Column[] = [
                { name: "To Do", stories: data.columns["To Do"] || [] },
                { name: "In Progress", stories: data.columns["In Progress"] || [] },
                { name: "Done", stories: data.columns["Done"] || [] },
              ];
              setColumns(fetchedColumns);
            } catch (e: any) {
              setError(e.message);
            }
          };
          fetchBoardData();
        }
      } catch (e) {
        console.error("Network error during status update:", e);
        // Revert UI on network error as well
        const fetchBoardData = async () => {
          try {
            const response = await fetch(`http://localhost:8000/api/projects/${projectId}/board`);
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setEpics(data.epics);
            const fetchedColumns: Column[] = [
              { name: "To Do", stories: data.columns["To Do"] || [] },
              { name: "In Progress", stories: data.columns["In Progress"] || [] },
              { name: "Done", stories: data.columns["Done"] || [] },
            ];
            setColumns(fetchedColumns);
          } catch (e: any) {
            setError(e.message);
          }
        };
        fetchBoardData();
      }
    }
  };

  if (isLoading) {
    return <div className="flex justify-center items-center h-screen text-white">Loading Kanban Board...</div>;
  }

  if (error) {
    return <div className="flex justify-center items-center h-screen text-red-500">Error: {error}</div>;
  }

  return (
    <div className="p-4 bg-[#141313] min-h-screen text-white">
      <h1 className="text-3xl font-bold mb-6">Project Kanban Board - {projectId}</h1>
      <DndContext sensors={sensors} collisionDetection={closestCorners} onDragEnd={handleDragEnd}>
        <div className="flex space-x-4 overflow-x-auto">
          {columns.map((column) => (
            <KanbanColumn key={column.name} column={column} epics={epics} />
          ))}
        </div>
      </DndContext>
    </div>
  );
};

export default KanbanBoardPage;