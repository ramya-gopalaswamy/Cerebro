import { motion, AnimatePresence } from 'framer-motion'

interface Orb {
  type?: string
  emotion?: string
  color?: string
  task_type?: string
  reason: string
  image_url?: string
  colors?: { primary: string; glow: string }
}

interface OrbJarProps {
  orbs: Orb[]
}

const ORB_CONFIG: Record<string, { emoji: string; label: string; gradient: string; glow: string }> = {
  joy: { 
    emoji: '😊', 
    label: 'Joy', 
    gradient: 'from-yellow-400 to-orange-400',
    glow: 'rgba(255, 215, 0, 0.6)'
  },
  sadness: { 
    emoji: '😢', 
    label: 'Sadness', 
    gradient: 'from-blue-400 to-blue-600',
    glow: 'rgba(91, 141, 217, 0.6)'
  },
  anger: { 
    emoji: '😤', 
    label: 'Anger', 
    gradient: 'from-red-500 to-red-700',
    glow: 'rgba(229, 57, 53, 0.6)'
  },
  anxiety: { 
    emoji: '😰', 
    label: 'Anxiety', 
    gradient: 'from-purple-400 to-purple-600',
    glow: 'rgba(156, 39, 176, 0.6)'
  },
  disgust: { 
    emoji: '🤢', 
    label: 'Disgust', 
    gradient: 'from-green-400 to-green-600',
    glow: 'rgba(76, 175, 80, 0.6)'
  }
}

export default function OrbJar({ orbs }: OrbJarProps) {
  const getOrbType = (orb: Orb) => orb.type || orb.emotion || 'joy'
  const joyCount = orbs.filter(o => getOrbType(o) === 'joy').length

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="hq-panel p-6"
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <motion.span 
            className="text-3xl"
            animate={{ rotate: [0, 10, -10, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            🏺
          </motion.span>
          <div>
            <h3 className="text-lg font-bold text-white font-display">Memory Jar</h3>
            <p className="text-purple-300 text-xs">Core Memories</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <motion.span 
            className="text-yellow-400 font-bold"
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ duration: 1, repeat: Infinity }}
          >
            {joyCount} ✨
          </motion.span>
          <span className="text-purple-300 text-sm">| {orbs.length} total</span>
        </div>
      </div>

      {/* Jar Visualization - Styled like Inside Out memory containers */}
      <div className="relative h-56 memory-jar overflow-hidden">
        {/* Jar lid */}
        <div className="absolute -top-1 left-1/2 -translate-x-1/2 w-3/4 h-6 bg-gradient-to-b from-white/30 to-white/10 rounded-t-lg border-x-2 border-t-2 border-white/30 z-10" />
        
        {/* Inner glow effect */}
        <div className="absolute inset-0 bg-gradient-to-t from-purple-500/20 via-transparent to-transparent" />
        
        {/* Light reflection on glass */}
        <div className="absolute top-8 left-4 w-2 h-24 bg-gradient-to-b from-white/30 to-transparent rounded-full" />
        
        {/* Orbs container */}
        <div className="absolute inset-4 top-8 flex flex-wrap content-end justify-center gap-3 p-3">
          <AnimatePresence>
            {orbs.map((orb, i) => {
              const orbType = getOrbType(orb)
              const config = ORB_CONFIG[orbType] || ORB_CONFIG.joy
              
              return (
                <motion.div
                  key={i}
                  initial={{ scale: 0, y: -100, opacity: 0 }}
                  animate={{ 
                    scale: 1, 
                    y: 0,
                    opacity: 1,
                  }}
                  transition={{ 
                    type: 'spring', 
                    stiffness: 200, 
                    damping: 15, 
                    delay: i * 0.15 
                  }}
                  whileHover={{ 
                    scale: 1.3, 
                    zIndex: 20,
                    boxShadow: `0 0 40px 15px ${config.glow}`
                  }}
                  className={`memory-orb w-12 h-12 flex items-center justify-center cursor-pointer relative bg-gradient-to-br ${config.gradient}`}
                  style={{
                    boxShadow: `0 0 20px 8px ${config.glow}, inset 0 0 15px rgba(255,255,255,0.3)`,
                  }}
                  title={orb.reason}
                >
                  <motion.span 
                    className="text-xl relative z-10"
                    animate={{ 
                      y: [0, -3, 0],
                    }}
                    transition={{ 
                      duration: 2, 
                      repeat: Infinity,
                      delay: i * 0.3 
                    }}
                  >
                    {config.emoji}
                  </motion.span>
                </motion.div>
              )
            })}
          </AnimatePresence>
        </div>

        {/* Empty state */}
        {orbs.length === 0 && (
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <motion.span 
              className="text-5xl mb-3 opacity-30"
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              🌟
            </motion.span>
            <p className="text-purple-300/50 text-sm text-center px-4">
              Complete tasks to create<br/>core memories!
            </p>
          </div>
        )}
      </div>

      {/* Emotion Legend */}
      <div className="mt-4 flex flex-wrap justify-center gap-2">
        {['joy', 'sadness', 'anger', 'anxiety', 'disgust'].map((emotion) => {
          const config = ORB_CONFIG[emotion]
          return (
            <div 
              key={emotion} 
              className="flex items-center gap-1 px-2 py-1 rounded-full bg-white/5 text-xs"
            >
              <span>{config.emoji}</span>
              <span className="text-purple-200">{config.label}</span>
            </div>
          )
        })}
      </div>

      {/* Recent orb details */}
      {orbs.length > 0 && (
        <div className="mt-4 space-y-2">
          <h4 className="text-sm text-purple-300 font-medium flex items-center gap-2">
            <span>📜</span> Recent Memories
          </h4>
          {orbs.slice(-3).reverse().map((orb, i) => {
            const orbType = getOrbType(orb)
            const config = ORB_CONFIG[orbType] || ORB_CONFIG.joy
            
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.1 }}
                className="flex items-start gap-3 p-3 rounded-xl hq-panel-sm"
              >
                <motion.span 
                  className="text-xl"
                  animate={{ scale: [1, 1.1, 1] }}
                  transition={{ duration: 1.5, repeat: Infinity, delay: i * 0.2 }}
                >
                  {config.emoji}
                </motion.span>
                <div className="flex-1 min-w-0">
                  <span className="text-purple-200 text-xs font-medium capitalize">{config.label}</span>
                  <p className="text-white/80 text-sm truncate">{orb.reason}</p>
                </div>
              </motion.div>
            )
          })}
        </div>
      )}
    </motion.div>
  )
}
