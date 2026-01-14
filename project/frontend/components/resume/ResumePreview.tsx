'use client'

import { ResumeContent } from '@/types/resume'

interface Props {
  content: ResumeContent
}

export default function ResumePreview({ content }: Props) {
  const { personal_info, work_experience, education, skills, languages } = content

  return (
    <div className="bg-white shadow-lg p-8 max-w-[800px] mx-auto" id="resume-preview">
      {/* Header */}
      <header className="border-b pb-4 mb-6">
        <h1 className="text-3xl font-bold text-gray-900">
          {personal_info.first_name} {personal_info.last_name}
        </h1>
        <div className="mt-2 flex flex-wrap gap-4 text-sm text-gray-600">
          {personal_info.email && <span>{personal_info.email}</span>}
          {personal_info.phone && <span>{personal_info.phone}</span>}
          {personal_info.location && <span>{personal_info.location}</span>}
        </div>
        {personal_info.summary && (
          <p className="mt-4 text-gray-700">{personal_info.summary}</p>
        )}
      </header>

      {/* Work Experience */}
      {work_experience.length > 0 && (
        <section className="mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-3 uppercase tracking-wide">
            Work Experience
          </h2>
          {work_experience.map((exp, index) => (
            <div key={index} className="mb-4">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-gray-900">{exp.position}</h3>
                  <p className="text-gray-600">{exp.company}</p>
                </div>
                <span className="text-sm text-gray-500">
                  {exp.start_date} - {exp.is_current ? 'Present' : exp.end_date}
                </span>
              </div>
              {exp.description && (
                <p className="mt-2 text-gray-700 text-sm">{exp.description}</p>
              )}
              {exp.achievements.length > 0 && (
                <ul className="mt-2 list-disc list-inside text-sm text-gray-700">
                  {exp.achievements.map((achievement, i) => (
                    <li key={i}>{achievement}</li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </section>
      )}

      {/* Education */}
      {education.length > 0 && (
        <section className="mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-3 uppercase tracking-wide">
            Education
          </h2>
          {education.map((edu, index) => (
            <div key={index} className="mb-4">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-gray-900">{edu.institution}</h3>
                  <p className="text-gray-600">
                    {edu.degree}
                    {edu.field_of_study && ` in ${edu.field_of_study}`}
                  </p>
                </div>
                <span className="text-sm text-gray-500">
                  {edu.start_date} - {edu.end_date}
                </span>
              </div>
              {edu.gpa && (
                <p className="mt-1 text-sm text-gray-600">GPA: {edu.gpa}</p>
              )}
            </div>
          ))}
        </section>
      )}

      {/* Skills */}
      {skills.length > 0 && (
        <section className="mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-3 uppercase tracking-wide">
            Skills
          </h2>
          <div className="flex flex-wrap gap-2">
            {skills.map((skill, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm"
              >
                {skill.name}
              </span>
            ))}
          </div>
        </section>
      )}

      {/* Languages */}
      {languages.length > 0 && (
        <section>
          <h2 className="text-lg font-semibold text-gray-900 mb-3 uppercase tracking-wide">
            Languages
          </h2>
          <div className="flex flex-wrap gap-4">
            {languages.map((lang, index) => (
              <span key={index} className="text-gray-700">
                {lang.name} ({lang.proficiency})
              </span>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
