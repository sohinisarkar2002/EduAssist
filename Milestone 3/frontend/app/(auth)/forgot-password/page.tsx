"use client";

import { useState } from "react";
import Link from "next/link";
import { Eye, EyeOff, CheckCircle, ArrowRight } from "lucide-react";

type Step = "email" | "verification" | "reset" | "success";

export default function ForgotPassword() {
  const [step, setStep] = useState<Step>("email");
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handleEmailSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      setStep("verification");
    }
  };

  const handleVerificationSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (code) {
      setStep("reset");
    }
  };

  const handleResetSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (password && confirmPassword && password === confirmPassword) {
      setStep("success");
    }
  };

  return (
    <div className="relative flex min-h-screen w-full flex-col bg-slate-50 overflow-x-hidden">
      {/* Header */}
      <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#e7edf3] px-10 py-3">
        <Link href="/" className="flex items-center gap-4 text-[#0d141b]">
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
          <h2 className="text-[#0d141b] text-lg font-bold leading-tight tracking-[-0.015em]">
            EduAssist
          </h2>
        </Link>
      </header>

      {/* Main Content */}
      <div className="flex flex-1 justify-center px-6 py-5 gap-12">
        {/* Left Side - Form */}
        <div className="flex flex-col w-full max-w-[480px] justify-center">
          {/* Step 1: Email Verification */}
          {step === "email" && (
            <>
              <div className="mb-8">
                <h1 className="text-[#0d141b] text-[28px] font-bold leading-tight mb-2">
                  Reset your password
                </h1>
                <p className="text-[#4c739a] text-sm">
                  Enter your email address and we'll send you a verification code
                </p>
              </div>

              <form onSubmit={handleEmailSubmit} className="space-y-6">
                <div>
                  <label className="text-[#0d141b] text-base font-medium leading-normal pb-2 block">
                    Email Address
                  </label>
                  <input
                    type="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="w-full px-4 py-3 rounded-lg text-[#0d141b] focus:outline-0 focus:ring-0 border border-[#cfdbe7] bg-slate-50 focus:border-[#cfdbe7] placeholder:text-[#4c739a] text-base font-normal leading-normal"
                  />
                </div>

                <button
                  type="submit"
                  className="w-full px-4 py-3 rounded-lg bg-[#1380ec] text-slate-50 text-sm font-bold leading-normal tracking-[0.015em] hover:bg-[#1380ec]/90 transition-colors flex items-center justify-center gap-2"
                >
                  Send Verification Code
                  <ArrowRight className="w-4 h-4" />
                </button>
              </form>

              <div className="flex gap-2 mt-6">
                <p className="text-[#4c739a] text-sm">
                  Remember your password?{" "}
                  <Link href="/login" className="text-[#0d141b] underline hover:text-[#4c739a]">
                    Back to login
                  </Link>
                </p>
              </div>
            </>
          )}

          {/* Step 2: Verification Code */}
          {step === "verification" && (
            <>
              <div className="mb-8">
                <h1 className="text-[#0d141b] text-[28px] font-bold leading-tight mb-2">
                  Check your email
                </h1>
                <p className="text-[#4c739a] text-sm">
                  We've sent a verification code to {email}
                </p>
              </div>

              <form onSubmit={handleVerificationSubmit} className="space-y-6">
                <div>
                  <label className="text-[#0d141b] text-base font-medium leading-normal pb-2 block">
                    Verification Code
                  </label>
                  <input
                    type="text"
                    placeholder="Enter 6-digit code"
                    value={code}
                    onChange={(e) => setCode(e.target.value.replace(/\D/g, "").slice(0, 6))}
                    required
                    maxLength={6}
                    className="w-full px-4 py-3 rounded-lg text-[#0d141b] focus:outline-0 focus:ring-0 border border-[#cfdbe7] bg-slate-50 focus:border-[#cfdbe7] placeholder:text-[#4c739a] text-base font-normal leading-normal text-center tracking-widest"
                  />
                  <p className="text-[#4c739a] text-xs mt-2">
                    Didn't receive the code?{" "}
                    <button
                      type="button"
                      onClick={() => setStep("email")}
                      className="text-[#0d141b] underline hover:text-[#4c739a]"
                    >
                      Resend
                    </button>
                  </p>
                </div>

                <button
                  type="submit"
                  className="w-full px-4 py-3 rounded-lg bg-[#1380ec] text-slate-50 text-sm font-bold leading-normal tracking-[0.015em] hover:bg-[#1380ec]/90 transition-colors flex items-center justify-center gap-2"
                >
                  Verify Code
                  <ArrowRight className="w-4 h-4" />
                </button>
              </form>
            </>
          )}

          {/* Step 3: Reset Password */}
          {step === "reset" && (
            <>
              <div className="mb-8">
                <h1 className="text-[#0d141b] text-[28px] font-bold leading-tight mb-2">
                  Create new password
                </h1>
                <p className="text-[#4c739a] text-sm">
                  Enter a strong password to secure your account
                </p>
              </div>

              <form onSubmit={handleResetSubmit} className="space-y-6">
                <div>
                  <label className="text-[#0d141b] text-base font-medium leading-normal pb-2 block">
                    New Password
                  </label>
                  <div className="relative">
                    <input
                      type={showPassword ? "text" : "password"}
                      placeholder="Enter new password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                      className="w-full px-4 py-3 rounded-lg text-[#0d141b] focus:outline-0 focus:ring-0 border border-[#cfdbe7] bg-slate-50 focus:border-[#cfdbe7] placeholder:text-[#4c739a] text-base font-normal leading-normal pr-10"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-[#4c739a]"
                    >
                      {showPassword ? (
                        <EyeOff className="w-5 h-5" />
                      ) : (
                        <Eye className="w-5 h-5" />
                      )}
                    </button>
                  </div>
                  <p className="text-[#4c739a] text-xs mt-2">
                    Use at least 8 characters, including uppercase, lowercase, and numbers
                  </p>
                </div>

                <div>
                  <label className="text-[#0d141b] text-base font-medium leading-normal pb-2 block">
                    Confirm Password
                  </label>
                  <div className="relative">
                    <input
                      type={showConfirmPassword ? "text" : "password"}
                      placeholder="Confirm new password"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      required
                      className="w-full px-4 py-3 rounded-lg text-[#0d141b] focus:outline-0 focus:ring-0 border border-[#cfdbe7] bg-slate-50 focus:border-[#cfdbe7] placeholder:text-[#4c739a] text-base font-normal leading-normal pr-10"
                    />
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-[#4c739a]"
                    >
                      {showConfirmPassword ? (
                        <EyeOff className="w-5 h-5" />
                      ) : (
                        <Eye className="w-5 h-5" />
                      )}
                    </button>
                  </div>
                  {password && confirmPassword && password !== confirmPassword && (
                    <p className="text-red-500 text-xs mt-2">Passwords do not match</p>
                  )}
                </div>

                <button
                  type="submit"
                  disabled={password !== confirmPassword}
                  className="w-full px-4 py-3 rounded-lg bg-[#1380ec] text-slate-50 text-sm font-bold leading-normal tracking-[0.015em] hover:bg-[#1380ec]/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  Reset Password
                  <ArrowRight className="w-4 h-4" />
                </button>
              </form>
            </>
          )}

          {/* Step 4: Success */}
          {step === "success" && (
            <>
              <div className="flex flex-col items-center justify-center text-center mb-8">
                <div className="mb-4">
                  <CheckCircle className="w-16 h-16 text-green-500 mx-auto" />
                </div>
                <h1 className="text-[#0d141b] text-[28px] font-bold leading-tight mb-2">
                  Password reset successful
                </h1>
                <p className="text-[#4c739a] text-sm">
                  Your password has been changed successfully. You can now log in with your new password.
                </p>
              </div>

              <Link
                href="/login"
                className="w-full px-4 py-3 rounded-lg bg-[#1380ec] text-slate-50 text-sm font-bold leading-normal tracking-[0.015em] hover:bg-[#1380ec]/90 transition-colors flex items-center justify-center gap-2"
              >
                Back to Login
                <ArrowRight className="w-4 h-4" />
              </Link>
            </>
          )}
        </div>

        {/* Right Side - Illustration */}
        <div className="hidden lg:flex flex-col w-[400px] justify-center">
          <div className="rounded-lg overflow-hidden shadow-lg bg-slate-50 p-4">
            <div
              className="w-full aspect-square bg-center bg-cover bg-no-repeat rounded-lg"
              style={{
                backgroundImage:
                  'url("https://lh3.googleusercontent.com/aida-public/AB6AXuDgZIz-eeU-p0EAjdIeuHeGh59wkAucQQdvUlc-mOoaeUiGJJFDNEnr4EZdoXztxVjIBlTxDKpVk0-ONTGHE2Hk9pcb4ig1XOTEE4KE8j0ExNiOgNzLjQSjGddz6-BSrXuyf0OG2WkoGSlcZzcM6xoAQe-Iv2wPHcNLmi6oGWpIw7QTPFFR7oFtuelrlvr7gd3B_AxmUkh9MQxMXzTeXAEuyic8vEbbdbeHLpD6NHWqO6bTEsE271xa23iHrh_pJsGal8tdpWbkYfY")',
              }}
            />
          </div>
          <p className="text-[#4c739a] text-sm text-center mt-6">
            {step === "email" &&
              "We'll help you recover your account with a simple verification process"}
            {step === "verification" &&
              "Check your email for the verification code"}
            {step === "reset" &&
              "Create a strong password to protect your account"}
            {step === "success" &&
              "You're all set! Log in with your new password"}
          </p>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-[#e7edf3] px-10 py-6 text-center text-[#4c739a] text-sm">
        <p>© 2025 EduAssist. All rights reserved.</p>
      </footer>
    </div>
  );
}
