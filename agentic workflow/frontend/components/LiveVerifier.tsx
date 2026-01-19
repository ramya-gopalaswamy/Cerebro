import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

interface LiveVerifierProps {
  resumeId: string
  leetcodeUsername: string
  apiBase: string
  onComplete: (results: any[], orbs: any[]) => void
  onThought: (thought: string) => void
}

interface StreamEvent {
  type: string
  thought?: string
  source?: string
  result?: any
  orb?: any
  message?: string
  error?: string
}

export default function LiveVerifier({ 
  resumeId, 
  leetcodeUsername, 
  apiBase, 
  onComplete,
  onThought 
}: LiveVerifierProps) {
  const [isRunning, setIsRunning] = useState(false)
  const [events, setEvents] = useState<StreamEvent[]>([])
  const [currentAction, setCurrentAction] = useState<string>('')
  const [verificationResults, setVerificationResults] = useState<any[]>([])
  const [orbs, setOrbs] = useState<any[]>([])
  const eventsEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom
  useEffect(() => {
    eventsEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [events])

  const startVerification = async () => {
    setIsRunning(true)
    setEvents([])
    setVerificationResults([])
    setOrbs([])
    setCurrentAction('Connecting to agents...')

    try {
      const response = await fetch(`${apiBase}/api/verify/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_id: resumeId,
          leetcode_username: leetcodeUsername,
          targets: { leetcode: 5, applications: 2 }
        })
      })

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()

      if (!reader) throw new Error('No reader available')

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n').filter(line => line.startsWith('data: '))

        for (const line of lines) {
          try {
            const data = JSON.parse(line.replace('data: ', '')) as StreamEvent
            handleEvent(data)
          } catch (e) {
            console.error('Failed to parse event:', e)
          }
        }
      }
    } catch (error) {
      console.error('Verification failed:', error)
      setEvents(prev => [...prev, { type: 'error', error: String(error) }])
    } finally {
      setIsRunning(false)
      setCurrentAction('')
    }
  }

  const handleEvent = (event: StreamEvent) => {
    setEvents(prev => [...prev, event])

    switch (event.type) {
      case 'start':
        setCurrentAction(event.message || 'Starting...')
        break
      
      case 'thought':
        if (event.thought) {
          onThought(event.thought)
          setCurrentAction(event.thought)
        }
        break
      
      case 'verification_start':
        setCurrentAction(`Checking ${event.source}...`)
        break
      
      case 'verification_complete':
        if (event.result) {
          setVerificationResults(prev => [...prev, event.result])
        }
        break
      
      case 'orb_generating':
        setCurrentAction(`Generating ${event.emotion?.toUpperCase()} orb...`)
        break
      
      case 'orb_awarded':
        if (event.orb) {
          setOrbs(prev => [...prev, event.orb])
        }
        break
      
      case 'complete':
        setCurrentAction('Verification complete!')
        onComplete(verificationResults, orbs)
        break
      
      case 'error':
        setCurrentAction(`Error: ${event.error}`)
        break
    }
  }

  return (
    <div className="glass rounded-xl p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-bold text-white">Live Verification</h3>
        {!isRunning && (
          <button
            onClick={startVerification}
            className="px-6 py-2 rounded-lg bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-medium hover:from-indigo-500 hover:to-purple-500 transition"
          >
            🚀 Start Verification
          </button>
        )}
      </div>

      {/* Current Action */}
      {currentAction && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex items-center gap-3 p-4 rounded-lg bg-indigo-500/10 border border-indigo-500/30"
        >
          {isRunning && (
            <div className="w-5 h-5 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
          )}
          <span className="text-indigo-300">{currentAction}</span>
        </motion.div>
      )}

      {/* Event Stream */}
      <div className="h-80 overflow-y-auto space-y-2 p-4 rounded-lg bg-black/20">
        <AnimatePresence>
          {events.map((event, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className={`text-sm p-2 rounded ${getEventStyle(event.type)}`}
            >
              <span className="text-white/50 mr-2">[{event.type}]</span>
              <span className="text-white/80">
                {event.thought || event.message || JSON.stringify(event).slice(0, 100)}
              </span>
            </motion.div>
          ))}
        </AnimatePresence>
        <div ref={eventsEndRef} />
      </div>

      {/* Results Summary */}
      {verificationResults.length > 0 && (
        <div className="grid grid-cols-2 gap-4">
          {verificationResults.map((result, i) => (
            <div
              key={i}
              className={`p-4 rounded-lg ${
                result.count >= result.target
                  ? 'bg-green-500/10 border border-green-500/30'
                  : 'bg-yellow-500/10 border border-yellow-500/30'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-white font-medium capitalize">{result.source}</span>
                <span className={`text-2xl font-bold ${
                  result.count >= result.target ? 'text-green-400' : 'text-yellow-400'
                }`}>
                  {result.count}/{result.target}
                </span>
              </div>
              <p className="text-white/50 text-sm">
                {result.count >= result.target ? '✓ Target met!' : '○ Keep going!'}
              </p>
            </div>
          ))}
        </div>
      )}

      {/* Awarded Orbs */}
      {orbs.length > 0 && (
        <div className="space-y-3">
          <h4 className="text-white font-semibold">Orbs Awarded</h4>
          <div className="flex gap-4">
            {orbs.map((orb, i) => (
              <motion.div
                key={i}
                initial={{ scale: 0, rotate: -180 }}
                animate={{ scale: 1, rotate: 0 }}
                transition={{ type: 'spring', stiffness: 200 }}
                className={`w-16 h-16 rounded-full flex items-center justify-center orb-${orb.emotion}`}
                style={{
                  background: `radial-gradient(circle at 30% 30%, ${orb.colors?.primary || '#fff'}, ${orb.colors?.glow || '#888'})`
                }}
              >
                <span className="text-2xl">
                  {orb.emotion === 'joy' && '😊'}
                  {orb.emotion === 'sadness' && '😢'}
                  {orb.emotion === 'anger' && '😤'}
                  {orb.emotion === 'anxiety' && '😰'}
                  {orb.emotion === 'logic' && '🧠'}
                </span>
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function getEventStyle(type: string): string {
  switch (type) {
    case 'thought':
      return 'bg-indigo-500/10 border-l-2 border-indigo-500'
    case 'verification_complete':
      return 'bg-green-500/10 border-l-2 border-green-500'
    case 'orb_awarded':
      return 'bg-yellow-500/10 border-l-2 border-yellow-500'
    case 'error':
      return 'bg-red-500/10 border-l-2 border-red-500'
    default:
      return 'bg-white/5'
  }
}
