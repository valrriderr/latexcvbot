export interface PersonalInfo {
  first_name: string
  last_name: string
  email: string
  phone: string
  location: string
  linkedin?: string
  website?: string
  summary?: string
}

export interface WorkExperience {
  company: string
  position: string
  location?: string
  start_date: string
  end_date?: string
  is_current: boolean
  description?: string
  achievements: string[]
}

export interface Education {
  institution: string
  degree: string
  field_of_study?: string
  location?: string
  start_date: string
  end_date?: string
  gpa?: string
  achievements: string[]
}

export interface Skill {
  name: string
  level?: 'beginner' | 'intermediate' | 'advanced' | 'expert'
}

export interface Language {
  name: string
  proficiency: 'native' | 'fluent' | 'advanced' | 'intermediate' | 'basic'
}

export interface ResumeContent {
  personal_info: PersonalInfo
  work_experience: WorkExperience[]
  education: Education[]
  skills: Skill[]
  languages: Language[]
}

export type ResumeLanguage = 'en' | 'ru' | 'fr'

export interface Resume {
  id: string
  user_id: string
  title: string
  language: ResumeLanguage
  template_id: string
  content: ResumeContent
  current_version: number
  created_at: string
  updated_at: string
}
