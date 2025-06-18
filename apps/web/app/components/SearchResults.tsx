import { SearchResult } from "../../types";

interface SearchResultsProps {
  results: SearchResult[];
}

export default function SearchResults({ results }: SearchResultsProps) {
  return (
    <div className="space-y-4" data-oid="_07r8pp">
      {results.map((result) => (
        <div
          key={result.url}
          className="p-4 border rounded-md"
          data-oid="lonix8n"
        >
          <a
            href={result.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline"
            data-oid="3bv5u65"
          >
            <h3 className="font-semibold" data-oid="vf0qm3i">
              {result.title}
            </h3>
          </a>
          <p className="text-sm text-gray-600" data-oid="_xbh_18">
            {result.snippet}
          </p>
        </div>
      ))}
    </div>
  );
}
