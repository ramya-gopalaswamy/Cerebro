import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import ResumeUpload from '../components/ResumeUpload'
import DailyPlan from '../components/DailyPlan'
import JobCard from '../components/JobCard'
import OrbJar from '../components/OrbJar'
import AgentThoughts from '../components/AgentThoughts'
import SkillGaps from '../components/SkillGaps'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

type ViewState = 'upload' | 'dashboard' | 'verify'

interface ParsedResume {
  name: string
  current_title: string
  years_experience: number
  skills: Array<{ name: string; category: string }>
  inferred: {
    experience_level: string
    strengths: string[]
    weaknesses: string[]
    skills_to_develop: string[]
  }
}

// Floating memory orb component
const FloatingOrb = ({ color, size, delay, duration, left, top }: any) => (
  <motion.div
    className="floating-orb memory-orb"
    style={{
      width: size,
      height: size,
      left: `${left}%`,
      top: `${top}%`,
      background: `linear-gradient(135deg, ${color} 0%, ${color}99 100%)`,
      boxShadow: `0 0 ${size/2}px ${size/4}px ${color}66`,
    }}
    animate={{
      y: [0, -30, 0],
      x: [0, 10, -10, 0],
      opacity: [0.4, 0.7, 0.4],
    }}
    transition={{
      duration: duration,
      delay: delay,
      repeat: Infinity,
      ease: "easeInOut"
    }}
  />
)

export default function JobLandPage() {
  const [view, setView] = useState<ViewState>('upload')
  const [resumeId, setResumeId] = useState<string | null>(null)
  const [parsedResume, setParsedResume] = useState<ParsedResume | null>(null)
  const [leetcodeUsername, setLeetcodeUsername] = useState('')
  const [dailyPlan, setDailyPlan] = useState<any>(null)
  const [matchedJobs, setMatchedJobs] = useState<any[]>([])
  const [skillGaps, setSkillGaps] = useState<any[]>([])
  const [skillGapsSummary, setSkillGapsSummary] = useState<any>(null)
  const [orbs, setOrbs] = useState<any[]>([])
  const [agentThoughts, setAgentThoughts] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [verificationResults, setVerificationResults] = useState<any[]>([])
  const [isVerifying, setIsVerifying] = useState(false)
  const [leetcodeData, setLeetcodeData] = useState<any>(null)
  const [gmailData, setGmailData] = useState<any>(null)

  // Handle resume upload complete
  const handleResumeUploaded = (id: string, parsed: ParsedResume) => {
    setResumeId(id)
    setParsedResume(parsed)
    setView('dashboard')
  }

  // Create plan - calls backend which uses Yutori/TinyFish
  const handleCreatePlan = async () => {
    if (!resumeId || !leetcodeUsername) return
    
    setIsLoading(true)
    setAgentThoughts([])
    setAgentThoughts(prev => [...prev, '🧠 Joy is activating the planning console...'])
    
    try {
      const response = await fetch(`${API_BASE}/api/plan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_id: resumeId,
          leetcode_username: leetcodeUsername,
          targets: { leetcode: 5, applications: 2 }
        })
      })
      
      const data = await response.json()
      
      if (data.daily_plan) {
        setDailyPlan(data.daily_plan)
        const problemCount = data.daily_plan?.leetcode?.problems?.length || 0
        setAgentThoughts(prev => [...prev, `✨ Created a plan with ${problemCount} memory-making challenges!`])
      }
      
      if (data.matched_jobs?.length > 0) {
        setMatchedJobs(data.matched_jobs)
        setAgentThoughts(prev => [...prev, `🌟 Found ${data.matched_jobs.length} dream job opportunities!`])
      }
      
      if (data.skill_gaps?.length > 0) {
        setSkillGaps(data.skill_gaps)
        setAgentThoughts(prev => [...prev, `📚 Mapped ${data.skill_gaps.length} skill islands to explore`])
      }
      
      if (data.skill_gaps_summary) {
        setSkillGapsSummary(data.skill_gaps_summary)
      }
      
      if (data.agent_thoughts) {
        setAgentThoughts(prev => [...prev, ...data.agent_thoughts])
      }
      
    } catch (error) {
      console.error('Planning failed:', error)
      setAgentThoughts(prev => [...prev, `😰 Fear detected an error: ${error}`])
    } finally {
      setIsLoading(false)
    }
  }

  // Verify progress - calls TinyFish to check LeetCode and Gmail
  const handleVerify = async () => {
    if (!leetcodeUsername) {
      alert('Please enter your LeetCode username first!')
      return
    }
    
    setIsVerifying(true)
    setVerificationResults([])
    setAgentThoughts(prev => [...prev, `🔍 Sadness is carefully checking your progress...`])
    
    try {
      const response = await fetch(`${API_BASE}/api/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_id: resumeId,
          leetcode_username: leetcodeUsername,
          targets: { leetcode: 5, applications: 2 }
        })
      })
      
      const data = await response.json()
      
      if (data.verification_results) {
        setVerificationResults(data.verification_results)
        
        data.verification_results.forEach((result: any) => {
          const emoji = result.status === 'success' ? '🌟' : '💪'
          setAgentThoughts(prev => [...prev, `${emoji} ${result.task_type}: ${result.actual}/${result.target} completed`])
        })
      }
      
      if (data.leetcode_data) {
        setLeetcodeData(data.leetcode_data)
      }
      
      if (data.gmail_data) {
        setGmailData(data.gmail_data)
      }
      
      if (data.orbs_earned?.length > 0) {
        setOrbs(prev => [...prev, ...data.orbs_earned])
        setAgentThoughts(prev => [...prev, `✨ ${data.orbs_earned.length} new memory orbs created!`])
      }
      
      if (data.agent_thoughts) {
        setAgentThoughts(prev => [...prev, ...data.agent_thoughts])
      }
      
    } catch (error) {
      console.error('Verification failed:', error)
      setAgentThoughts(prev => [...prev, `😰 Verification error: ${error}`])
    } finally {
      setIsVerifying(false)
    }
  }

  // Floating orbs configuration - Inside Out 5 core emotions
  const floatingOrbs = [
    { color: '#FFD700', size: 20, delay: 0, duration: 8, left: 5, top: 20 },      // Joy - Yellow
    { color: '#5B8DD9', size: 15, delay: 1, duration: 10, left: 90, top: 30 },    // Sadness - Blue
    { color: '#E53935', size: 18, delay: 2, duration: 7, left: 15, top: 70 },     // Anger - Red
    { color: '#9C27B0', size: 22, delay: 0.5, duration: 9, left: 85, top: 60 },   // Anxiety - Purple
    { color: '#4CAF50', size: 16, delay: 3, duration: 11, left: 50, top: 15 },    // Disgust - Green
    { color: '#FFD700', size: 12, delay: 1.5, duration: 8, left: 75, top: 80 },   // Joy - Yellow (extra)
  ]

  return (
    <div className="inside-out-bg min-h-screen relative">
      {/* Floating memory orbs */}
      <div className="floating-orbs">
        {floatingOrbs.map((orb, i) => (
          <FloatingOrb key={i} {...orb} />
        ))}
      </div>

      {/* Header - Headquarters Control Panel */}
      <header className="relative z-10 px-6 py-4">
        <div className="max-w-7xl mx-auto">
          <motion.div 
            className="hq-panel px-6 py-4 flex items-center justify-between"
            initial={{ y: -50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <div className="flex items-center gap-4">
              <motion.div 
                className="w-14 h-14 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 flex items-center justify-center shadow-joy"
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                <span className="text-2xl">🧠</span>
              </motion.div>
              <div>
                <h1 className="hq-title text-3xl">CEREBRO</h1>
                <p className="text-purple-300 text-sm font-medium tracking-wider">Headquarters Control</p>
              </div>
            </div>
            
            {parsedResume && (
              <div className="flex items-center gap-4">
                <div className="text-right">
                  <span className="text-white font-bold text-lg">{parsedResume.name}</span>
                  <p className="text-purple-300 text-sm">{parsedResume.current_title}</p>
                </div>
                <motion.div 
                  className="w-12 h-12 rounded-full memory-orb orb-joy flex items-center justify-center"
                  animate={{ rotate: 360 }}
                  transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                >
                  <span className="text-xl">👤</span>
                </motion.div>
              </div>
            )}
          </motion.div>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 max-w-7xl mx-auto px-6 py-8">
        <AnimatePresence mode="wait">
          {/* Upload View - Welcome Screen */}
          {view === 'upload' && (
            <motion.div
              key="upload"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="flex flex-col items-center justify-center min-h-[70vh]"
            >
              <motion.div 
                className="hq-panel p-12 text-center max-w-2xl"
                initial={{ y: 50 }}
                animate={{ y: 0 }}
                transition={{ delay: 0.2 }}
              >
                <motion.div
                  className="w-32 h-32 mx-auto mb-6 rounded-full bg-gradient-to-br from-yellow-400 via-orange-400 to-yellow-500 flex items-center justify-center shadow-joy"
                  animate={{ 
                    scale: [1, 1.05, 1],
                    rotate: [0, 5, -5, 0]
                  }}
                  transition={{ duration: 3, repeat: Infinity }}
                >
                  <span className="text-6xl">✨</span>
                </motion.div>
                
                <h2 className="hq-title text-4xl mb-3">Welcome to Headquarters!</h2>
                <p className="text-purple-200 text-lg mb-8">
                  Let's create some amazing core memories together! 
                  <br/>Upload your resume to begin your journey.
                </p>
                
                <ResumeUpload onUploaded={handleResumeUploaded} apiBase={API_BASE} />
                
                <div className="mt-8 flex justify-center gap-4">
                  {/* Joy, Sadness, Anger, Anxiety, Disgust */}
                  {['😊', '😢', '😤', '😰', '🤢'].map((emoji, i) => (
                    <motion.span
                      key={i}
                      className="text-2xl"
                      animate={{ y: [0, -10, 0] }}
                      transition={{ duration: 1, delay: i * 0.2, repeat: Infinity }}
                    >
                      {emoji}
                    </motion.span>
                  ))}
                </div>
              </motion.div>
            </motion.div>
          )}

          {/* Dashboard View */}
          {view === 'dashboard' && parsedResume && (
            <motion.div
              key="dashboard"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="grid grid-cols-12 gap-6"
            >
              {/* Left Column - Plan & Jobs */}
              <div className="col-span-8 space-y-6">
                {/* Control Console */}
                <motion.div 
                  className="hq-panel p-6"
                  initial={{ x: -50, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: 0.1 }}
                >
                  <div className="flex items-center gap-3 mb-4">
                    <motion.span 
                      className="text-3xl"
                      animate={{ rotate: [0, 20, -20, 0] }}
                      transition={{ duration: 2, repeat: Infinity }}
                    >
                      🎮
                    </motion.span>
                    <h3 className="text-xl font-bold text-white font-display">Control Console</h3>
                  </div>
                  
                  <div className="flex gap-4 mb-4">
                    <input
                      type="text"
                      placeholder="Enter your LeetCode username..."
                      value={leetcodeUsername}
                      onChange={(e) => setLeetcodeUsername(e.target.value)}
                      className="hq-input flex-1"
                    />
                    <motion.button
                      onClick={handleCreatePlan}
                      disabled={!leetcodeUsername || isLoading}
                      className="console-btn console-btn-joy disabled:opacity-50"
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      {isLoading ? (
                        <span className="flex items-center gap-2">
                          <motion.span animate={{ rotate: 360 }} transition={{ duration: 1, repeat: Infinity }}>⚙️</motion.span>
                          Creating...
                        </span>
                      ) : (
                        <span className="flex items-center gap-2">✨ Create Plan</span>
                      )}
                    </motion.button>
                  </div>
                  
                  <motion.button
                    onClick={handleVerify}
                    disabled={!leetcodeUsername || isVerifying}
                    className="console-btn console-btn-primary disabled:opacity-50 w-full"
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    {isVerifying ? (
                      <span className="flex items-center justify-center gap-2">
                        <motion.span animate={{ scale: [1, 1.2, 1] }} transition={{ duration: 0.5, repeat: Infinity }}>🔍</motion.span>
                        Checking Memories...
                      </span>
                    ) : (
                      <span className="flex items-center justify-center gap-2">🔍 Verify My Progress</span>
                    )}
                  </motion.button>
                </motion.div>

                {/* Daily Plan */}
                {dailyPlan && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                  >
                    <DailyPlan plan={dailyPlan} />
                  </motion.div>
                )}

                {/* Verification Results */}
                {verificationResults.length > 0 && (
                  <motion.div 
                    className="hq-panel p-6"
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                  >
                    <div className="flex items-center gap-3 mb-4">
                      <span className="text-2xl">📊</span>
                      <h3 className="text-xl font-bold text-white font-display">Memory Verification</h3>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                      {verificationResults.map((result, i) => (
                        <motion.div
                          key={i}
                          className={`hq-panel-sm p-4 ${
                            result.status === 'success'
                              ? 'border-green-500/50'
                              : 'border-yellow-500/50'
                          }`}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: i * 0.1 }}
                        >
                          <div className="flex items-center justify-between mb-3">
                            <span className="text-white font-bold capitalize flex items-center gap-2">
                              {result.task_type === 'leetcode' ? '💻' : '📧'}
                              {result.task_type}
                            </span>
                            <motion.span 
                              className={`text-3xl font-bold ${
                                result.status === 'success' ? 'text-green-400' : 'text-yellow-400'
                              }`}
                              animate={{ scale: [1, 1.1, 1] }}
                              transition={{ duration: 1, repeat: Infinity }}
                            >
                              {result.actual}/{result.target}
                            </motion.span>
                          </div>
                          
                          <p className="text-purple-200 text-sm">{result.details}</p>
                          
                          {result.task_type === 'leetcode' && result.recent_submissions && (
                            <div className="mt-3 space-y-1">
                              <span className="text-purple-300 text-xs font-medium">Recent Memories:</span>
                              {result.recent_submissions.slice(0, 3).map((sub: any, j: number) => (
                                <div key={j} className="text-xs text-purple-200 flex items-center gap-2">
                                  <span className={`px-2 py-0.5 rounded-full text-white ${
                                    sub.difficulty === 'Easy' ? 'badge-easy' :
                                    sub.difficulty === 'Medium' ? 'badge-medium' :
                                    'badge-hard'
                                  }`}>{sub.difficulty[0]}</span>
                                  <span>{sub.problem}</span>
                                </div>
                              ))}
                            </div>
                          )}
                          
                          {result.task_type === 'applications' && result.interviews?.length > 0 && (
                            <motion.div 
                              className="mt-3 p-3 rounded-xl bg-gradient-to-r from-purple-500/30 to-pink-500/30 border border-purple-400/40"
                              animate={{ boxShadow: ['0 0 20px rgba(168,85,247,0.3)', '0 0 40px rgba(168,85,247,0.5)', '0 0 20px rgba(168,85,247,0.3)'] }}
                              transition={{ duration: 2, repeat: Infinity }}
                            >
                              <span className="text-purple-200 text-xs font-bold">🎉 INTERVIEW SCHEDULED!</span>
                              <div className="text-white font-bold mt-1">{result.interviews[0].company}</div>
                            </motion.div>
                          )}
                        </motion.div>
                      ))}
                    </div>
                  </motion.div>
                )}

                {/* Matched Jobs */}
                {matchedJobs.length > 0 && (
                  <motion.div 
                    className="space-y-4"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.3 }}
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">🌟</span>
                      <h3 className="text-xl font-bold text-white font-display">Dream Job Islands</h3>
                    </div>
                    {matchedJobs.map((job, i) => (
                      <motion.div
                        key={i}
                        initial={{ opacity: 0, x: -30 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.1 * i }}
                      >
                        <JobCard job={job} />
                      </motion.div>
                    ))}
                  </motion.div>
                )}
                
                {/* Skill Gaps Section */}
                {skillGaps.length > 0 && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                  >
                    <SkillGaps gaps={skillGaps} summary={skillGapsSummary} />
                  </motion.div>
                )}

                {/* Agent Thoughts */}
                {agentThoughts.length > 0 && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5 }}
                  >
                    <AgentThoughts thoughts={agentThoughts} />
                  </motion.div>
                )}
              </div>

              {/* Right Column - Profile & Orbs */}
              <div className="col-span-4 space-y-6">
                {/* Profile Summary */}
                <motion.div 
                  className="hq-panel p-6"
                  initial={{ x: 50, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ delay: 0.2 }}
                >
                  <div className="flex items-center gap-3 mb-4">
                    <motion.div 
                      className="w-12 h-12 rounded-full memory-orb orb-joy"
                      animate={{ scale: [1, 1.1, 1] }}
                      transition={{ duration: 2, repeat: Infinity }}
                    />
                    <div>
                      <h3 className="text-lg font-bold text-white font-display">Your Profile</h3>
                      <p className="text-purple-300 text-sm">Core Identity</p>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="hq-panel-sm p-3">
                      <span className="text-purple-300 text-xs">Experience Level</span>
                      <div className="text-white font-bold capitalize flex items-center gap-2">
                        <span className="text-xl">⭐</span>
                        {parsedResume.inferred.experience_level}
                      </div>
                    </div>
                    
                    <div className="hq-panel-sm p-3">
                      <span className="text-purple-300 text-xs">Years of Experience</span>
                      <div className="text-white font-bold flex items-center gap-2">
                        <span className="text-xl">📅</span>
                        {parsedResume.years_experience} years
                      </div>
                    </div>
                    
                    <div>
                      <span className="text-purple-300 text-xs block mb-2">💪 Core Strengths</span>
                      <div className="flex flex-wrap gap-2">
                        {parsedResume.inferred.strengths.slice(0, 3).map((s, i) => (
                          <motion.span 
                            key={i} 
                            className="px-3 py-1 rounded-full bg-gradient-to-r from-green-500/30 to-emerald-500/30 border border-green-400/40 text-green-300 text-xs font-medium"
                            initial={{ opacity: 0, scale: 0 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.3 + i * 0.1 }}
                          >
                            {s}
                          </motion.span>
                        ))}
                      </div>
                    </div>
                    
                    <div>
                      <span className="text-purple-300 text-xs block mb-2">🎯 Skills to Grow</span>
                      <div className="flex flex-wrap gap-2">
                        {parsedResume.inferred.skills_to_develop.slice(0, 3).map((s, i) => (
                          <motion.span 
                            key={i} 
                            className="px-3 py-1 rounded-full bg-gradient-to-r from-yellow-500/30 to-orange-500/30 border border-yellow-400/40 text-yellow-300 text-xs font-medium"
                            initial={{ opacity: 0, scale: 0 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.5 + i * 0.1 }}
                          >
                            {s}
                          </motion.span>
                        ))}
                      </div>
                    </div>
                  </div>
                </motion.div>

                {/* Orb Jar */}
                <motion.div
                  initial={{ y: 50, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.4 }}
                >
                  <OrbJar orbs={orbs} />
                </motion.div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Footer */}
      <footer className="relative z-10 text-center py-6 text-purple-300 text-sm">
        <p>Made with 💜 by the emotions at Headquarters</p>
      </footer>
    </div>
  )
}
