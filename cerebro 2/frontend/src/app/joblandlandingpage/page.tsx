"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

const roles = [
  'Software Engineer',
  'Product Manager',
  'Data Scientist',
  'Designer',
  'Marketing',
  'Sales',
  'Other',
];

export default function JobLandLandingPage() {
  const [selectedRole, setSelectedRole] = useState('');
  const router = useRouter();

  return (
    <div
      className="min-h-screen w-full flex flex-col items-center justify-center relative"
      style={{
        backgroundImage: "url('/assets/images/jobland.png')",
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
      }}
    >
      <h1
        className="text-8xl font-extrabold text-white mb-2 mt-2 text-center drop-shadow-[0_0_40px_rgba(255,255,255,0.9)]"
        style={{
          textShadow: '0 0 40px #fff, 0 0 80px #fff',
          letterSpacing: '0.08em',
          position: 'relative',
          top: '-2.5rem',
        }}
      >
        JOBLAND
      </h1>
      <div className="flex flex-col items-center justify-center mt-4">
        <h2 className="text-3xl md:text-4xl font-bold text-white mb-8 text-center drop-shadow-lg">
          What job role are you looking for?
        </h2>
        <div className="w-full max-w-xl">
          <select
            value={selectedRole}
            onChange={e => setSelectedRole(e.target.value)}
            className="w-full bg-black bg-opacity-80 text-white text-xl rounded-2xl px-6 py-5 mb-6 border-2 border-pink-400 focus:outline-none focus:ring-2 focus:ring-pink-400 shadow-lg"
          >
            <option value="">Select a role...</option>
            {roles.map(role => (
              <option key={role} value={role}>{role}</option>
            ))}
          </select>
        </div>
        <button
          className="mt-2 mb-8 px-8 py-4 rounded-full bg-pink-500 text-white text-2xl font-extrabold shadow-lg hover:bg-pink-600 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
          disabled={!selectedRole}
          onClick={() => {
            if (selectedRole === 'Software Engineer') {
              router.push('/joblandlandingpage/jobonboarding');
            } else {
              router.push('/'); // or keep existing behavior for other roles
            }
          }}
        >
          ENTER JOBLAND
        </button>
      </div>
    </div>
  );
}
