"use client";

import React, { useState } from 'react';
import { api } from '../../services/api';
import { useRouter } from 'next/navigation';

function getPasswordStrength(password: string) {
  if (!password) return '';
  let score = 0;
  if (password.length >= 8) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[a-z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[^A-Za-z0-9]/.test(password)) score++;
  if (score >= 4) return 'Strong';
  if (score >= 2) return 'Medium';
  return 'Weak';
}

export default function HeadquartersInit() {
  const [email, setEmail] = useState('');
  const [pass, setPass] = useState('');
  const [repeatPass, setRepeatPass] = useState('');
  const [message, setMessage] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState('');
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (email && pass) {
      setMessage('Logging in...');
      try {
        const res = await api.login(email, pass);
        setMessage(res.message || 'Login successful!');
        if (res.access_token) {
          // Fetch profile with JWT
          const profile = await api.getProfile(res.access_token);
          setMessage(`Welcome, ${profile.user}!`);
          // Optionally store token/profile in localStorage or context
        }
        router.push('/onboarding');
      } catch (err: any) {
        setMessage(err.message || 'Login failed.');
      }
    } else {
      setMessage('Missing parameters.');
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !pass || !repeatPass) {
      setMessage('Please fill all fields.');
      return;
    }
    if (pass !== repeatPass) {
      setMessage('Passwords do not match.');
      return;
    }
    if (getPasswordStrength(pass) === 'Weak') {
      setMessage('Password is too weak.');
      return;
    }
    setMessage('Registering...');
    try {
      const res = await api.register(email, pass);
      setMessage(res.message || 'Registration successful!');
      setIsRegistering(false);
      // Redirect to onboarding for new user
      router.push('/onboarding');
    } catch (err: any) {
      setMessage(err.message || 'Registration failed.');
    }
  };

  return (
    <div className="signup-background min-h-screen flex flex-col items-center justify-center transition-colors duration-500 relative">
      <div className="z-10 w-full max-w-lg mx-auto flex flex-col items-center">
        <h1 className="text-4xl font-extrabold mb-6 tracking-widest text-center drop-shadow-lg text-white" style={{textShadow:'0 0 10px #fff'}}>HEADQUARTERS INITIALIZATION</h1>
        <h1 className="text-4xl font-extrabold text-center text-blue-700 mb-6">Welcome to Cerebro!</h1>
        <div className="w-full bg-black/70 rounded-3xl shadow-2xl p-8 border-4 border-white/20 flex flex-col items-center">
          {!isRegistering ? (
            <>
              <form className="w-full flex flex-col gap-6" onSubmit={handleLogin}>
                <label htmlFor="email" className="text-cyan-200 text-lg font-bold tracking-wide mb-1">CORE IDENTITY <span className="text-xs text-cyan-400">(Email)</span></label>
                <input id="email" name="email" type="email" autoComplete="email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="Enter your email" className="w-full px-6 py-4 rounded-full border-2 border-cyan-400 bg-black/60 text-cyan-200 text-lg font-mono focus:outline-none focus:ring-2 focus:ring-cyan-400 shadow-inner" />
                <label htmlFor="password" className="text-pink-200 text-lg font-bold tracking-wide mb-1">SECURITY ACCESS <span className="text-xs text-pink-400">(Password)</span></label>
                <input id="password" name="password" type="password" autoComplete="new-password" value={pass} onChange={e=>setPass(e.target.value)} placeholder="Enter your password" className="w-full px-6 py-4 rounded-full border-2 border-pink-400 bg-black/60 text-pink-200 text-lg font-mono focus:outline-none focus:ring-2 focus:ring-pink-400 shadow-inner" />
                <button type="submit" className="mt-4 py-4 rounded-full w-full text-2xl font-bold tracking-widest bg-gradient-to-r from-cyan-400 via-green-400 to-pink-400 text-white shadow-xl hover:scale-105 transition-all duration-200 border-2 border-white flex items-center justify-center gap-2 relative overflow-hidden cool-activate-btn">
                  <span className="absolute left-0 top-0 w-full h-full animate-pulse bg-gradient-to-r from-cyan-500/20 via-green-500/10 to-pink-500/20 blur-lg opacity-60"></span>
                  <span className="relative z-10">ACTIVATE CONSOLE</span>
                </button>
              </form>
              <button type="button" onClick={() => { setIsRegistering(true); setMessage(''); setPass(''); setRepeatPass(''); }} className="mt-6 py-3 rounded-full w-full text-lg font-bold tracking-wide bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 text-white shadow-md hover:scale-105 transition-all duration-200 border-2 border-white/60 flex items-center justify-center gap-2">
                NEW USER? SIGN UP
              </button>
            </>
          ) : (
            <>
              <form className="w-full flex flex-col gap-6" onSubmit={handleRegister}>
                <label htmlFor="signup-email" className="text-cyan-200 text-lg font-bold tracking-wide mb-1">EMAIL</label>
                <input id="signup-email" name="email" type="email" autoComplete="email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="Enter your email" className="w-full px-6 py-4 rounded-full border-2 border-cyan-400 bg-black/60 text-cyan-200 text-lg font-mono focus:outline-none focus:ring-2 focus:ring-cyan-400 shadow-inner" />
                <label htmlFor="signup-password" className="text-pink-200 text-lg font-bold tracking-wide mb-1">PASSWORD</label>
                <input id="signup-password" name="password" type="password" autoComplete="new-password" value={pass} onChange={e=>{setPass(e.target.value); setPasswordStrength(getPasswordStrength(e.target.value));}} placeholder="Enter your password" className="w-full px-6 py-4 rounded-full border-2 border-pink-400 bg-black/60 text-pink-200 text-lg font-mono focus:outline-none focus:ring-2 focus:ring-pink-400 shadow-inner" />
                <label htmlFor="repeat-password" className="text-pink-200 text-lg font-bold tracking-wide mb-1">REPEAT PASSWORD</label>
                <input id="repeat-password" name="repeatPassword" type="password" autoComplete="new-password" value={repeatPass} onChange={e=>setRepeatPass(e.target.value)} placeholder="Repeat your password" className="w-full px-6 py-4 rounded-full border-2 border-pink-400 bg-black/60 text-pink-200 text-lg font-mono focus:outline-none focus:ring-2 focus:ring-pink-400 shadow-inner" />
                <div className="text-xs text-gray-300 mt-2">
                  Password must be at least 8 characters, contain upper and lower case letters, a number, and a special character.
                </div>
                <div className={`text-sm font-bold mt-1 ${passwordStrength === 'Strong' ? 'text-green-400' : passwordStrength === 'Medium' ? 'text-yellow-400' : 'text-red-400'}`}>
                  Strength: {passwordStrength || 'Enter password'}
                </div>
                <button type="submit" className="mt-4 py-4 rounded-full w-full text-2xl font-bold tracking-widest bg-gradient-to-r from-green-400 via-cyan-400 to-blue-400 text-white shadow-xl hover:scale-105 transition-all duration-200 border-2 border-white flex items-center justify-center gap-2 relative overflow-hidden cool-activate-btn">
                  <span className="absolute left-0 top-0 w-full h-full animate-pulse bg-gradient-to-r from-green-500/20 via-cyan-500/10 to-blue-500/20 blur-lg opacity-60"></span>
                  <span className="relative z-10">SIGN UP</span>
                </button>
              </form>
              <button type="button" onClick={() => { setIsRegistering(false); setMessage(''); setPass(''); setRepeatPass(''); }} className="mt-6 py-3 rounded-full w-full text-lg font-bold tracking-wide bg-gradient-to-r from-gray-400 via-gray-600 to-gray-800 text-white shadow-md hover:scale-105 transition-all duration-200 border-2 border-white/60 flex items-center justify-center gap-2">
                Back to Login
              </button>
            </>
          )}
          {message && <div className="mt-6 text-lg font-semibold text-green-300 animate-pulse">{message}</div>}
        </div>
      </div>
      <style jsx global>{`
        body { background: unset; }
        .cool-activate-btn {
          box-shadow: 0 0 40px 10px #00fff7, 0 0 80px 20px #ff00e0;
          letter-spacing: 0.15em;
        }
        .cool-activate-btn:hover {
          filter: brightness(1.2) saturate(1.3);
          box-shadow: 0 0 80px 20px #00fff7, 0 0 120px 40px #ff00e0;
        }
        .signup-background {
          background-image: url('/background.jpg');
          background-size: cover;
          background-position: center;
        }
      `}</style>
    </div>
  );
}
