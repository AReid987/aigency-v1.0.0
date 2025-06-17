import { Progress } from "@repo/ui/progress";

interface ProgressTrackerProps {
  progress: number;
}

export function ProgressTracker({ progress }: ProgressTrackerProps) {
  return (
    <div className="space-y-2" data-oid="l0v-hol">
      <div className="flex justify-between" data-oid="a0xxuvs">
        <span className="text-sm font-medium" data-oid="ekavppt">
          Project Progress
        </span>
        <span className="text-sm text-gray-500" data-oid="8o9xvhp">
          {progress}%
        </span>
      </div>
      <Progress value={progress} className="h-2" data-oid="vp3ze16" />
    </div>
  );
}
