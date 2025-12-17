"use client";

import { useState } from "react";
import Link from "next/link";
import { Eye, EyeOff } from "lucide-react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className="relative flex min-h-screen w-full flex-col bg-neutral-50 overflow-x-hidden">
      {/* Header */}
      <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#ededed] px-10 py-3">
        <Link href="/" className="flex items-center gap-4 text-[#141414]">
          <div className="size-4">
            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <g clipPath="url(#clip0_6_543)">
                <path
                  d="M42.1739 20.1739L27.8261 5.82609C29.1366 7.13663 28.3989 10.1876 26.2002 13.7654C24.8538 15.9564 22.9595 18.3449 20.6522 20.6522C18.3449 22.9595 15.9564 24.8538 13.7654 26.2002C10.1876 28.3989 7.13663 29.1366 5.82609 27.8261L20.1739 42.1739C21.4845 43.4845 24.5355 42.7467 28.1133 40.548C30.3042 39.2016 32.6927 37.3073 35 35C37.3073 32.6927 39.2016 30.3042 40.548 28.1133C42.7467 24.5355 43.4845 21.4845 42.1739 20.1739Z"
                  fill="currentColor"
                />
                <path
                  fillRule="evenodd"
                  clipRule="evenodd"
                  d="M7.24189 26.4066C7.31369 26.4411 7.64204 26.5637 8.52504 26.3738C9.59462 26.1438 11.0343 25.5311 12.7183 24.4963C14.7583 23.2426 17.0256 21.4503 19.238 19.238C21.4503 17.0256 23.2426 14.7583 24.4963 12.7183C25.5311 11.0343 26.1438 9.59463 26.3738 8.52504C26.5637 7.64204 26.4411 7.31369 26.4066 7.24189C26.345 7.21246 26.143 7.14535 25.6664 7.1918C24.9745 7.25925 23.9954 7.5498 22.7699 8.14278C20.3369 9.32007 17.3369 11.4915 14.4142 14.4142C11.4915 17.3369 9.32007 20.3369 8.14278 22.7699C7.5498 23.9954 7.25925 24.9745 7.1918 25.6664C7.14534 26.143 7.21246 26.345 7.24189 26.4066ZM29.9001 10.7285C29.4519 12.0322 28.7617 13.4172 27.9042 14.8126C26.465 17.1544 24.4686 19.6641 22.0664 22.0664C19.6641 24.4686 17.1544 26.465 14.8126 27.9042C13.4172 28.7617 12.0322 29.4519 10.7285 29.9001L21.5754 40.747C21.6001 40.7606 21.8995 40.931 22.8729 40.7217C23.9424 40.4916 25.3821 39.879 27.0661 38.8441C29.1062 37.5904 31.3734 35.7982 33.5858 33.5858C35.7982 31.3734 37.5904 29.1062 38.8441 27.0661C39.879 25.3821 40.4916 23.9425 40.7216 22.8729C40.931 21.8995 40.7606 21.6001 40.747 21.5754L29.9001 10.7285ZM29.2403 4.41187L43.5881 18.7597C44.9757 20.1473 44.9743 22.1235 44.6322 23.7139C44.2714 25.3919 43.4158 27.2666 42.252 29.1604C40.8128 31.5022 38.8165 34.012 36.4142 36.4142C34.012 38.8165 31.5022 40.8128 29.1604 42.252C27.2666 43.4158 25.3919 44.2714 23.7139 44.6322C22.1235 44.9743 20.1473 44.9757 18.7597 43.5881L4.41187 29.2403C3.29027 28.1187 3.08209 26.5973 3.21067 25.2783C3.34099 23.9415 3.8369 22.4852 4.54214 21.0277C5.96129 18.0948 8.43335 14.7382 11.5858 11.5858C14.7382 8.43335 18.0948 5.9613 21.0277 4.54214C22.4852 3.8369 23.9415 3.34099 25.2783 3.21067C26.5973 3.08209 28.1187 3.29028 29.2403 4.41187Z"
                  fill="currentColor"
                />
              </g>
              <defs>
                <clipPath id="clip0_6_543">
                  <rect width="48" height="48" fill="white" />
                </clipPath>
              </defs>
            </svg>
          </div>
          <h2 className="text-[#141414] text-lg font-bold leading-tight tracking-[-0.015em]">
            EduAssist
          </h2>
        </Link>
      </header>

      {/* Main Content */}
      <div className="flex flex-1 justify-center px-6 py-5 gap-12">
        {/* Left Side - Form */}
        <div className="flex flex-col w-full max-w-[480px] justify-center">
          <div className="mb-12">
            <h1 className="text-[#141414] text-[32px] font-bold leading-tight mb-2">
              Sign in to your account
            </h1>
            <p className="text-neutral-500 text-base">
              Welcome back! Please login to your account
            </p>
          </div>

          {/* Email Field */}
          <div className="mb-6">
            <label className="text-[#141414] text-base font-medium leading-normal pb-2 block">
              Email
            </label>
            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 rounded-lg text-[#141414] focus:outline-0 focus:ring-0 border border-[#dbdbdb] bg-neutral-50 focus:border-[#dbdbdb] placeholder:text-neutral-500 text-base font-normal leading-normal"
            />
          </div>

          {/* Password Field */}
          <div className="mb-6">
            <label className="text-[#141414] text-base font-medium leading-normal pb-2 block">
              Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 rounded-lg text-[#141414] focus:outline-0 focus:ring-0 border border-[#dbdbdb] bg-neutral-50 focus:border-[#dbdbdb] placeholder:text-neutral-500 text-base font-normal leading-normal pr-10"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-500"
              >
                {showPassword ? (
                  <EyeOff className="w-5 h-5" />
                ) : (
                  <Eye className="w-5 h-5" />
                )}
              </button>
            </div>
          </div>

          {/* Remember & Forgot Password */}
          <div className="flex items-center justify-between mb-8">
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                className="w-4 h-4 rounded border-[#dbdbdb] bg-neutral-50 text-[#141414]"
              />
              <span className="text-neutral-500 text-sm">Remember me</span>
            </label>
            <Link
              href="/forgot-password"
              className="text-neutral-500 text-sm underline hover:text-[#141414] transition-colors"
            >
              Forgot Password?
            </Link>
          </div>

          {/* Login Button */}
          <button className="w-full px-4 py-3 rounded-lg bg-[#141414] text-neutral-50 text-sm font-bold leading-normal tracking-[0.015em] mb-3 hover:bg-[#141414]/90 transition-colors">
            Login
          </button>

          {/* Sign Up Button */}
          <Link
            href="/signup"
            className="w-full px-4 py-3 rounded-lg bg-[#ededed] text-[#141414] text-sm font-bold leading-normal tracking-[0.015em] mb-4 hover:bg-[#ededed]/80 transition-colors flex items-center justify-center"
          >
            Take me to Sign up
          </Link>

          {/* Divider */}
          <div className="flex items-center gap-4 mb-4">
            <div className="flex-1 h-px bg-[#dbdbdb]"></div>
            <span className="text-neutral-500 text-sm">OR</span>
            <div className="flex-1 h-px bg-[#dbdbdb]"></div>
          </div>

          {/* Social Login */}
          <button className="w-full px-4 py-3 rounded-lg border border-[#dbdbdb] bg-white text-[#141414] text-sm font-medium leading-normal mb-3 hover:bg-neutral-50 transition-colors flex items-center justify-center gap-2">
            <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
            </svg>
            Sign in with Google
          </button>
        </div>

        {/* Right Side - Illustration */}
        <div className="hidden lg:flex flex-col w-[400px] justify-center">
          <div className="rounded-lg overflow-hidden shadow-lg">
            <div
              className="w-full aspect-square bg-center bg-cover bg-no-repeat rounded-lg"
              style={{
                backgroundImage:
                  'url("https://lh3.googleusercontent.com/aida-public/AB6AXuDgZIz-eeU-p0EAjdIeuHeGh59wkAucQQdvUlc-mOoaeUiGJJFDNEnr4EZdoXztxVjIBlTxDKpVk0-ONTGHE2Hk9pcb4ig1XOTEE4KE8j0ExNiOgNzLjQSjGddz6-BSrXuyf0OG2WkoGSlcZzcM6xoAQe-Iv2wPHcNLmi6oGWpIw7QTPFFR7oFtuelrlvr7gd3B_AxmUkh9MQxMXzTeXAEuyic8vEbbdbeHLpD6NHWqO6bTEsE271xa23iHrh_pJsGal8tdpWbkYfY")',
              }}
            />
          </div>
          <p className="text-neutral-500 text-sm text-center mt-6">
            Sign in to unlock powerful teaching tools and transform your classroom experience
          </p>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-[#ededed] px-10 py-6 text-center text-neutral-500 text-sm">
        <p>© 2025 EduAssist. All rights reserved.</p>
      </footer>
    </div>
  );
}
