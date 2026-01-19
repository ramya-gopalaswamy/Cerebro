/**
 * Orb Jar component - Visual container for orbs
 */
'use client';

import React, { useMemo } from 'react';
import Jar from '@/assets/svg/Jar';
import Orb, { OrbType } from '@/assets/svg/Orb';
import { OrbInventory } from '@/services/api';

interface OrbJarProps {
  inventory: OrbInventory;
  className?: string;
}

const OrbJar: React.FC<OrbJarProps> = ({ inventory, className = '' }) => {
  // Generate orb elements based on inventory
  const orbs = useMemo(() => {
    const orbElements: { type: OrbType; id: string }[] = [];
    
    // Add gold orbs
    for (let i = 0; i < inventory.gold; i++) {
      orbElements.push({ type: 'gold', id: `gold-${i}` });
    }
    
    // Add blue orbs
    for (let i = 0; i < inventory.blue; i++) {
      orbElements.push({ type: 'blue', id: `blue-${i}` });
    }
    
    // Add red orbs
    for (let i = 0; i < inventory.red; i++) {
      orbElements.push({ type: 'red', id: `red-${i}` });
    }
    
    return orbElements;
  }, [inventory]);

  // Calculate positions for orbs (stack them)
  const getOrbPosition = (index: number, total: number) => {
    const baseY = 220; // Base Y position (bottom of jar)
    const orbSize = 40;
    const spacing = 5;
    const y = baseY - (index * (orbSize + spacing));
    const x = 100; // Center X
    const offsetX = (index % 2 === 0 ? -1 : 1) * (index % 3) * 3; // Slight horizontal offset
    
    return {
      x: x + offsetX,
      y: Math.max(60, y), // Don't go above jar opening
    };
  };

  const totalOrbs = inventory.gold + inventory.blue + inventory.red;

  return (
    <div className={`flex flex-col items-center ${className}`}>
      <Jar width={200} height={300} className="relative">
        {orbs.map((orb, index) => {
          const position = getOrbPosition(index, totalOrbs);
          return (
            <div
              key={orb.id}
              className="absolute orb-enter"
              style={{
                left: `${position.x}px`,
                bottom: `${300 - position.y}px`,
                transform: 'translateX(-50%)',
                zIndex: index,
              }}
            >
              <Orb type={orb.type} size={40} animated={true} />
            </div>
          );
        })}
      </Jar>
      
      {/* Inventory counts */}
      <div className="mt-4 text-center">
        <div className="flex gap-4 justify-center text-sm">
          <div className="flex items-center gap-1">
            <Orb type="gold" size={20} animated={false} />
            <span className="font-semibold">{inventory.gold}</span>
          </div>
          <div className="flex items-center gap-1">
            <Orb type="blue" size={20} animated={false} />
            <span className="font-semibold">{inventory.blue}</span>
          </div>
          <div className="flex items-center gap-1">
            <Orb type="red" size={20} animated={false} />
            <span className="font-semibold">{inventory.red}</span>
          </div>
        </div>
        <div className="mt-2 text-xs text-gray-500">
          Total: {totalOrbs} orbs
        </div>
      </div>
    </div>
  );
};

export default OrbJar;
