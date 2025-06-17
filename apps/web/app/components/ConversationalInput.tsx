import { useState } from "react";

export default function ConversationalInput({
  onSubmit,
}: {
  onSubmit: (input: string) => void;
}) {
  const [input, setInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(input);
    setInput("");
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4" data-oid="91fg21z">
      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Describe your product idea..."
        className="w-full p-2 border rounded-md min-h-[100px]"
        required
        data-oid="20ajq-q"
      />

      <button
        type="submit"
        className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
        data-oid="2l6:xys"
      >
        Submit Idea
      </button>
    </form>
  );
}
