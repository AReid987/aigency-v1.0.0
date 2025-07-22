import React from "react";
import { Progress } from "@repo/ui/progress";

interface ProgressTrackerProps {
  progress: number;
}

export function ProgressTracker({ progress }: ProgressTrackerProps) {
  return (
    <div className="space-y-2" data-oid="gyarsg2">
      <div className="flex justify-between" data-oid="tdrm27f">
        <span className="text-sm font-medium" data-oid="xs7a82x">
          Project Progress
        </span>
        <span className="text-sm text-gray-500" data-oid="g0u2rbs">
          {progress}%
        </span>
      </div>
      <Progress value={progress} className="h-2" data-oid="795h5y-" />
    </div>
  );
}
