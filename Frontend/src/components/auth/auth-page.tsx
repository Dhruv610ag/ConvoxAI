/**
 * Authentication Page
 * 
 * Main authentication page that toggles between login and signup forms.
 */

import React, { useState } from 'react';
import { LoginForm } from './login-form';
import { SignUpForm } from './signup-form';
import { Card, CardContent } from '@/components/ui/card';
import { AnimatedThemeToggler } from '@/components/ui/animated-theme-toggler';

export function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 p-4">
      {/* Theme Toggler */}
      <div className="absolute top-4 right-4">
        <AnimatedThemeToggler />
      </div>

      <div className="w-full max-w-md">

        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-br from-blue-600 to-purple-600 mb-4">
            <svg
              className="w-8 h-8 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
              />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">ConvoxAI</h2>
          <p className="text-gray-600 dark:text-gray-400">AI-Powered Call Summarization</p>
        </div>

        <Card className="backdrop-blur-sm bg-white/90 dark:bg-gray-800/90 shadow-xl">
          <CardContent className="pt-6">
            {isLogin ? (
              <LoginForm onToggleForm={() => setIsLogin(false)} />
            ) : (
              <SignUpForm onToggleForm={() => setIsLogin(true)} />
            )}
          </CardContent>
        </Card>

        <p className="text-center text-sm text-gray-600 dark:text-gray-400 mt-6">
          By continuing, you agree to our Terms of Service and Privacy Policy
        </p>
      </div>
    </div>
  );
}
