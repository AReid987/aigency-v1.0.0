import React from "react";
import { CanvasMode } from "../types";

interface ToolbarProps {
  mode: CanvasMode;
  onModeChange: (mode: CanvasMode) => void;
  enableAI?: boolean;
}

const modes: { label: string; value: CanvasMode; icon: string }[] = [
  {
    label: "ArchVision",
    value: "archvision",
    icon: "🏗️",
  },
  {
    label: "BrainCraft",
    value: "braincraft",
    icon: "🧠",
  },
  {
    label: "Hybrid",
    value: "hybrid",
    icon: "🔄",
  },
];

const tools = [
  { id: "select", label: "Select", icon: "👆" },
  { id: "pan", label: "Pan", icon: "✋" },
  { id: "draw", label: "Draw", icon: "✏️" },
  { id: "connect", label: "Connect", icon: "🔗" },
  { id: "delete", label: "Delete", icon: "🗑️" },
];

export const Toolbar: React.FC<ToolbarProps> = ({
  mode,
  onModeChange,
  enableAI = true,
}) => {
  return (
    <div
      className="w-16 bg-white border-r border-gray-200 flex flex-col items-center py-4 gap-4"
      data-oid="-575-o."
    >
      {/* Mode Selector */}
      <div className="flex flex-col gap-2" data-oid="xiz1omw">
        {modes.map(({ label, value, icon }) => (
          <button
            key={value}
            className={`w-12 h-12 rounded-lg flex items-center justify-center ${
              mode === value
                ? "bg-blue-500 text-white"
                : "bg-gray-100 hover:bg-gray-200"
            }`}
            onClick={() => onModeChange(value)}
            title={label}
            data-oid="b8kg24s"
          >
            <span role="img" aria-label={label} data-oid="icv_c_:">
              {icon}
            </span>
          </button>
        ))}
      </div>

      <div className="w-full h-px bg-gray-200 my-2" data-oid="_r_.lls" />

      {/* Tools */}
      <div className="flex flex-col gap-2" data-oid="eurmkd.">
        {tools.map(({ id, label, icon }) => (
          <button
            key={id}
            className="w-12 h-12 rounded-lg bg-gray-100 hover:bg-gray-200 flex items-center justify-center"
            title={label}
            data-oid="ymroec3"
          >
            <span role="img" aria-label={label} data-oid="_xurs_e">
              {icon}
            </span>
          </button>
        ))}
      </div>

      {/* AI Toggle */}
      {enableAI && (
        <>
          <div className="w-full h-px bg-gray-200 my-2" data-oid="dad9wg." />
          <button
            className="w-12 h-12 rounded-lg bg-purple-100 hover:bg-purple-200 flex items-center justify-center"
            title="AI Assistant"
            data-oid="5a:ck9g"
          >
            <span role="img" aria-label="AI" data-oid="7iwsnyv">
              🤖
            </span>
          </button>
        </>
      )}
    </div>
  );
};

export default Toolbar;
