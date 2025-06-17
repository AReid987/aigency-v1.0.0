import React from "react";
import { ViewType } from "../types";

interface ViewSelectorProps {
  currentView: ViewType;
  onViewChange: (view: ViewType) => void;
}

const views: { label: string; value: ViewType }[] = [
  { label: "2D", value: "2d" },
  { label: "3D", value: "3d" },
  { label: "ISO", value: "iso" },
];

export const ViewSelector: React.FC<ViewSelectorProps> = ({
  currentView,
  onViewChange,
}) => {
  return (
    <div className="flex gap-2 p-2 bg-white rounded shadow" data-oid="3z21a7j">
      {views.map(({ label, value }) => (
        <button
          key={value}
          className={`px-3 py-1 rounded ${
            currentView === value
              ? "bg-blue-500 text-white"
              : "bg-gray-100 hover:bg-gray-200"
          }`}
          onClick={() => onViewChange(value)}
          data-oid="o3tgvbu"
        >
          {label}
        </button>
      ))}
    </div>
  );
};

export default ViewSelector;
