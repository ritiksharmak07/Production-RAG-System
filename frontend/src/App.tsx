import { Routes, Route } from 'react-router-dom'
import { motion } from 'framer-motion'
import Layout from './layouts/Layout'
import HomePage from './pages/Home/HomePage'
import ChatPage from './pages/Chat/ChatPage'
import SearchPage from './pages/Search/SearchPage'
import UploadPage from './pages/Upload/UploadPage'
import SettingsPage from './pages/Settings/SettingsPage'
import NotFoundPage from './pages/Errors/NotFoundPage'

function App() {
  return (
    <Layout>
      <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.2 }}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </motion.div>
    </Layout>
  )
}

export default App
