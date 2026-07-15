import axios from 'axios'

export const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

export interface SearchResult {
  score: number
  text: string
  source: string
}

export interface SearchResponse {
  query: string
  results: SearchResult[]
}

export interface AskRequest {
  query: string
  top_k?: number
}

export interface AskResponse {
  query: string
  answer: string
  sources: string[]
}

export interface UploadResponse {
  message: string
  files: string[]
  ingested_documents: Array<Record<string, unknown>>
}

export async function searchDocuments(query: string, top_k = 5) {
  const response = await api.get<SearchResponse>('/search', {
    params: { query, top_k },
  })
  return response.data
}

export async function askQuestion(query: string, top_k = 5) {
  const response = await api.post<AskResponse>('/ask', { query, top_k })
  return response.data
}

export async function uploadFiles(files: FileList) {
  const formData = new FormData()
  Array.from(files).forEach((file) => formData.append('files', file))

  const response = await api.post<UploadResponse>('/upload/files', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}
