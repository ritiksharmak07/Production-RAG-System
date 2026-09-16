import { useState } from 'react'
import { motion } from 'framer-motion'
import { Send, Sparkles } from 'lucide-react'
import { useMutation } from '@tanstack/react-query'
import { askQuestion, type AskResponse } from '../../api/client'

const starterMessages = [
  'Summarize the key points from the uploaded documents.',
  'What are the most important findings?',
  'Show me the sources for this answer.',
]

export default function ChatPage() {
  const [messages, setMessages] = useState<Array<{ role: 'assistant' | 'user'; content: string; sources?: string[] }>>([
    { role: 'assistant', content: 'Hello! I can answer questions from your uploaded documents. Try asking something grounded in your knowledge base.' },
  ])
  const [draft, setDraft] = useState('')

  const mutation = useMutation<AskResponse, Error, string>({
    mutationFn: (query) => askQuestion(query, 5),
    onSuccess: (response, query) => {
      setMessages((prev) => [
        ...prev,
        { role: 'user', content: query },
        { role: 'assistant', content: response.answer, sources: response.sources },
      ])
    },
  })

  const sendMessage = () => {
    const trimmed = draft.trim()
    if (!trimmed) return

    setMessages((prev) => [...prev, { role: 'user', content: trimmed }])
    setDraft('')
    mutation.mutate(trimmed)
  }

  return (
    <div className="flex h-[80vh] flex-col rounded-3xl border border-white/10 bg-slate-900/70 p-4 shadow-2xl shadow-black/20">
      <div className="flex items-center gap-3 border-b border-white/10 pb-4">
        <div className="rounded-2xl bg-brand-500/15 p-2 text-brand-400">
          <Sparkles size={18} />
        </div>
        <div>
          <h2 className="font-semibold text-white">Document chat</h2>
          <p className="text-sm text-slate-400">Ask questions and receive grounded answers.</p>
        </div>
      </div>

      <div className="mt-4 flex-1 space-y-3 overflow-auto pr-2">
        {messages.map((message, index) => (
          <motion.div key={`${message.role}-${index}`} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} className={`rounded-2xl px-4 py-3 ${message.role === 'user' ? 'ml-10 bg-brand-600/20 text-slate-100' : 'mr-10 bg-white/5 text-slate-200'}`}>
            <div>{message.content}</div>
            {message.sources && (
              <div className="mt-3 rounded-2xl border border-slate-700 bg-slate-950/70 px-3 py-2 text-xs text-slate-400">
                <div className="mb-2 text-[11px] uppercase tracking-[0.24em] text-slate-500">Sources</div>
                <ul className="space-y-1">
                  {message.sources.map((source) => (
                    <li key={source} className="truncate">• {source}</li>
                  ))}
                </ul>
              </div>
            )}
          </motion.div>
        ))}

        {mutation.isPending && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="rounded-2xl bg-slate-800/80 px-4 py-3 text-sm text-slate-400">
            Generating answer...
          </motion.div>
        )}

        {mutation.isError && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="rounded-2xl bg-rose-500/10 px-4 py-3 text-sm text-rose-200">
            <div className="font-semibold">Backend error</div>
            <div>{mutation.error instanceof Error ? mutation.error.message : 'Failed to generate an answer.'}</div>
          </motion.div>
        )}
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        {starterMessages.map((message) => (
          <button key={message} onClick={() => setDraft(message)} className="rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-sm text-slate-300 transition hover:bg-white/10">
            {message}
          </button>
        ))}
      </div>

      <div className="mt-4 flex gap-2 rounded-2xl border border-white/10 bg-slate-950/70 p-2">
        <input
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          onKeyDown={(event) => event.key === 'Enter' && sendMessage()}
          placeholder="Ask about your documents..."
          className="flex-1 bg-transparent px-3 py-2 text-sm text-white outline-none"
          disabled={mutation.isPending}
        />
        <button onClick={sendMessage} disabled={mutation.isPending} className="rounded-xl bg-brand-500 p-2 text-white transition hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-50">
          <Send size={18} />
        </button>
      </div>
    </div>
  )
}
