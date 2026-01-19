import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'

interface LeetCodeProblem {
  number: number
  title: string
  difficulty: 'Easy' | 'Medium' | 'Hard'
  topic: string
  url: string
  relevance: string
  key_concept: string
  status: string
}

interface DailyPlanProps {
  plan: {
    date: string
    leetcode: {
      target_count: number
      difficulty_mix: { easy: number; medium: number; hard: number }
      focus_topics: string[]
      problems?: LeetCodeProblem[]
      progression_logic?: string
      role_alignment?: string
      reasoning: string
    }
    applications: {
      target_count: number
      job_types: string[]
      companies_to_target?: string[]
      reasoning: string
    }
    learning_tasks: Array<{ task: string; time_estimate: string; reasoning: string }>
    summary: string
  }
}

export default function DailyPlan({ plan }: DailyPlanProps) {
  const [showProblems, setShowProblems] = useState(false)
  
  const getDifficultyStyle = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'easy': return 'badge-easy'
      case 'medium': return 'badge-medium'
      case 'hard': return 'badge-hard'
      default: return 'bg-white/10'
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="hq-panel p-6 space-y-6"
    >
      {/* Header with floating animation */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <motion.span 
            className="text-3xl"
            animate={{ y: [0, -5, 0], rotate: [0, 5, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            📋
          </motion.span>
          <div>
            <h3 className="text-xl font-bold text-white font-display">Today's Adventure</h3>
            <p className="text-purple-300 text-sm">Your path to core memories</p>
          </div>
        </div>
        <div className="px-4 py-2 rounded-full bg-gradient-to-r from-purple-500/30 to-pink-500/30 border border-purple-400/40">
          <span className="text-purple-200 text-sm">{plan.date}</span>
        </div>
      </div>

      {/* Summary with thought bubble style */}
      <motion.div 
        className="thought-bubble p-4"
        initial={{ scale: 0.95 }}
        animate={{ scale: 1 }}
      >
        <p className="text-purple-100 text-sm leading-relaxed pl-4">
          {plan.summary}
        </p>
      </motion.div>

      <div className="grid grid-cols-2 gap-6">
        {/* LeetCode Section - Joy's Island */}
        <motion.div 
          className="space-y-3"
          whileHover={{ scale: 1.02 }}
          transition={{ type: 'spring', stiffness: 300 }}
        >
          <div className="flex items-center gap-2">
            <motion.span 
              className="text-3xl"
              animate={{ rotate: [0, 10, -10, 0] }}
              transition={{ duration: 3, repeat: Infinity }}
            >
              💻
            </motion.span>
            <h4 className="font-bold text-white font-display">Coding Challenges</h4>
          </div>
          
          <div className="hq-panel-sm p-4 space-y-4">
            {/* Target with glowing effect */}
            <div className="flex items-center justify-between">
              <span className="text-purple-200">Target</span>
              <motion.span 
                className="text-4xl font-bold text-yellow-400 font-display"
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
                style={{ textShadow: '0 0 20px rgba(255, 215, 0, 0.5)' }}
              >
                {plan.leetcode.target_count}
              </motion.span>
            </div>
            
            {/* Difficulty mix as orbs */}
            <div className="flex gap-3 justify-center">
              {plan.leetcode.difficulty_mix.easy > 0 && (
                <motion.div 
                  className="flex items-center gap-2 px-3 py-2 rounded-full bg-gradient-to-r from-green-500/30 to-emerald-500/30 border border-green-400/40"
                  whileHover={{ scale: 1.1 }}
                >
                  <span className="w-3 h-3 rounded-full bg-green-400 shadow-lg" style={{ boxShadow: '0 0 10px rgba(74, 222, 128, 0.5)' }} />
                  <span className="text-green-300 text-sm font-medium">{plan.leetcode.difficulty_mix.easy} Easy</span>
                </motion.div>
              )}
              {plan.leetcode.difficulty_mix.medium > 0 && (
                <motion.div 
                  className="flex items-center gap-2 px-3 py-2 rounded-full bg-gradient-to-r from-yellow-500/30 to-orange-500/30 border border-yellow-400/40"
                  whileHover={{ scale: 1.1 }}
                >
                  <span className="w-3 h-3 rounded-full bg-yellow-400 shadow-lg" style={{ boxShadow: '0 0 10px rgba(250, 204, 21, 0.5)' }} />
                  <span className="text-yellow-300 text-sm font-medium">{plan.leetcode.difficulty_mix.medium} Medium</span>
                </motion.div>
              )}
              {plan.leetcode.difficulty_mix.hard > 0 && (
                <motion.div 
                  className="flex items-center gap-2 px-3 py-2 rounded-full bg-gradient-to-r from-red-500/30 to-rose-500/30 border border-red-400/40"
                  whileHover={{ scale: 1.1 }}
                >
                  <span className="w-3 h-3 rounded-full bg-red-400 shadow-lg" style={{ boxShadow: '0 0 10px rgba(248, 113, 113, 0.5)' }} />
                  <span className="text-red-300 text-sm font-medium">{plan.leetcode.difficulty_mix.hard} Hard</span>
                </motion.div>
              )}
            </div>

            {/* Focus Topics as floating islands */}
            <div>
              <span className="text-purple-300 text-xs block mb-2">🏝️ Focus Islands:</span>
              <div className="flex flex-wrap gap-2">
                {plan.leetcode.focus_topics.map((topic, i) => (
                  <motion.span 
                    key={i} 
                    className="px-3 py-1 rounded-full bg-gradient-to-r from-cyan-500/30 to-blue-500/30 border border-cyan-400/30 text-cyan-200 text-xs font-medium"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.1 }}
                    whileHover={{ scale: 1.1, y: -3 }}
                  >
                    {topic}
                  </motion.span>
                ))}
              </div>
            </div>

            {/* Show Problems Button - Joy's style */}
            {plan.leetcode.problems && plan.leetcode.problems.length > 0 && (
              <motion.button
                onClick={() => setShowProblems(!showProblems)}
                className="console-btn console-btn-joy w-full"
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.98 }}
              >
                <span className="flex items-center justify-center gap-2">
                  {showProblems ? '🔼 Hide Problems' : `✨ View ${plan.leetcode.problems.length} Problems`}
                </span>
              </motion.button>
            )}

            <p className="text-purple-300/70 text-xs italic text-center">
              {plan.leetcode.reasoning}
            </p>
          </div>
        </motion.div>

        {/* Applications Section - Dream Island */}
        <motion.div 
          className="space-y-3"
          whileHover={{ scale: 1.02 }}
          transition={{ type: 'spring', stiffness: 300 }}
        >
          <div className="flex items-center gap-2">
            <motion.span 
              className="text-3xl"
              animate={{ y: [0, -5, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              🌟
            </motion.span>
            <h4 className="font-bold text-white font-display">Dream Jobs</h4>
          </div>
          
          <div className="hq-panel-sm p-4 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-purple-200">Target</span>
              <motion.span 
                className="text-4xl font-bold text-purple-400 font-display"
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
                style={{ textShadow: '0 0 20px rgba(168, 85, 247, 0.5)' }}
              >
                {plan.applications.target_count}
              </motion.span>
            </div>

            <div>
              <span className="text-purple-300 text-xs block mb-2">🎯 Job Types:</span>
              <div className="flex flex-wrap gap-2">
                {plan.applications.job_types.map((type, i) => (
                  <motion.span 
                    key={i} 
                    className="px-3 py-1 rounded-full bg-gradient-to-r from-purple-500/30 to-pink-500/30 border border-purple-400/30 text-purple-200 text-xs font-medium"
                    initial={{ opacity: 0, scale: 0 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: i * 0.15 }}
                    whileHover={{ scale: 1.1 }}
                  >
                    {type}
                  </motion.span>
                ))}
              </div>
            </div>

            {/* Companies */}
            {plan.applications.companies_to_target && (
              <div>
                <span className="text-purple-300 text-xs block mb-2">🏢 Target Companies:</span>
                <div className="flex flex-wrap gap-2">
                  {plan.applications.companies_to_target.slice(0, 3).map((company, i) => (
                    <motion.span 
                      key={i} 
                      className="px-3 py-1 rounded-full bg-gradient-to-r from-yellow-500/20 to-orange-500/20 border border-yellow-400/30 text-yellow-200 text-xs font-medium"
                      whileHover={{ scale: 1.1, boxShadow: '0 0 15px rgba(255, 215, 0, 0.3)' }}
                    >
                      {company}
                    </motion.span>
                  ))}
                </div>
              </div>
            )}

            <p className="text-purple-300/70 text-xs italic text-center">
              {plan.applications.reasoning}
            </p>
          </div>
        </motion.div>
      </div>

      {/* Learning Tasks - Knowledge Island */}
      {plan.learning_tasks && plan.learning_tasks.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <motion.span 
              className="text-3xl"
              animate={{ rotate: [0, -10, 10, 0] }}
              transition={{ duration: 4, repeat: Infinity }}
            >
              📚
            </motion.span>
            <h4 className="font-bold text-white font-display">Learning Quests</h4>
          </div>
          
          <div className="space-y-3">
            {plan.learning_tasks.map((task, i) => (
              <motion.div 
                key={i} 
                className="hq-panel-sm p-4 flex items-center justify-between"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.1 }}
                whileHover={{ x: 5, borderColor: 'rgba(168, 85, 247, 0.5)' }}
              >
                <div className="flex items-start gap-3">
                  <motion.span 
                    className="text-2xl"
                    animate={{ rotate: [0, 10, 0] }}
                    transition={{ duration: 2, repeat: Infinity, delay: i * 0.3 }}
                  >
                    {i === 0 ? '🎓' : i === 1 ? '🔧' : '🚀'}
                  </motion.span>
                  <div>
                    <span className="text-white font-medium">{task.task}</span>
                    <p className="text-purple-300/60 text-xs mt-1">{task.reasoning}</p>
                  </div>
                </div>
                <span className="px-3 py-1 rounded-full bg-gradient-to-r from-cyan-500/30 to-blue-500/30 border border-cyan-400/30 text-cyan-200 text-sm font-medium whitespace-nowrap">
                  {task.time_estimate}
                </span>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Expandable Problems Section */}
      <AnimatePresence>
        {showProblems && plan.leetcode.problems && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="space-y-4 border-t border-purple-500/30 pt-6 overflow-hidden"
          >
            <div className="flex items-center justify-between">
              <h4 className="font-bold text-white font-display flex items-center gap-2">
                <motion.span
                  animate={{ rotate: 360 }}
                  transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
                >
                  🎯
                </motion.span>
                Today's LeetCode Problems
              </h4>
              <span className="text-purple-300 text-xs px-3 py-1 rounded-full bg-purple-500/20 border border-purple-400/30">
                Google-focused prep
              </span>
            </div>

            {/* Progression Logic */}
            {plan.leetcode.progression_logic && (
              <motion.div 
                className="p-4 rounded-xl bg-gradient-to-r from-cyan-500/20 to-blue-500/20 border border-cyan-400/30"
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
              >
                <span className="text-cyan-300 font-medium flex items-center gap-2 mb-2">
                  <span>📈</span> Progression Path
                </span>
                <p className="text-cyan-100/80 text-sm">{plan.leetcode.progression_logic}</p>
              </motion.div>
            )}

            {/* Problems List */}
            <div className="space-y-4">
              {plan.leetcode.problems.map((problem, i) => (
                <motion.div
                  key={problem.number}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.1 }}
                  className="hq-panel-sm p-5 hover:border-yellow-500/40 transition-all duration-300"
                  whileHover={{ scale: 1.01 }}
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <span className="text-purple-400 text-sm font-mono bg-purple-500/20 px-2 py-1 rounded">
                        #{problem.number}
                      </span>
                      <a 
                        href={problem.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-white font-bold hover:text-yellow-400 transition text-lg"
                      >
                        {problem.title}
                      </a>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${getDifficultyStyle(problem.difficulty)}`}>
                      {problem.difficulty}
                    </span>
                  </div>
                  
                  <div className="flex items-center gap-2 mb-3">
                    <span className="px-3 py-1 rounded-full bg-white/10 text-purple-200 text-xs font-medium">
                      📁 {problem.topic}
                    </span>
                  </div>
                  
                  <p className="text-purple-200/70 text-sm mb-2">
                    <span className="text-purple-300 font-medium">Why this problem:</span> {problem.relevance}
                  </p>
                  
                  <motion.div 
                    className="bg-gradient-to-r from-yellow-500/10 to-orange-500/10 rounded-lg p-3 border border-yellow-400/20"
                    whileHover={{ borderColor: 'rgba(255, 215, 0, 0.4)' }}
                  >
                    <p className="text-yellow-200 text-sm">
                      <span className="text-yellow-400 font-medium">💡 Key Concept:</span> {problem.key_concept}
                    </p>
                  </motion.div>
                  
                  <motion.a 
                    href={problem.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="console-btn console-btn-primary mt-4 inline-flex items-center gap-2 text-sm"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <span>🚀</span> Solve on LeetCode
                  </motion.a>
                </motion.div>
              ))}
            </div>

            {/* Role Alignment */}
            {plan.leetcode.role_alignment && (
              <motion.div 
                className="p-4 rounded-xl bg-gradient-to-r from-purple-500/20 to-pink-500/20 border border-purple-400/30"
                initial={{ x: 20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
              >
                <span className="text-purple-300 font-medium flex items-center gap-2 mb-2">
                  <span>🎯</span> Role Alignment
                </span>
                <p className="text-purple-100/80 text-sm">{plan.leetcode.role_alignment}</p>
              </motion.div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}
