import { SearchResult } from "../../types";

interface SearchResultsProps {
  results: SearchResult[];
}

export default function SearchResults({ results }: SearchResultsProps) {
  return (
    <div className="space-y-4" data-oid="ke6:qcb">
      {results.map((result) => (
        <div
          key={result.url}
          className="p-4 border rounded-md"
          data-oid="esu8f_o"
        >
          <a
            href={result.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline"
            data-oid="q43f99l"
          >
            <h3 className="font-semibold" data-oid="05j6ura">
              {result.title}
            </h3>
          </a>
          <p className="text-sm text-gray-600" data-oid=":26ei3e">
            {result.snippet}
          </p>
        </div>
      ))}
    </div>
  );
}
