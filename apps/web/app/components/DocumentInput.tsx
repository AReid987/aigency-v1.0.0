import { useState } from "react";

interface DocumentInputProps {
  documentType: "PRD" | "FRD" | "ERD" | "DRD";
  onSubmit: (content: string) => void;
}

export default function DocumentInput({
  documentType,
  onSubmit,
}: DocumentInputProps) {
  const [content, setContent] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(content);
    setContent("");
  };

  return (
    <div className="document-input" data-oid="ar06::h">
      <h3 data-oid=":2h.imw">{documentType} Document Input</h3>
      <form onSubmit={handleSubmit} data-oid="xixhq6_">
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder={`Enter ${documentType} content...`}
          className="w-full p-2 border rounded-md min-h-[200px]"
          required
          data-oid="2upq0vl"
        />

        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 mt-2"
          data-oid="1cfqvag"
        >
          Submit {documentType}
        </button>
      </form>
    </div>
  );
}
