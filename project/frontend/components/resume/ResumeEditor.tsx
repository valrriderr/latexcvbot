'use client'

import { useState, useCallback } from 'react'
import { ResumeContent, WorkExperience, Education } from '@/types/resume'
import debounce from '@/lib/debounce'

interface Props {
  content: ResumeContent
  onUpdate: (content: ResumeContent) => void
}

export default function ResumeEditor({ content, onUpdate }: Props) {
  const [localContent, setLocalContent] = useState(content)

  const debouncedUpdate = useCallback(
    debounce((newContent: ResumeContent) => {
      onUpdate(newContent)
    }, 1000),
    [onUpdate]
  )

  const updateContent = (updates: Partial<ResumeContent>) => {
    const newContent = { ...localContent, ...updates }
    setLocalContent(newContent)
    debouncedUpdate(newContent)
  }

  const updatePersonalInfo = (field: string, value: string) => {
    updateContent({
      personal_info: { ...localContent.personal_info, [field]: value }
    })
  }

  return (
    <div className="space-y-8">
      {/* Personal Information */}
      <section>
        <h2 className="text-lg font-semibold mb-4">Personal Information</h2>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">First Name</label>
            <input
              type="text"
              value={localContent.personal_info.first_name}
              onChange={(e) => updatePersonalInfo('first_name', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
            <input
              type="text"
              value={localContent.personal_info.last_name}
              onChange={(e) => updatePersonalInfo('last_name', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input
              type="email"
              value={localContent.personal_info.email}
              onChange={(e) => updatePersonalInfo('email', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
            <input
              type="tel"
              value={localContent.personal_info.phone}
              onChange={(e) => updatePersonalInfo('phone', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <div className="col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
            <input
              type="text"
              value={localContent.personal_info.location}
              onChange={(e) => updatePersonalInfo('location', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              placeholder="City, Country"
            />
          </div>
          <div className="col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Summary</label>
            <textarea
              value={localContent.personal_info.summary || ''}
              onChange={(e) => updatePersonalInfo('summary', e.target.value)}
              rows={4}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              placeholder="Brief professional summary..."
            />
          </div>
        </div>
      </section>

      {/* Work Experience */}
      <section>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold">Work Experience</h2>
          <button
            onClick={() => {
              const newExperience: WorkExperience = {
                company: '',
                position: '',
                start_date: '',
                is_current: false,
                achievements: []
              }
              updateContent({
                work_experience: [...localContent.work_experience, newExperience]
              })
            }}
            className="text-sm text-primary-600 hover:underline"
          >
            + Add Experience
          </button>
        </div>
        {localContent.work_experience.map((exp, index) => (
          <div key={index} className="mb-6 p-4 border border-gray-200 rounded-lg">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Company</label>
                <input
                  type="text"
                  value={exp.company}
                  onChange={(e) => {
                    const updated = [...localContent.work_experience]
                    updated[index] = { ...exp, company: e.target.value }
                    updateContent({ work_experience: updated })
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Position</label>
                <input
                  type="text"
                  value={exp.position}
                  onChange={(e) => {
                    const updated = [...localContent.work_experience]
                    updated[index] = { ...exp, position: e.target.value }
                    updateContent({ work_experience: updated })
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
                <input
                  type="text"
                  value={exp.start_date}
                  onChange={(e) => {
                    const updated = [...localContent.work_experience]
                    updated[index] = { ...exp, start_date: e.target.value }
                    updateContent({ work_experience: updated })
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  placeholder="Jan 2020"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
                <input
                  type="text"
                  value={exp.end_date || ''}
                  onChange={(e) => {
                    const updated = [...localContent.work_experience]
                    updated[index] = { ...exp, end_date: e.target.value }
                    updateContent({ work_experience: updated })
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  placeholder="Present"
                  disabled={exp.is_current}
                />
              </div>
              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  value={exp.description || ''}
                  onChange={(e) => {
                    const updated = [...localContent.work_experience]
                    updated[index] = { ...exp, description: e.target.value }
                    updateContent({ work_experience: updated })
                  }}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
            </div>
            <button
              onClick={() => {
                const updated = localContent.work_experience.filter((_, i) => i !== index)
                updateContent({ work_experience: updated })
              }}
              className="mt-2 text-sm text-red-600 hover:underline"
            >
              Remove
            </button>
          </div>
        ))}
      </section>

      {/* Education */}
      <section>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold">Education</h2>
          <button
            onClick={() => {
              const newEducation: Education = {
                institution: '',
                degree: '',
                start_date: '',
                achievements: []
              }
              updateContent({
                education: [...localContent.education, newEducation]
              })
            }}
            className="text-sm text-primary-600 hover:underline"
          >
            + Add Education
          </button>
        </div>
        {localContent.education.map((edu, index) => (
          <div key={index} className="mb-6 p-4 border border-gray-200 rounded-lg">
            <div className="grid grid-cols-2 gap-4">
              <div className="col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-1">Institution</label>
                <input
                  type="text"
                  value={edu.institution}
                  onChange={(e) => {
                    const updated = [...localContent.education]
                    updated[index] = { ...edu, institution: e.target.value }
                    updateContent({ education: updated })
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Degree</label>
                <input
                  type="text"
                  value={edu.degree}
                  onChange={(e) => {
                    const updated = [...localContent.education]
                    updated[index] = { ...edu, degree: e.target.value }
                    updateContent({ education: updated })
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Field of Study</label>
                <input
                  type="text"
                  value={edu.field_of_study || ''}
                  onChange={(e) => {
                    const updated = [...localContent.education]
                    updated[index] = { ...edu, field_of_study: e.target.value }
                    updateContent({ education: updated })
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
                <input
                  type="text"
                  value={edu.start_date}
                  onChange={(e) => {
                    const updated = [...localContent.education]
                    updated[index] = { ...edu, start_date: e.target.value }
                    updateContent({ education: updated })
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  placeholder="Sep 2016"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
                <input
                  type="text"
                  value={edu.end_date || ''}
                  onChange={(e) => {
                    const updated = [...localContent.education]
                    updated[index] = { ...edu, end_date: e.target.value }
                    updateContent({ education: updated })
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                  placeholder="May 2020"
                />
              </div>
            </div>
            <button
              onClick={() => {
                const updated = localContent.education.filter((_, i) => i !== index)
                updateContent({ education: updated })
              }}
              className="mt-2 text-sm text-red-600 hover:underline"
            >
              Remove
            </button>
          </div>
        ))}
      </section>

      {/* Skills */}
      <section>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold">Skills</h2>
          <button
            onClick={() => {
              updateContent({
                skills: [...localContent.skills, { name: '' }]
              })
            }}
            className="text-sm text-primary-600 hover:underline"
          >
            + Add Skill
          </button>
        </div>
        <div className="flex flex-wrap gap-2">
          {localContent.skills.map((skill, index) => (
            <div key={index} className="flex items-center gap-2 bg-gray-100 px-3 py-1 rounded-full">
              <input
                type="text"
                value={skill.name}
                onChange={(e) => {
                  const updated = [...localContent.skills]
                  updated[index] = { ...skill, name: e.target.value }
                  updateContent({ skills: updated })
                }}
                className="bg-transparent border-none focus:outline-none text-sm w-24"
                placeholder="Skill name"
              />
              <button
                onClick={() => {
                  const updated = localContent.skills.filter((_, i) => i !== index)
                  updateContent({ skills: updated })
                }}
                className="text-gray-500 hover:text-red-600"
              >
                &times;
              </button>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
