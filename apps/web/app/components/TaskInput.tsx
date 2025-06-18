import { useState } from "react";

interface TaskInputProps {
  onSubmit: (task: {
    title: string;
    description: string;
    complexity: number;
  }) => void;
}

export default function TaskInput({ onSubmit }: TaskInputProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [complexity, setComplexity] = useState(0);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ title, description, complexity });
    setTitle("");
    setDescription("");
    setComplexity(0);
  };

  return (
    <div className="task-input" data-oid="gm6dm9n">
      <h3 data-oid="6c1v:c_">Create New Task</h3>
      <form onSubmit={handleSubmit} data-oid="x5xw2tf">
        <div className="form-group" data-oid="ymwm3_6">
          <label htmlFor="title" data-oid="knwao:k">
            Title
          </label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter task title"
            required
            data-oid="_k_7fd0"
          />
        </div>
        <div className="form-group" data-oid="orlr3rn">
          <label htmlFor="description" data-oid="3i167pd">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Enter task description"
            className="w-full p-2 border rounded-md min-h-[100px]"
            data-oid="4meebm:"
          />
        </div>
        <div className="form-group" data-oid="uo5s_1w">
          <label htmlFor="complexity" data-oid="_mh9196">
            Complexity
          </label>
          <input
            id="complexity"
            type="number"
            value={complexity}
            onChange={(e) => setComplexity(Number(e.target.value))}
            min="0"
            required
            data-oid="0sd0t3i"
          />
        </div>
        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 mt-2"
          data-oid="cljkbma"
        >
          Create Task
        </button>
      </form>
    </div>
  );
}
