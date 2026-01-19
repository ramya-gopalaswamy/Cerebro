import React from 'react';
import { Briefcase, Code } from 'lucide-react';

export interface ProgressTrackProps {
  title: string;
  icon: 'briefcase' | 'code';
  color: 'blue' | 'green';
  completed: number;
  total: number;
  avatarEmoji?: string;
  avatarImage?: string; // new prop for image
  showTarget?: boolean;
}

export function ProgressTrack({ 
  title, 
  icon, 
  color, 
  completed, 
  total, 
  avatarEmoji,
  avatarImage,
  showTarget = false 
}: ProgressTrackProps) {
  const IconComponent = icon === 'briefcase' ? Briefcase : Code;
  
  const colorStyles = {
    blue: {
      glow: 'rgba(100, 181, 246, 0.6)',
      gradient: 'linear-gradient(90deg, #42a5f5 0%, #1e88e5 100%)',
      badge: 'linear-gradient(135deg, #29b6f6 0%, #039be5 100%)',
      icon: '#81d4fa'
    },
    green: {
      glow: 'rgba(129, 199, 132, 0.6)',
      gradient: 'linear-gradient(90deg, #66bb6a 0%, #43a047 100%)',
      badge: 'linear-gradient(135deg, #66bb6a 0%, #388e3c 100%)',
      icon: '#a5d6a7'
    }
  };

  const styles = colorStyles[color];

  return (
    <div className="relative">
      {/* Title */}
      <div className="flex items-center gap-3 mb-4">
        <div className="flex items-center gap-2 px-4 py-2 rounded-full"
          style={{
            background: styles.gradient,
            boxShadow: `0 4px 12px ${styles.glow}`
          }}>
          <IconComponent className="w-8 h-8 text-white" />
          <span className="text-xl md:text-2xl font-bold text-white tracking-wide"
            style={{ textShadow: '0 2px 4px rgba(0, 0, 0, 0.3)' }}>
            {title}
          </span>
        </div>
      </div>

      {/* Progress Track */}
      <div className="relative flex items-center gap-4 pl-8">
        {/* Track Line */}
        <div className="flex-1 relative flex items-center gap-3">
          {Array.from({ length: total }).map((_, index) => {
            const isCompleted = index < completed;
            const isCurrent = index === completed;
            const isLast = index === total - 1;
            return (
              <div key={index} className="relative flex items-center flex-1">
                {/* Node */}
                <div className="relative z-10 flex items-center justify-center"
                  style={{
                    width: isCurrent ? '72px' : '56px',
                    height: isCurrent ? '72px' : '56px',
                    transition: 'all 0.3s ease'
                  }}>
                  {/* Avatar image for last node if provided */}
                  {isLast && avatarImage ? (
                    <img src={avatarImage} alt="avatar" className="w-16 h-16 rounded-full border-4 border-white bg-white/80 shadow-xl object-cover" />
                  ) : (
                    <div className="absolute inset-0 rounded-full"
                      style={{
                        background: isCompleted || isCurrent ? styles.badge : 'rgba(255, 255, 255, 0.2)',
                        boxShadow: isCurrent 
                          ? `0 0 30px ${styles.glow}, 0 4px 12px rgba(0, 0, 0, 0.3)`
                          : isCompleted 
                            ? `0 0 15px ${styles.glow}`
                            : 'none',
                        border: '3px solid rgba(255, 255, 255, 0.4)'
                      }}>
                    </div>
                  )}
                  <div className="relative z-10 flex items-center justify-center">
                    {isLast && avatarImage ? null : isCurrent ? (
                      <span className="text-2xl font-black text-white"
                        style={{ textShadow: '0 2px 4px rgba(0, 0, 0, 0.5)' }}>
                        {completed}
                      </span>
                    ) : (
                      <IconComponent 
                        className="text-white" 
                        size={isCompleted ? 28 : 24}
                        style={{ 
                          opacity: isCompleted ? 1 : 0.5,
                          filter: isCompleted ? 'drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3))' : 'none'
                        }} 
                      />
                    )}
                  </div>
                </div>
                {/* Connector Line */}
                {index < total - 1 && (
                  <div className="flex-1 h-3 rounded-full mx-2"
                    style={{
                      background: index < completed 
                        ? styles.gradient
                        : 'rgba(255, 255, 255, 0.2)',
                      boxShadow: index < completed 
                        ? `0 0 10px ${styles.glow}`
                        : 'none',
                      transition: 'all 0.3s ease'
                    }}>
                  </div>
                )}
              </div>
            );
          })}
        </div>
        {/* Avatar Emoji (legacy, if no image) */}
        {avatarImage ? null : (
          <div className="flex-shrink-0 w-20 h-20 rounded-full flex items-center justify-center text-4xl"
            style={{
              background: 'linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1))',
              border: '3px solid rgba(255, 255, 255, 0.3)',
              boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)'
            }}>
            {avatarEmoji}
          </div>
        )}
      </div>
      {/* Target Speech Bubble */}
      {showTarget && (
        <div className="absolute top-0 right-0 -mt-8 mr-16">
          <div className="relative bg-white rounded-3xl px-6 py-4 shadow-lg"
            style={{
              boxShadow: '0 4px 16px rgba(0, 0, 0, 0.2)'
            }}>
            <p className="text-sm font-bold text-purple-900 text-center leading-tight">
              YOUR DAILY TARGETS:<br />
              <span className="text-base">3 JOB APPLICATIONS +<br />1 LEETCODE PROBLEM</span>
            </p>
            {/* Speech bubble tail */}
            <div className="absolute bottom-0 right-8 translate-y-full">
              <div className="relative">
                <div className="w-6 h-6 bg-white rounded-full -mt-3"></div>
                <div className="w-4 h-4 bg-white rounded-full -mt-2 ml-4"></div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
