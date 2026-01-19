/**
 * SVG Glass Jar component for orbs
 */
import React from 'react';

interface JarProps {
  width?: number;
  height?: number;
  className?: string;
  children?: React.ReactNode;
}

const Jar: React.FC<JarProps> = ({ width = 200, height = 300, className = '', children }) => {
  return (
    <div className={`relative inline-block ${className}`}>
      <svg
        width={width}
        height={height}
        viewBox="0 0 200 300"
        className="drop-shadow-lg"
      >
        <defs>
          <linearGradient id="glassGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="rgba(255, 255, 255, 0.2)" />
            <stop offset="100%" stopColor="rgba(255, 255, 255, 0.05)" />
          </linearGradient>
          <filter id="glassBlur">
            <feGaussianBlur in="SourceGraphic" stdDeviation="2" />
          </filter>
        </defs>
        
        {/* Jar body - glass effect */}
        <path
          d="M 60 40 L 60 260 Q 60 280 80 280 L 120 280 Q 140 280 140 260 L 140 40 Q 140 20 120 20 L 80 20 Q 60 20 60 40 Z"
          fill="url(#glassGradient)"
          stroke="rgba(255, 255, 255, 0.3)"
          strokeWidth="2"
          className="glass"
          style={{ backdropFilter: 'blur(10px)' }}
        />
        
        {/* Jar rim */}
        <ellipse
          cx="100"
          cy="40"
          rx="40"
          ry="5"
          fill="rgba(255, 255, 255, 0.4)"
          stroke="rgba(255, 255, 255, 0.5)"
          strokeWidth="1"
        />
        
        {/* Jar base */}
        <ellipse
          cx="100"
          cy="275"
          rx="35"
          ry="8"
          fill="rgba(255, 255, 255, 0.3)"
          stroke="rgba(255, 255, 255, 0.4)"
          strokeWidth="1"
        />
        
        {/* Reflection/highlight */}
        <ellipse
          cx="75"
          cy="80"
          rx="15"
          ry="60"
          fill="rgba(255, 255, 255, 0.15)"
          opacity="0.5"
        />
      </svg>
      
      {/* Orbs container (absolute positioned) */}
      <div className="absolute inset-0 flex items-end justify-center pb-8">
        <div className="relative w-full h-full">
          {children}
        </div>
      </div>
    </div>
  );
};

export default Jar;
