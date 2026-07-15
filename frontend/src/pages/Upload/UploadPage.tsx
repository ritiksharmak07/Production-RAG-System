import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { FileUp, UploadCloud } from 'lucide-react'
import { uploadFiles, type UploadResponse } from '../../api/client'
import { useNotifications } from '../../hooks/useNotifications'
import NotificationPanel from '../../components/NotificationPanel'

export default function UploadPage() {
  const [selectedFiles, setSelectedFiles] = useState<FileList | null>(null)
  const { notifications, pushNotification } = useNotifications()

  const mutation = useMutation<UploadResponse, Error, FileList>({
    mutationFn: (files) => uploadFiles(files),
    onSuccess: (data) => {
      pushNotification('Upload complete. Documents are being ingested.', 'success')
      setSelectedFiles(null)
      console.log('Ingested documents:', data.ingested_documents)
    },
    onError: (error) => {
      const message = error instanceof Error ? error.message : 'Upload failed.'
      pushNotification(message, 'error')
    },
  })

  const handleUpload = () => {
    if (!selectedFiles || selectedFiles.length === 0) {
      pushNotification('Select at least one file to upload.', 'error')
      return
    }
    mutation.mutate(selectedFiles)
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-6 shadow-2xl shadow-black/20">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-white">Upload documents</h1>
            <p className="mt-2 text-sm text-slate-400">Support for PDFs, DOCX, TXT, and CSV files is wired into the backend ingestion pipeline.</p>
          </div>
          <button
            type="button"
            onClick={handleUpload}
            className="rounded-2xl bg-brand-500 px-5 py-3 text-sm font-semibold text-white transition hover:bg-brand-600 disabled:cursor-not-allowed disabled:opacity-50"
            disabled={mutation.isPending}
          >
            {mutation.isPending ? 'Uploading...' : 'Upload Files'}
          </button>
        </div>

        <label className="mt-6 flex cursor-pointer flex-col items-center justify-center rounded-3xl border border-dashed border-brand-500/30 bg-brand-500/10 p-10 text-center transition hover:bg-brand-500/20">
          <UploadCloud size={28} className="text-brand-400" />
          <span className="mt-3 font-medium text-white">Drop files here or click to browse</span>
          <span className="mt-2 text-sm text-slate-400">PDF • DOCX • TXT • CSV</span>
          <input type="file" multiple className="hidden" onChange={(event) => setSelectedFiles(event.target.files)} />
        </label>

        {selectedFiles && (
          <div className="mt-6 space-y-2">
            {Array.from(selectedFiles).map((file) => (
              <div key={file.name} className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-slate-200">
                <FileUp size={16} className="text-brand-400" />
                {file.name}
              </div>
            ))}
          </div>
        )}

        {mutation.isError && (
          <div className="mt-4 rounded-2xl border border-rose-500/20 bg-rose-500/10 p-4 text-sm text-rose-200">
            {mutation.error instanceof Error ? mutation.error.message : 'Upload failed.'}
          </div>
        )}
      </div>

      <div className="rounded-3xl border border-white/10 bg-slate-900/70 p-6 text-sm text-slate-400">
        <p>Uploads are validated and ingested to the backend pipeline. You can monitor progress in the notification feed.</p>
      </div>

      <NotificationPanel notifications={notifications} />
    </div>
  )
}
