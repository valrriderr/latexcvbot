import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-white to-gray-100">
      <div className="text-center max-w-3xl px-6">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          Build Professional Resumes with AI
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Create, translate, and export your resume in multiple languages and formats.
          Powered by advanced AI for professional results.
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/auth/register"
            className="px-8 py-3 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition"
          >
            Get Started
          </Link>
          <Link
            href="/auth/login"
            className="px-8 py-3 bg-white text-primary-600 border border-primary-600 rounded-lg font-medium hover:bg-primary-50 transition"
          >
            Sign In
          </Link>
        </div>
      </div>

      <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl px-6">
        <div className="p-6 bg-white rounded-xl shadow-sm">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">AI Translation</h3>
          <p className="text-gray-600">
            Translate your resume to English, Russian, or French with professional HR-optimized language.
          </p>
        </div>
        <div className="p-6 bg-white rounded-xl shadow-sm">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Multiple Templates</h3>
          <p className="text-gray-600">
            Choose from professionally designed templates that stand out to recruiters.
          </p>
        </div>
        <div className="p-6 bg-white rounded-xl shadow-sm">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Export Anywhere</h3>
          <p className="text-gray-600">
            Download your resume as PDF, or export to LaTeX for advanced customization.
          </p>
        </div>
      </div>
    </main>
  )
}
