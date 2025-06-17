import { type JSX } from "react";

export function Code({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}): JSX.Element {
  return (
    <code className={className} data-oid="9s_zdl4">
      {children}
    </code>
  );
}
