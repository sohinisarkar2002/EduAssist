"use client";

import Link from "next/link";
import {
  GraduationCap,
  BookOpen,
  Users,
  FileText,
  Presentation,
  ArrowRight,
  Sparkles
} from "lucide-react";

export default function Landing() {
  const features = [
    {
      title: "Knowledge Assistant",
      description: "AI-powered answers to student questions with detailed explanations",
      icon: GraduationCap,
      path: "/features/knowledge-assistant"
    },
    {
      title: "Study Guide Generator",
      description: "Automatically generate comprehensive study guides from lecture content",
      icon: BookOpen,
      path: "/features/study-guide-generator"
    },
    {
      title: "Admin Workflow Agent",
      description: "Streamline administrative tasks with AI assistance",
      icon: Users,
      path: "/features/admin-workflow"
    },
    {
      title: "Assessment Generator",
      description: "Create customized assessments with AI-generated questions",
      icon: FileText,
      path: "/features/assessment-generator"
    },
    {
      title: "Slide Deck Creator",
      description: "Generate professional slide decks from lecture notes",
      icon: Presentation,
      path: "/features/slide-deck-generator"
    },
  ];

  return (
    <div className="min-h-screen bg-slate-50">
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
        <div className="flex items-center gap-6">
          <Link href="/dashboard" className="text-[#0d141b] text-sm font-medium leading-normal">
            Dashboard
          </Link>
          <Link
            href="/login"
            className="flex items-center gap-2 px-4 py-2 bg-[#0d141b] text-white rounded-lg text-sm font-medium hover:bg-[#0d141b]/90 transition-colors"
          >
            Get Started
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="px-6 py-20">
        <div className="max-w-3xl mx-auto text-center mb-16">
          <div className="flex justify-center mb-6">
            <div className="flex items-center gap-2 px-4 py-2 bg-blue-50 rounded-full">
              <Sparkles className="w-4 h-4 text-blue-600" />
              <span className="text-sm text-blue-600 font-medium">AI-Powered Teaching Assistant</span>
            </div>
          </div>
          <h1 className="text-[48px] font-bold text-[#0d141b] leading-tight tracking-[-0.015em] mb-4">
            Transform Your Teaching with AI
          </h1>
          <p className="text-[#4c739a] text-lg leading-relaxed mb-8">
            EduAssist helps educators create better content, engage students more effectively, and save time on administrative tasks using advanced AI technology.
          </p>
          <Link
            href="/login"
            className="inline-flex items-center gap-2 px-6 py-3 bg-[#0d141b] text-white rounded-lg text-base font-bold hover:bg-[#0d141b]/90 transition-colors"
          >
            Start Free Today
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-6 py-20 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-[36px] font-bold text-[#0d141b] leading-tight mb-4">
              Powerful Features
            </h2>
            <p className="text-[#4c739a] text-lg">
              Everything you need to enhance your teaching experience
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature) => {
              const Icon = feature.icon;
              return (
                <Link
                  key={feature.path}
                  href={feature.path}
                  className="group p-6 border border-[#e7edf3] rounded-lg hover:border-[#0d141b] hover:shadow-lg transition-all"
                >
                  <div className="flex items-start gap-4">
                    <div className="p-3 bg-[#e7edf3] rounded-lg group-hover:bg-[#0d141b] transition-colors">
                      <Icon className="w-6 h-6 text-[#0d141b] group-hover:text-white transition-colors" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-[#0d141b] font-bold text-base leading-tight mb-2">
                        {feature.title}
                      </h3>
                      <p className="text-[#4c739a] text-sm leading-relaxed">
                        {feature.description}
                      </p>
                    </div>
                  </div>
                </Link>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-6 py-20">
        <div className="max-w-3xl mx-auto bg-[#0d141b] rounded-lg p-12 text-center">
          <h2 className="text-[32px] font-bold text-white leading-tight mb-4">
            Ready to Transform Your Teaching?
          </h2>
          <p className="text-gray-300 text-base mb-8">
            Join educators worldwide using EduAssist to enhance their teaching and improve student outcomes.
          </p>
          <Link
            href="/login"
            className="inline-flex items-center gap-2 px-6 py-3 bg-white text-[#0d141b] rounded-lg font-bold hover:bg-gray-100 transition-colors"
          >
            Get Started Now
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-[#e7edf3] px-6 py-8">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <p className="text-[#4c739a] text-sm">© 2025 EduAssist. All rights reserved.</p>
          <div className="flex items-center gap-6 text-[#4c739a] text-sm">
            <Link href="#" className="hover:text-[#0d141b] transition-colors">
              Privacy
            </Link>
            <Link href="#" className="hover:text-[#0d141b] transition-colors">
              Terms
            </Link>
            <Link href="#" className="hover:text-[#0d141b] transition-colors">
              Contact
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
