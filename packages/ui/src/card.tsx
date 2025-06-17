import { type JSX } from "react";

export function Card({
  className,
  title,
  children,
  href,
}: {
  className?: string;
  title: string;
  children: React.ReactNode;
  href: string;
}): JSX.Element {
  return (
    <a
      className={className}
      href={`${href}?utm_source=create-turbo&utm_medium=basic&utm_campaign=create-turbo"`}
      rel="noopener noreferrer"
      target="_blank"
      data-oid="nu:5_7g"
    >
      <h2 data-oid="utdbyab">
        {title} <span data-oid="mulln66">-&gt;</span>
      </h2>
      <p data-oid="f6lsbhb">{children}</p>
    </a>
  );
}
