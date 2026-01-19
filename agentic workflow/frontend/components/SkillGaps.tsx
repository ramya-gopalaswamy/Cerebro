import { motion, AnimatePresence } from 'framer-motion'
import { useState } from 'react'

interface SkillGap {
  id: number
  topic: string
  priority: 'HIGH' | 'MEDIUM' | 'LOW'
  current_state: string
  target_skills: string[]
  resources: {
    free: Array<{ title: string; type: string; url: string }>
    paid: Array<{ title: string; platform: string; cost: string; url: string }>
  }
  estimated_time: string
  hands_on_project: string
  status: string
}

interface SkillGapsProps {
  gaps: SkillGap[]
  summary?: {
    total_gaps: number
    high_priority: number
    medium_priority: number
    recommended_focus_order: string[]
  }
}

export default function SkillGaps({ gaps, summary }: SkillGapsProps) {
  const [expandedGap, setExpandedGap] = useState<number | null>(null)

  const getPriorityStyle = (priority: string) => {
    switch (priority.toUpperCase()) {
      case 'HIGH': return { 
        gradient: 'from-red-500/30 to-rose-500/30', 
        border: 'border-red-400/40',
        text: 'text-red-300',
        glow: 'rgba(239, 68, 68, 0.3)'
      }
      case 'MEDIUM': return { 
        gradient: 'from-yellow-500/30 to-orange-500/30', 
        border: 'border-yellow-400/40',
        text: 'text-yellow-300',
        glow: 'rgba(245, 158, 11, 0.3)'
      }
      case 'LOW': return { 
        gradient: 'from-green-500/30 to-emerald-500/30', 
        border: 'border-green-400/40',
        text: 'text-green-300',
        glow: 'rgba(34, 197, 94, 0.3)'
      }
      default: return { 
        gradient: 'from-purple-500/30 to-indigo-500/30', 
        border: 'border-purple-400/40',
        text: 'text-purple-300',
        glow: 'rgba(168, 85, 247, 0.3)'
      }
    }
  }

  const getPriorityEmoji = (priority: string) => {
    switch (priority.toUpperCase()) {
      case 'HIGH': return '🔥'
      case 'MEDIUM': return '⚡'
      case 'LOW': return '🌱'
      default: return '📚'
    }
  }

  if (!gaps || gaps.length === 0) return null

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="hq-panel p-6 space-y-6"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <motion.span 
            className="text-3xl"
            animate={{ rotate: [0, 10, -10, 0], y: [0, -5, 0] }}
            transition={{ duration: 3, repeat: Infinity }}
          >
            🏝️
          </motion.span>
          <div>
            <h3 className="text-xl font-bold text-white font-display">Skill Islands</h3>
            <p className="text-purple-300 text-sm">Your journey to mastery</p>
          </div>
        </div>
        <span className="text-purple-400/50 text-xs px-3 py-1 rounded-full bg-purple-500/10 border border-purple-400/20">
          Powered by Yutori
        </span>
      </div>

      {/* Summary Stats - Styled as floating orbs */}
      {summary && (
        <div className="grid grid-cols-3 gap-4">
          <motion.div 
            className="hq-panel-sm p-4 text-center"
            whileHover={{ scale: 1.05, y: -5 }}
          >
            <motion.div 
              className="text-3xl font-bold text-white font-display"
              animate={{ scale: [1, 1.1, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              {summary.total_gaps}
            </motion.div>
            <div className="text-purple-300 text-xs">Total Islands</div>
          </motion.div>
          <motion.div 
            className="p-4 text-center rounded-xl bg-gradient-to-br from-red-500/20 to-rose-500/20 border border-red-400/30"
            whileHover={{ scale: 1.05, y: -5, boxShadow: '0 10px 30px rgba(239, 68, 68, 0.3)' }}
          >
            <motion.div 
              className="text-3xl font-bold text-red-400 font-display"
              animate={{ scale: [1, 1.15, 1] }}
              transition={{ duration: 1.5, repeat: Infinity }}
            >
              {summary.high_priority}
            </motion.div>
            <div className="text-red-300/70 text-xs">🔥 High Priority</div>
          </motion.div>
          <motion.div 
            className="p-4 text-center rounded-xl bg-gradient-to-br from-yellow-500/20 to-orange-500/20 border border-yellow-400/30"
            whileHover={{ scale: 1.05, y: -5, boxShadow: '0 10px 30px rgba(245, 158, 11, 0.3)' }}
          >
            <motion.div 
              className="text-3xl font-bold text-yellow-400 font-display"
              animate={{ scale: [1, 1.1, 1] }}
              transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
            >
              {summary.medium_priority}
            </motion.div>
            <div className="text-yellow-300/70 text-xs">⚡ Medium Priority</div>
          </motion.div>
        </div>
      )}

      {/* Skill Gaps List - Styled as floating islands */}
      <div className="space-y-4">
        {gaps.map((gap, index) => {
          const style = getPriorityStyle(gap.priority)
          return (
            <motion.div
              key={gap.id}
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.08 }}
              className={`rounded-xl border overflow-hidden bg-gradient-to-r ${style.gradient} ${style.border}`}
              whileHover={{ scale: 1.01 }}
            >
              {/* Header - Always Visible */}
              <button
                onClick={() => setExpandedGap(expandedGap === gap.id ? null : gap.id)}
                className="w-full p-4 flex items-center justify-between hover:bg-white/5 transition text-left"
              >
                <div className="flex items-center gap-4">
                  <motion.span 
                    className="text-2xl"
                    animate={{ y: [0, -3, 0] }}
                    transition={{ duration: 2, repeat: Infinity, delay: index * 0.2 }}
                  >
                    {getPriorityEmoji(gap.priority)}
                  </motion.span>
                  <div>
                    <h4 className="font-bold text-white">{gap.topic}</h4>
                    <p className="text-purple-200/60 text-xs">{gap.current_state}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`px-3 py-1 rounded-full text-xs font-bold ${style.text} bg-white/10`}>
                    {gap.priority}
                  </span>
                  <motion.span 
                    className="text-purple-300"
                    animate={{ rotate: expandedGap === gap.id ? 180 : 0 }}
                  >
                    ▼
                  </motion.span>
                </div>
              </button>

              {/* Expanded Content */}
              <AnimatePresence>
                {expandedGap === gap.id && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                    className="border-t border-white/10 overflow-hidden"
                  >
                    <div className="p-5 space-y-4">
                      {/* Target Skills */}
                      <div>
                        <span className="text-purple-300 text-xs font-medium block mb-2">🎯 Skills to Unlock:</span>
                        <div className="flex flex-wrap gap-2">
                          {gap.target_skills.map((skill, i) => (
                            <motion.span 
                              key={i} 
                              className="px-3 py-1 rounded-full bg-gradient-to-r from-cyan-500/30 to-blue-500/30 border border-cyan-400/30 text-cyan-200 text-xs font-medium"
                              initial={{ opacity: 0, scale: 0 }}
                              animate={{ opacity: 1, scale: 1 }}
                              transition={{ delay: i * 0.1 }}
                            >
                              {skill}
                            </motion.span>
                          ))}
                        </div>
                      </div>

                      {/* Time Estimate */}
                      <div className="flex items-center gap-3 p-3 rounded-xl bg-white/5">
                        <span className="text-xl">⏱️</span>
                        <div>
                          <span className="text-purple-300 text-xs">Estimated Time:</span>
                          <p className="text-white font-medium">{gap.estimated_time}</p>
                        </div>
                      </div>

                      {/* Resources */}
                      <div className="grid grid-cols-2 gap-4">
                        {/* Free Resources */}
                        <motion.div 
                          className="rounded-xl p-4 bg-gradient-to-br from-green-500/20 to-emerald-500/20 border border-green-400/30"
                          whileHover={{ scale: 1.02 }}
                        >
                          <span className="text-green-300 text-sm font-bold flex items-center gap-2 mb-3">
                            <span>🆓</span> Free Resources
                          </span>
                          {gap.resources.free.map((resource, i) => (
                            <motion.a
                              key={i}
                              href={resource.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="block text-green-100/80 text-sm hover:text-green-300 transition mb-2 p-2 rounded-lg hover:bg-white/5"
                              whileHover={{ x: 5 }}
                            >
                              <span className="font-medium">{resource.title}</span>
                              <span className="text-green-300/50 text-xs ml-1">({resource.type})</span>
                            </motion.a>
                          ))}
                        </motion.div>

                        {/* Paid Resources */}
                        <motion.div 
                          className="rounded-xl p-4 bg-gradient-to-br from-purple-500/20 to-pink-500/20 border border-purple-400/30"
                          whileHover={{ scale: 1.02 }}
                        >
                          <span className="text-purple-300 text-sm font-bold flex items-center gap-2 mb-3">
                            <span>💎</span> Premium Resources
                          </span>
                          {gap.resources.paid.map((resource, i) => (
                            <motion.a
                              key={i}
                              href={resource.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="block text-purple-100/80 text-sm hover:text-purple-300 transition mb-2 p-2 rounded-lg hover:bg-white/5"
                              whileHover={{ x: 5 }}
                            >
                              <span className="font-medium">{resource.title}</span>
                              <span className="text-purple-300/50 text-xs ml-1">{resource.cost}</span>
                            </motion.a>
                          ))}
                        </motion.div>
                      </div>

                      {/* Hands-on Project */}
                      <motion.div 
                        className="rounded-xl p-4 bg-gradient-to-r from-yellow-500/20 to-orange-500/20 border border-yellow-400/30"
                        whileHover={{ borderColor: 'rgba(251, 191, 36, 0.5)' }}
                      >
                        <span className="text-yellow-300 text-sm font-bold flex items-center gap-2 mb-2">
                          <motion.span
                            animate={{ rotate: [0, 20, -20, 0] }}
                            transition={{ duration: 2, repeat: Infinity }}
                          >
                            🛠️
                          </motion.span>
                          Build This Project:
                        </span>
                        <p className="text-yellow-100/80 text-sm leading-relaxed">{gap.hands_on_project}</p>
                      </motion.div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          )
        })}
      </div>

      {/* Recommended Focus Order - Journey Path */}
      {summary?.recommended_focus_order && (
        <motion.div 
          className="hq-panel-sm p-5"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <span className="text-purple-300 text-sm font-bold flex items-center gap-2 mb-4">
            <motion.span
              animate={{ x: [0, 5, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              🗺️
            </motion.span>
            Recommended Journey:
          </span>
          <div className="flex flex-wrap items-center gap-2">
            {summary.recommended_focus_order.map((topic, i) => (
              <motion.div 
                key={i} 
                className="flex items-center gap-2"
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.1 }}
              >
                <span className="w-7 h-7 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 text-white text-xs font-bold flex items-center justify-center shadow-lg">
                  {i + 1}
                </span>
                <span className="text-white/90 text-sm font-medium">{topic}</span>
                {i < summary.recommended_focus_order.length - 1 && (
                  <motion.span 
                    className="text-purple-400 mx-1"
                    animate={{ x: [0, 3, 0] }}
                    transition={{ duration: 1, repeat: Infinity, delay: i * 0.2 }}
                  >
                    →
                  </motion.span>
                )}
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}
    </motion.div>
  )
}
