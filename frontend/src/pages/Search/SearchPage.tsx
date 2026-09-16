import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Search as SearchIcon } from 'lucide-react'
import { searchDocuments, type SearchResponse } from '../../api/client'

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [currentQuery, setCurrentQuery] = useState('')

  const searchQuery = useQuery<SearchResponse, Error>({
    queryKey: ['search', currentQuery],
    queryFn: () => searchDocuments(currentQuery),
    enabled: currentQuery.length > 0,
    staleTime: 1000 * 60 * 2,
    retry: false,
  })

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-6 shadow-2xl shadow-black/20">
        <h1 className="text-2xl font-semibold text-white">Semantic search</h1>
        <p className="mt-2 text-sm text-slate-400">Search across your documents with hybrid retrieval and similarity scoring.</p>
        <div className="mt-4 flex flex-col gap-3 sm:flex-row">
          <label className="flex-1 rounded-2xl border border-white/10 bg-slate-950/70 p-2">
            <div className="flex items-center gap-2">
              <SearchIcon className="text-slate-400" size={18} />
              <input
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Search your knowledge base..."
                className="w-full bg-transparent px-3 py-2 text-sm text-white outline-none"
              />
            </div>
          </label>
          <button
            type="button"
            onClick={() => setCurrentQuery(query.trim())}
            disabled={!query.trim() || searchQuery.isLoading}
            className="rounded-2xl bg-brand-500 px-5 py-3 text-sm font-semibold text-white transition hover:bg-brand-600 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {searchQuery.isLoading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </div>

      <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-6 shadow-2xl shadow-black/20">
        {searchQuery.isError && (
          <div className="rounded-2xl border border-rose-500/20 bg-rose-500/10 p-4 text-sm text-rose-200">
            Could not fetch search results. Please try again.
          </div>
        )}

        {!currentQuery && <p className="text-sm text-slate-400">Enter a query to search your knowledge base.</p>}

        {searchQuery.status === 'pending' && <p className="text-sm text-slate-400">Loading results...</p>}

        {searchQuery.data && (
          <div className="space-y-4">
            {searchQuery.data.results.length === 0 ? (
              <p className="text-sm text-slate-400">No relevant documents were found for this query.</p>
            ) : (
              searchQuery.data.results.map((result, idx) => (
                <div key={`${result.source}-${idx}`} className="rounded-3xl border border-white/10 bg-slate-950/80 p-5">
                  <div className="flex items-center justify-between gap-4 text-sm text-slate-400">
                    <span>Source: {result.source}</span>
                    <span>Score: {result.score.toFixed(3)}</span>
                  </div>
                  <p className="mt-3 text-sm leading-7 text-slate-200">{result.text}</p>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  )
}
