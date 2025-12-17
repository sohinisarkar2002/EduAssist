"use client";

import { useState } from "react";
import Link from "next/link";
import { Eye, EyeOff } from "lucide-react";

export default function Signup() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    courseCode: "",
    role: "",
  });

  const [showPassword, setShowPassword] = useState(false);
  const [agreedToTerms, setAgreedToTerms] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
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
          <div className="mb-8">
            <h1 className="text-[#0d141b] text-[28px] font-bold leading-tight text-center mb-2">
              Create your account
            </h1>
          </div>

          {/* Name Field */}
          <div className="mb-6">
            <label className="text-[#0d141b] text-base font-medium leading-normal pb-2 block">
              Name
            </label>
            <input
              type="text"
              name="name"
              placeholder="Enter your name"
              value={formData.name}
              onChange={handleChange}
              className="w-full px-4 py-3 rounded-lg text-[#0d141b] focus:outline-0 focus:ring-0 border border-[#cfdbe7] bg-slate-50 focus:border-[#cfdbe7] placeholder:text-[#4c739a] text-base font-normal leading-normal"
            />
          </div>

          {/* Email Field */}
          <div className="mb-6">
            <label className="text-[#0d141b] text-base font-medium leading-normal pb-2 block">
              Email
            </label>
            <input
              type="email"
              name="email"
              placeholder="Enter your email"
              value={formData.email}
              onChange={handleChange}
              className="w-full px-4 py-3 rounded-lg text-[#0d141b] focus:outline-0 focus:ring-0 border border-[#cfdbe7] bg-slate-50 focus:border-[#cfdbe7] placeholder:text-[#4c739a] text-base font-normal leading-normal"
            />
          </div>

          {/* Password Field */}
          <div className="mb-6">
            <label className="text-[#0d141b] text-base font-medium leading-normal pb-2 block">
              Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                placeholder="Enter your password"
                value={formData.password}
                onChange={handleChange}
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
          </div>

          {/* Course Code Field */}
          <div className="mb-6">
            <label className="text-[#0d141b] text-base font-medium leading-normal pb-2 block">
              Course Code
            </label>
            <input
              type="text"
              name="courseCode"
              placeholder="Enter course code"
              value={formData.courseCode}
              onChange={handleChange}
              className="w-full px-4 py-3 rounded-lg text-[#0d141b] focus:outline-0 focus:ring-0 border border-[#cfdbe7] bg-slate-50 focus:border-[#cfdbe7] placeholder:text-[#4c739a] text-base font-normal leading-normal"
            />
          </div>

          {/* TA Role Verification */}
          <div className="mb-6">
            <label className="text-[#0d141b] text-base font-medium leading-normal pb-2 block">
              TA Role Verification
            </label>
            <select
              name="role"
              value={formData.role}
              onChange={handleChange}
              className="w-full px-4 py-3 rounded-lg text-[#0d141b] focus:outline-0 focus:ring-0 border border-[#cfdbe7] bg-slate-50 focus:border-[#cfdbe7] placeholder:text-[#4c739a] text-base font-normal leading-normal appearance-none bg-no-repeat"
              style={{
                backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='24px' height='24px' fill='rgb(76,115,154)' viewBox='0 0 256 256'%3e%3cpath d='M181.66,170.34a8,8,0,0,1,0,11.32l-48,48a8,8,0,0,1-11.32,0l-48-48a8,8,0,0,1,11.32-11.32L128,212.69l42.34-42.35A8,8,0,0,1,181.66,170.34Zm-96-84.68L128,43.31l42.34,42.35a8,8,0,0,0,11.32-11.32l-48-48a8,8,0,0,0-11.32,0l-48,48A8,8,0,0,0,85.66,85.66Z'%3e%3c/path%3e%3c/svg%3e")`,
                backgroundPosition: "calc(100% - 12px) center",
                backgroundRepeat: "no-repeat",
                paddingRight: "40px",
              }}
            >
              <option value="">Select role</option>
              <option value="ta">Teaching Assistant</option>
              <option value="professor">Professor</option>
              <option value="instructor">Instructor</option>
            </select>
          </div>

          {/* Terms & Conditions */}
          <div className="mb-6 flex items-start gap-2">
            <input
              type="checkbox"
              id="terms"
              checked={agreedToTerms}
              onChange={(e) => setAgreedToTerms(e.target.checked)}
              className="mt-1 w-4 h-4 rounded border-[#cfdbe7] bg-slate-50 text-[#0d141b]"
            />
            <label htmlFor="terms" className="text-[#4c739a] text-sm">
              I agree to the{" "}
              <span className="text-[#0d141b] font-medium">Terms & Conditions</span> and{" "}
              <span className="text-[#0d141b] font-medium">Privacy Policy</span>
            </label>
          </div>

          {/* Create Account Button */}
          <button className="w-full px-4 py-3 rounded-lg bg-[#1380ec] text-slate-50 text-sm font-bold leading-normal tracking-[0.015em] mb-4 hover:bg-[#1380ec]/90 transition-colors">
            Create Account
          </button>

          {/* Login Link */}
          <p className="text-[#4c739a] text-sm font-normal leading-normal text-center">
            Already have an account?{" "}
            <Link href="/login" className="text-[#4c739a] underline hover:text-[#0d141b]">
              Login
            </Link>
          </p>
        </div>

        {/* Right Side - Illustration */}
        <div className="hidden lg:flex flex-col w-[400px] justify-center">
          <div className="rounded-lg overflow-hidden shadow-lg bg-slate-50 p-4">
            <div
              className="w-full aspect-square bg-center bg-cover bg-no-repeat rounded-lg"
              style={{
                backgroundImage:
                  'url("https://lh3.googleusercontent.com/aida-public/AB6AXuCEhohKfPYvJDqcRslXk9jJaRCxeJqW5_AFJ5HpsUH-yEscQF4PBz0tuaxybGcyKV805h5tzhd1M57l2tK0-B2NeraePN8is1yjG095Vh1X0ouMph6Y4MnYfin2rxM4alSHYCi5VKJeU002zKrJEzbSzcP7IjjEgGEY-CkRXb3S8fKaiIM1oZFC35jm6bfvpU5lDXbCgLkEf5acb1B1ftjeTNOo6vewgpNCJb3Nh_nmHu3-7kpDAYMbt_m3nNQgYZ2hiob3uE-TeMU")',
              }}
            />
          </div>
          <p className="text-[#4c739a] text-sm text-center mt-6">
            Join thousands of educators and TAs using EduAssist to enhance their teaching
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
