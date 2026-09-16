import { motion } from 'framer-motion'
import { ArrowRight, Bot, FileUp, Search } from 'lucide-react'
import { Link } from 'react-router-dom'

const cards = [
  { title: 'Chat with documents', description: 'Ask grounded questions over your indexed corpus.', icon: Bot },
  { title: 'Semantic search', description: 'Find relevant content with hybrid retrieval.', icon: Search },
  { title: 'Upload knowledge', description: 'Ingest PDFs, DOCX, TXT, and CSV files with one click.', icon: FileUp },
]

export default function HomePage() {
  return (
    <div className="space-y-8">
      <motion.section initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="rounded-3xl border border-white/10 bg-slate-900/70 p-8 shadow-2xl shadow-black/20">
        <div className="max-w-2xl">
          <p className="mb-3 inline-flex items-center rounded-full border border-brand-500/30 bg-brand-500/10 px-3 py-1 text-sm text-brand-300">AI document assistant</p>
          <h1 className="text-4xl font-semibold tracking-tight text-white sm:text-5xl">Build grounded answers from your private documents.</h1>
          <p className="mt-4 text-lg text-slate-400">A modern RAG interface for uploading knowledge, searching it semantically, and chatting with your corpus in real time.</p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link to="/chat" className="inline-flex items-center gap-2 rounded-2xl bg-brand-500 px-4 py-3 font-medium text-white transition hover:bg-brand-700">Start chatting <ArrowRight size={18} /></Link>
            <Link to="/upload" className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 font-medium text-slate-200 transition hover:bg-white/10">Upload documents</Link>
          </div>
        </div>
      </motion.section>

      <div className="grid gap-4 md:grid-cols-3">
        {cards.map(({ title, description, icon: Icon }) => (
          <motion.div key={title} whileHover={{ y: -3 }} className="rounded-3xl border border-white/10 bg-slate-900/70 p-6">
            <div className="mb-4 inline-flex rounded-2xl bg-white/10 p-3 text-brand-400">
              <Icon size={20} />
            </div>
            <h2 className="text-lg font-semibold text-white">{title}</h2>
            <p className="mt-2 text-sm text-slate-400">{description}</p>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
