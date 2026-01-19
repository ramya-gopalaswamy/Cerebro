import { motion, AnimatePresence } from 'framer-motion'
import { useEffect, useRef } from 'react'

interface AgentThoughtsProps {
  thoughts: string[]
}

// Emotion detection for styling - Inside Out characters
const getEmotionFromThought = (thought: string) => {
  const lower = thought.toLowerCase()
  
  // Joy - success, completion, positive outcomes
  if (lower.includes('joy') || lower.includes('✨') || lower.includes('🌟') || lower.includes('success') || lower.includes('created') || lower.includes('found') || lower.includes('completed') || lower.includes('amazing')) {
    return { emoji: '😊', color: 'from-yellow-500/30 to-orange-500/30', border: 'border-yellow-400/40', text: 'text-yellow-200' }
  }
  
  // Sadness - checking, careful analysis, reflection
  if (lower.includes('sadness') || lower.includes('checking') || lower.includes('careful') || lower.includes('verif')) {
    return { emoji: '😢', color: 'from-blue-500/30 to-cyan-500/30', border: 'border-blue-400/40', text: 'text-blue-200' }
  }
  
  // Anger - errors, frustration, failures
  if (lower.includes('anger') || lower.includes('frustrat') || lower.includes('failed') || lower.includes('error') || lower.includes('❌')) {
    return { emoji: '😤', color: 'from-red-500/30 to-rose-500/30', border: 'border-red-400/40', text: 'text-red-200' }
  }
  
  // Anxiety - worry, fear, uncertainty
  if (lower.includes('anxiety') || lower.includes('fear') || lower.includes('worry') || lower.includes('😰') || lower.includes('uncertain')) {
    return { emoji: '😰', color: 'from-purple-500/30 to-violet-500/30', border: 'border-purple-400/40', text: 'text-purple-200' }
  }
  
  // Disgust - rejection, bad results
  if (lower.includes('disgust') || lower.includes('reject') || lower.includes('bad') || lower.includes('wrong')) {
    return { emoji: '🤢', color: 'from-green-500/30 to-emerald-500/30', border: 'border-green-400/40', text: 'text-green-200' }
  }
  
  // Searching
  if (lower.includes('search') || lower.includes('🔍') || lower.includes('looking')) {
    return { emoji: '🔍', color: 'from-cyan-500/30 to-blue-500/30', border: 'border-cyan-400/40', text: 'text-cyan-200' }
  }
  
  // Planning/Analyzing
  if (lower.includes('🧠') || lower.includes('plan') || lower.includes('analyzing') || lower.includes('thinking')) {
    return { emoji: '🧠', color: 'from-pink-500/30 to-purple-500/30', border: 'border-pink-400/40', text: 'text-pink-200' }
  }
  
  // Default - neutral thinking
  return { emoji: '💭', color: 'from-purple-500/20 to-indigo-500/20', border: 'border-purple-400/30', text: 'text-purple-200' }
}

export default function AgentThoughts({ thoughts }: AgentThoughtsProps) {
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: 'smooth'
    })
  }, [thoughts])

  if (thoughts.length === 0) return null

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="hq-panel p-5"
    >
      <div className="flex items-center gap-3 mb-4">
        <motion.div 
          className="w-10 h-10 rounded-full bg-gradient-to-br from-pink-400 to-purple-500 flex items-center justify-center shadow-lg"
          animate={{ scale: [1, 1.1, 1] }}
          transition={{ duration: 2, repeat: Infinity }}
          style={{ boxShadow: '0 0 20px rgba(219, 39, 119, 0.4)' }}
        >
          <span className="text-xl">🧠</span>
        </motion.div>
        <div>
          <h4 className="text-lg font-bold text-white font-display">Headquarters Console</h4>
          <p className="text-purple-300 text-xs">What the emotions are thinking...</p>
        </div>
        <motion.div 
          className="ml-auto flex gap-1"
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        >
          {/* Joy, Sadness, Anger, Anxiety, Disgust */}
          {['😊', '😢', '😤', '😰', '🤢'].map((emoji, i) => (
            <motion.span 
              key={i} 
              className="text-sm"
              animate={{ y: [0, -3, 0] }}
              transition={{ duration: 0.5, delay: i * 0.1, repeat: Infinity }}
            >
              {emoji}
            </motion.span>
          ))}
        </motion.div>
      </div>

      <div
        ref={scrollRef}
        className="max-h-72 overflow-y-auto space-y-2 pr-2"
      >
        <AnimatePresence>
          {thoughts.map((thought, i) => {
            const emotion = getEmotionFromThought(thought)
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -20, scale: 0.95 }}
                animate={{ opacity: 1, x: 0, scale: 1 }}
                transition={{ delay: i * 0.03, type: 'spring', stiffness: 200 }}
                className={`p-3 rounded-xl bg-gradient-to-r ${emotion.color} border ${emotion.border} relative overflow-hidden`}
              >
                {/* Shimmer effect */}
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full animate-shimmer" />
                
                <div className="flex items-start gap-3 relative">
                  <motion.span 
                    className="text-lg flex-shrink-0"
                    animate={{ scale: [1, 1.1, 1] }}
                    transition={{ duration: 1, delay: i * 0.1 }}
                  >
                    {emotion.emoji}
                  </motion.span>
                  <p className={`text-sm ${emotion.text} leading-relaxed`}>
                    {thought}
                  </p>
                </div>
              </motion.div>
            )
          })}
        </AnimatePresence>
      </div>

      {/* Active thinking indicator */}
      <motion.div 
        className="mt-4 flex items-center justify-center gap-2 text-purple-300 text-sm"
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 2, repeat: Infinity }}
      >
        <motion.span
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
        >
          ⚡
        </motion.span>
        <span>Emotions are processing...</span>
      </motion.div>
    </motion.div>
  )
}
