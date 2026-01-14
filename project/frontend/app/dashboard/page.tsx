'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import { useAuthStore } from '@/lib/store'
import { Resume } from '@/types/resume'

export default function DashboardPage() {
  const router = useRouter()
  const { token, logout } = useAuthStore()
  const [resumes, setResumes] = useState<Resume[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!token) {
      router.push('/auth/login')
      return
    }

    const fetchResumes = async () => {
      try {
        const response = await api.get('/api/v1/resumes/')
        setResumes(response.data)
      } catch (error) {
        console.error('Failed to fetch resumes:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchResumes()
  }, [token, router])

  const createNewResume = async () => {
    try {
      const response = await api.post('/api/v1/resumes/', {
        title: 'Untitled Resume',
        language: 'en',
      })
      router.push(`/editor/${response.data.id}`)
    } catch (error) {
      console.error('Failed to create resume:', error)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold text-gray-900">My Resumes</h1>
          <button
            onClick={logout}
            className="text-gray-600 hover:text-gray-900"
          >
            Sign Out
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        <button
          onClick={createNewResume}
          className="mb-8 px-6 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition"
        >
          + Create New Resume
        </button>

        {resumes.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-600 mb-4">You don't have any resumes yet.</p>
            <p className="text-gray-500">Click the button above to create your first resume.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {resumes.map((resume) => (
              <Link
                key={resume.id}
                href={`/editor/${resume.id}`}
                className="block p-6 bg-white rounded-xl shadow-sm hover:shadow-md transition"
              >
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{resume.title}</h3>
                <p className="text-sm text-gray-500 mb-2">
                  Language: {resume.language.toUpperCase()}
                </p>
                <p className="text-sm text-gray-500">
                  Last updated: {new Date(resume.updated_at).toLocaleDateString()}
                </p>
              </Link>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
