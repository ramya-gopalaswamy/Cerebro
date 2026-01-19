/**
 * SVG Orb component (Gold, Blue, Red)
 */
import React from 'react';

export type OrbType = 'gold' | 'blue' | 'red';

interface OrbProps {
  type: OrbType;
  size?: number;
  className?: string;
  animated?: boolean;
}

const Orb: React.FC<OrbProps> = ({ type, size = 40, className = '', animated = true }) => {
  const colors = {
    gold: {
      gradient: ['#FFD700', '#FFA500'],
      glow: 'rgba(255, 215, 0, 0.6)',
    },
    blue: {
      gradient: ['#4169E1', '#6495ED'],
      glow: 'rgba(65, 105, 225, 0.6)',
    },
    red: {
      gradient: ['#DC143C', '#FF6347'],
      glow: 'rgba(220, 20, 60, 0.6)',
    },
  };

  const color = colors[type];
  const animationClasses = animated ? 'orb-float orb-glow' : '';
  const orbClass = `orb-${type}`;

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 40 40"
      className={`${orbClass} ${animationClasses} ${className}`}
      style={{
        filter: `drop-shadow(0 0 ${size / 4}px ${color.glow})`,
      }}
    >
      <defs>
        <radialGradient id={`gradient-${type}`} cx="30%" cy="30%">
          <stop offset="0%" stopColor={color.gradient[0]} stopOpacity="1" />
          <stop offset="100%" stopColor={color.gradient[1]} stopOpacity="0.8" />
        </radialGradient>
      </defs>
      <circle
        cx="20"
        cy="20"
        r="18"
        fill={`url(#gradient-${type})`}
        opacity="0.9"
      />
      {/* Highlight for 3D effect */}
      <ellipse
        cx="14"
        cy="14"
        rx="6"
        ry="8"
        fill="rgba(255, 255, 255, 0.3)"
        opacity="0.6"
      />
    </svg>
  );
};

export default Orb;
