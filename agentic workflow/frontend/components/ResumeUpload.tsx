import { useState, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

interface ResumeUploadProps {
  onUploaded: (resumeId: string, parsed: any) => void
  apiBase: string
}

export default function ResumeUpload({ onUploaded, apiBase }: ResumeUploadProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [uploadStage, setUploadStage] = useState(0) // 0-3 for different emotions

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
  }, [])

  const handleDragIn = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }, [])

  const handleDragOut = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
    
    const files = e.dataTransfer.files
    if (files && files.length > 0) {
      handleFile(files[0])
    }
  }, [])

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      handleFile(files[0])
    }
  }

  const handleFile = async (file: File) => {
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setError('Please upload a PDF file')
      return
    }

    setIsUploading(true)
    setError(null)
    setUploadStage(0)
    setUploadProgress('Joy is receiving your resume...')

    const formData = new FormData()
    formData.append('file', file)

    try {
      await new Promise(resolve => setTimeout(resolve, 800))
      setUploadStage(1)
      setUploadProgress('Fear is checking the document format...')
      
      const response = await fetch(`${apiBase}/api/resume/upload`, {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail || 'Upload failed')
      }

      setUploadStage(2)
      setUploadProgress('Sadness is carefully reading every detail...')
      await new Promise(resolve => setTimeout(resolve, 600))
      
      const data = await response.json()
      
      setUploadStage(3)
      setUploadProgress('Joy found something amazing! ✨')
      
      // Short delay to show completion
      setTimeout(() => {
        onUploaded(data.resume_id, data.parsed)
      }, 800)

    } catch (err: any) {
      setError(err.message || 'Failed to upload resume')
      setIsUploading(false)
    }
  }

  const emotionEmojis = ['😊', '😰', '😢', '😊']
  const emotionColors = [
    'from-yellow-400 to-orange-400',
    'from-purple-400 to-violet-400',
    'from-blue-400 to-cyan-400',
    'from-yellow-400 to-orange-400'
  ]

  return (
    <div className="w-full max-w-lg">
      <motion.div
        onDragEnter={handleDragIn}
        onDragLeave={handleDragOut}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        animate={{
          borderColor: isDragging ? 'rgba(168, 85, 247, 0.8)' : 'rgba(168, 85, 247, 0.3)',
          boxShadow: isDragging 
            ? '0 0 40px 10px rgba(168, 85, 247, 0.3)' 
            : '0 0 20px 5px rgba(168, 85, 247, 0.1)'
        }}
        className="hq-panel border-2 border-dashed border-purple-500/40 p-12 text-center cursor-pointer transition-all duration-300"
      >
        <AnimatePresence mode="wait">
          {isUploading ? (
            <motion.div
              key="uploading"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              className="space-y-6"
            >
              {/* Animated emotion orb */}
              <motion.div 
                className={`w-24 h-24 mx-auto rounded-full bg-gradient-to-br ${emotionColors[uploadStage]} flex items-center justify-center`}
                animate={{ 
                  scale: [1, 1.1, 1],
                  rotate: [0, 5, -5, 0]
                }}
                transition={{ duration: 1, repeat: Infinity }}
                style={{ 
                  boxShadow: uploadStage === 3 
                    ? '0 0 40px 15px rgba(255, 215, 0, 0.5)' 
                    : '0 0 30px 10px rgba(168, 85, 247, 0.4)'
                }}
              >
                <motion.span 
                  className="text-5xl"
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ duration: 0.5, repeat: Infinity }}
                >
                  {emotionEmojis[uploadStage]}
                </motion.span>
              </motion.div>
              
              {/* Progress text */}
              <motion.p 
                className="text-purple-100 text-lg font-medium"
                key={uploadProgress}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                {uploadProgress}
              </motion.p>
              
              {/* Progress dots */}
              <div className="flex justify-center gap-2">
                {[0, 1, 2, 3].map((i) => (
                  <motion.div
                    key={i}
                    className={`w-3 h-3 rounded-full ${
                      i <= uploadStage 
                        ? 'bg-gradient-to-r from-yellow-400 to-orange-400' 
                        : 'bg-white/20'
                    }`}
                    animate={i === uploadStage ? { scale: [1, 1.3, 1] } : {}}
                    transition={{ duration: 0.5, repeat: Infinity }}
                  />
                ))}
              </div>
            </motion.div>
          ) : (
            <motion.div
              key="idle"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
            >
              {/* Floating document icon */}
              <motion.div 
                className="relative w-28 h-28 mx-auto mb-6"
                animate={{ y: [0, -10, 0] }}
                transition={{ duration: 3, repeat: Infinity }}
              >
                <motion.div 
                  className="absolute inset-0 rounded-2xl bg-gradient-to-br from-yellow-400/20 to-orange-400/20 border-2 border-yellow-400/30"
                  animate={{ rotate: [-5, 5, -5] }}
                  transition={{ duration: 4, repeat: Infinity }}
                />
                <motion.div 
                  className="absolute inset-2 rounded-xl bg-gradient-to-br from-purple-500/30 to-pink-500/30 border border-purple-400/40 flex items-center justify-center"
                  animate={{ rotate: [5, -5, 5] }}
                  transition={{ duration: 3, repeat: Infinity }}
                >
                  <span className="text-5xl">📄</span>
                </motion.div>
              </motion.div>
              
              <h3 className="text-white text-xl font-bold font-display mb-2">
                Drop Your Resume Here
              </h3>
              <p className="text-purple-200/60 text-sm mb-6">
                Joy is excited to learn about you! (PDF only)
              </p>
              
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileInput}
                className="hidden"
                id="resume-upload"
              />
              <motion.label
                htmlFor="resume-upload"
                className="console-btn console-btn-joy inline-flex items-center gap-2 cursor-pointer"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <span>✨</span>
                <span>Select File</span>
              </motion.label>
              
              {/* Sparkles */}
              <div className="flex justify-center gap-4 mt-6">
                {['✨', '🌟', '💫', '⭐', '✨'].map((spark, i) => (
                  <motion.span
                    key={i}
                    className="text-xl"
                    animate={{ 
                      y: [0, -10, 0],
                      opacity: [0.5, 1, 0.5]
                    }}
                    transition={{ 
                      duration: 1.5, 
                      delay: i * 0.2, 
                      repeat: Infinity 
                    }}
                  >
                    {spark}
                  </motion.span>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* Error message */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mt-4 p-4 rounded-xl bg-gradient-to-r from-red-500/20 to-rose-500/20 border border-red-400/30 text-center"
          >
            <span className="text-2xl mr-2">😤</span>
            <span className="text-red-200">{error}</span>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
