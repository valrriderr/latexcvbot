'use client'

import { useEffect, useState } from 'react'
import { useRouter, useParams } from 'next/navigation'
import { api } from '@/lib/api'
import { useAuthStore } from '@/lib/store'
import { Resume, ResumeContent } from '@/types/resume'
import ResumeEditor from '@/components/resume/ResumeEditor'
import ResumePreview from '@/components/resume/ResumePreview'

export default function EditorPage() {
  const router = useRouter()
  const params = useParams()
  const { token } = useAuthStore()
  const [resume, setResume] = useState<Resume | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (!token) {
      router.push('/auth/login')
      return
    }

    const fetchResume = async () => {
      try {
        const response = await api.get(`/api/v1/resumes/${params.id}`)
        setResume(response.data)
      } catch (error) {
        console.error('Failed to fetch resume:', error)
        router.push('/dashboard')
      } finally {
        setLoading(false)
      }
    }

    fetchResume()
  }, [token, params.id, router])

  const handleUpdate = async (content: ResumeContent) => {
    if (!resume) return

    setSaving(true)
    try {
      const response = await api.put(`/api/v1/resumes/${resume.id}`, { content })
      setResume(response.data)
    } catch (error) {
      console.error('Failed to save resume:', error)
    } finally {
      setSaving(false)
    }
  }

  const handleExportPDF = async () => {
    // TODO: Implement PDF export
    alert('PDF export coming soon!')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!resume) return null

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-full mx-auto px-6 py-3 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <button
              onClick={() => router.push('/dashboard')}
              className="text-gray-600 hover:text-gray-900"
            >
              &larr; Back
            </button>
            <input
              type="text"
              value={resume.title}
              onChange={(e) => setResume({ ...resume, title: e.target.value })}
              className="text-lg font-semibold bg-transparent border-none focus:outline-none focus:ring-0"
            />
          </div>
          <div className="flex items-center gap-4">
            {saving && <span className="text-sm text-gray-500">Saving...</span>}
            <button
              onClick={handleExportPDF}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition"
            >
              Export PDF
            </button>
          </div>
        </div>
      </header>

      <main className="flex h-[calc(100vh-57px)]">
        <div className="w-1/2 overflow-y-auto p-6 bg-white border-r">
          <ResumeEditor content={resume.content} onUpdate={handleUpdate} />
        </div>
        <div className="w-1/2 overflow-y-auto p-6 bg-gray-100">
          <ResumePreview content={resume.content} />
        </div>
      </main>
    </div>
  )
}
