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
    <div className="task-input" data-oid="talw37t">
      <h3 data-oid="2mdp-81">Create New Task</h3>
      <form onSubmit={handleSubmit} data-oid="gxcgfa_">
        <div className="form-group" data-oid="9v:eeu.">
          <label htmlFor="title" data-oid=".dtmq1g">
            Title
          </label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter task title"
            required
            data-oid="ma411q6"
          />
        </div>
        <div className="form-group" data-oid="ox6h_em">
          <label htmlFor="description" data-oid="s10e:3n">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Enter task description"
            className="w-full p-2 border rounded-md min-h-[100px]"
            data-oid="dh9sqr0"
          />
        </div>
        <div className="form-group" data-oid="l:3pa9k">
          <label htmlFor="complexity" data-oid="cvk.dsy">
            Complexity
          </label>
          <input
            id="complexity"
            type="number"
            value={complexity}
            onChange={(e) => setComplexity(Number(e.target.value))}
            min="0"
            required
            data-oid="_j0ocf5"
          />
        </div>
        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 mt-2"
          data-oid="k0o9ffc"
        >
          Create Task
        </button>
      </form>
    </div>
  );
}
