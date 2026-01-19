import { motion } from 'framer-motion'

interface JobCardProps {
  job: {
    company: string
    title: string
    location?: string
    salary_range?: string
    apply_url?: string
    description?: string
    key_requirements?: string[]
    match_reason: string
    skill_gaps: string[]
    why_apply?: string
    source?: string
  }
}

export default function JobCard({ job }: JobCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      className="hq-panel p-6 hover:border-yellow-500/40 transition-all duration-300"
      whileHover={{ scale: 1.01 }}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-1">
            <motion.span 
              className="text-2xl"
              animate={{ rotate: [0, 10, -10, 0] }}
              transition={{ duration: 3, repeat: Infinity }}
            >
              🏢
            </motion.span>
            <span className="text-yellow-400 font-bold text-lg font-display">{job.company}</span>
          </div>
          <h4 className="text-xl font-bold text-white pl-10">{job.title}</h4>
        </div>
        {job.apply_url && (
          <motion.a
            href={job.apply_url}
            target="_blank"
            rel="noopener noreferrer"
            className="console-btn console-btn-joy text-sm"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <span className="flex items-center gap-2">
              🚀 Apply Now
            </span>
          </motion.a>
        )}
      </div>

      {/* Location and Salary */}
      <div className="flex items-center gap-4 text-sm mb-4 pl-10">
        {job.location && (
          <motion.span 
            className="flex items-center gap-2 px-3 py-1 rounded-full bg-gradient-to-r from-cyan-500/20 to-blue-500/20 border border-cyan-400/30 text-cyan-200"
            whileHover={{ scale: 1.05 }}
          >
            📍 {job.location}
          </motion.span>
        )}
        {job.salary_range && (
          <motion.span 
            className="flex items-center gap-2 px-3 py-1 rounded-full bg-gradient-to-r from-green-500/20 to-emerald-500/20 border border-green-400/30 text-green-200"
            whileHover={{ scale: 1.05 }}
          >
            💰 {job.salary_range}
          </motion.span>
        )}
      </div>

      {/* Description */}
      {job.description && (
        <p className="text-purple-200/70 text-sm mb-4 pl-10">
          {job.description}
        </p>
      )}

      {/* Key Requirements */}
      {job.key_requirements && job.key_requirements.length > 0 && (
        <div className="mb-4 pl-10">
          <span className="text-purple-300 text-xs font-medium block mb-2">📋 Key Requirements:</span>
          <div className="flex flex-wrap gap-2">
            {job.key_requirements.slice(0, 4).map((req, i) => (
              <motion.span
                key={i}
                className="px-3 py-1 rounded-full bg-purple-500/20 border border-purple-400/30 text-purple-200 text-xs"
                initial={{ opacity: 0, scale: 0 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.1 }}
              >
                {req}
              </motion.span>
            ))}
          </div>
        </div>
      )}

      {/* Match Reason - Joy's recommendation */}
      <motion.div 
        className="rounded-xl p-4 mb-4 bg-gradient-to-r from-green-500/20 to-emerald-500/20 border border-green-400/30"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <div className="flex items-center gap-2 mb-2">
          <motion.span 
            className="text-xl"
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          >
            ✨
          </motion.span>
          <span className="text-green-300 font-bold">Why Joy thinks this is perfect:</span>
        </div>
        <p className="text-green-100/80 text-sm leading-relaxed">{job.match_reason}</p>
      </motion.div>

      {/* Why Apply */}
      {job.why_apply && (
        <motion.div 
          className="rounded-xl p-4 mb-4 bg-gradient-to-r from-yellow-500/20 to-orange-500/20 border border-yellow-400/30"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xl">💡</span>
            <span className="text-yellow-300 font-bold">Why you should apply:</span>
          </div>
          <p className="text-yellow-100/80 text-sm leading-relaxed">{job.why_apply}</p>
        </motion.div>
      )}

      {/* Skill Gaps - Growth opportunities */}
      {job.skill_gaps && job.skill_gaps.length > 0 && (
        <div className="pl-10">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-lg">🎯</span>
            <span className="text-purple-300 text-xs font-medium">Growth Opportunities:</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {job.skill_gaps.map((skill, i) => (
              <motion.span
                key={i}
                className="px-3 py-1 rounded-full bg-gradient-to-r from-orange-500/20 to-red-500/20 border border-orange-400/30 text-orange-200 text-xs font-medium"
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 * i }}
                whileHover={{ scale: 1.1, borderColor: 'rgba(251, 146, 60, 0.5)' }}
              >
                {skill}
              </motion.span>
            ))}
          </div>
        </div>
      )}

      {/* Source badge */}
      {job.source && (
        <div className="mt-4 pt-4 border-t border-purple-500/20 flex justify-end">
          <span className="text-purple-400/50 text-xs flex items-center gap-1">
            <span>🔍</span> Found via {job.source.replace('_', ' ')}
          </span>
        </div>
      )}
    </motion.div>
  )
}
