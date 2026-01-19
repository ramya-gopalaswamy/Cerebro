import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

interface BrowserViewProps {
  viewUrl: string | null
  taskId: string | null
  status: 'idle' | 'running' | 'completed' | 'error'
  title: string
  onClose?: () => void
}

export default function BrowserView({ 
  viewUrl, 
  taskId, 
  status, 
  title,
  onClose 
}: BrowserViewProps) {
  const [isExpanded, setIsExpanded] = useState(true)

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="glass rounded-xl overflow-hidden"
    >
      {/* Browser Chrome */}
      <div className="flex items-center justify-between px-4 py-3 bg-gray-900/80 border-b border-white/10">
        <div className="flex items-center gap-3">
          {/* Traffic lights */}
          <div className="flex gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500 cursor-pointer hover:brightness-110" onClick={onClose} />
            <div className="w-3 h-3 rounded-full bg-yellow-500" />
            <div className="w-3 h-3 rounded-full bg-green-500 cursor-pointer hover:brightness-110" onClick={() => setIsExpanded(!isExpanded)} />
          </div>
          
          {/* Status indicator */}
          <div className="flex items-center gap-2 ml-4">
            {status === 'running' && (
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                className="w-4 h-4 border-2 border-indigo-500 border-t-transparent rounded-full"
              />
            )}
            {status === 'completed' && <span className="text-green-400">✓</span>}
            {status === 'error' && <span className="text-red-400">✗</span>}
            <span className="text-white/60 text-sm">{title}</span>
          </div>
        </div>
        
        {/* URL bar */}
        <div className="flex-1 mx-4 px-3 py-1.5 bg-black/40 rounded-lg">
          <span className="text-white/40 text-sm font-mono">
            {viewUrl ? new URL(viewUrl).hostname : 'Waiting for browser...'}
          </span>
        </div>
        
        {taskId && (
          <span className="text-white/30 text-xs">ID: {taskId.slice(0, 8)}...</span>
        )}
      </div>

      {/* Browser Content */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0 }}
            animate={{ height: 'auto' }}
            exit={{ height: 0 }}
            className="relative"
          >
            {viewUrl ? (
              <iframe
                src={viewUrl}
                className="w-full h-[500px] bg-gray-900"
                sandbox="allow-scripts allow-same-origin"
                title={title}
              />
            ) : (
              <div className="w-full h-[500px] bg-gray-900 flex flex-col items-center justify-center">
                {status === 'idle' && (
                  <>
                    <div className="text-6xl mb-4">🌐</div>
                    <p className="text-white/50">Browser not started</p>
                    <p className="text-white/30 text-sm mt-2">Click "Start" to begin automation</p>
                  </>
                )}
                {status === 'running' && !viewUrl && (
                  <>
                    <motion.div
                      animate={{ scale: [1, 1.2, 1] }}
                      transition={{ duration: 1.5, repeat: Infinity }}
                      className="text-6xl mb-4"
                    >
                      🤖
                    </motion.div>
                    <p className="text-white/50">Launching browser...</p>
                    <div className="flex gap-1 mt-4">
                      <motion.div
                        animate={{ opacity: [0.3, 1, 0.3] }}
                        transition={{ duration: 1, repeat: Infinity, delay: 0 }}
                        className="w-2 h-2 bg-indigo-500 rounded-full"
                      />
                      <motion.div
                        animate={{ opacity: [0.3, 1, 0.3] }}
                        transition={{ duration: 1, repeat: Infinity, delay: 0.2 }}
                        className="w-2 h-2 bg-indigo-500 rounded-full"
                      />
                      <motion.div
                        animate={{ opacity: [0.3, 1, 0.3] }}
                        transition={{ duration: 1, repeat: Infinity, delay: 0.4 }}
                        className="w-2 h-2 bg-indigo-500 rounded-full"
                      />
                    </div>
                  </>
                )}
              </div>
            )}
            
            {/* Live indicator overlay */}
            {status === 'running' && viewUrl && (
              <div className="absolute top-4 right-4 flex items-center gap-2 px-3 py-1.5 bg-red-600 rounded-full">
                <motion.div
                  animate={{ opacity: [1, 0.5, 1] }}
                  transition={{ duration: 1, repeat: Infinity }}
                  className="w-2 h-2 bg-white rounded-full"
                />
                <span className="text-white text-xs font-bold">LIVE</span>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}
