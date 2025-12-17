"use client";

import AppLayout from "@/components/AppLayout";
import { useState } from "react";

export default function SlideCreator() {
  const [activeTab, setActiveTab] = useState<"generator" | "feedback">("generator");

  const slides = [
    {
      title: "Slide 1",
      image: "https://api.builder.io/api/v1/image/assets/TEMP/8109900c3183f447fb448efcb62e2b8cc1208461?width=320",
    },
    {
      title: "Slide 2",
      image: "https://api.builder.io/api/v1/image/assets/TEMP/3083b456257ff9a53db3fcbe7eba04aabb526d44?width=320",
    },
    {
      title: "Slide 3",
      image: "https://api.builder.io/api/v1/image/assets/TEMP/56de945994231ef8e48cf046fe42e3e63f992057?width=320",
    },
    {
      title: "Slide 4",
      image: "https://api.builder.io/api/v1/image/assets/TEMP/7d453d3b9d88e683f8f7d50d3193ffb7cc6c7f7b?width=320",
    },
    {
      title: "Slide 5",
      image: "https://api.builder.io/api/v1/image/assets/TEMP/4cd9c87f62ae3609a47081e1c24daa6bfa493b42?width=320",
    },
  ];

  const outline = [
    "Introduction to Machine Learning",
    "Supervised Learning",
    "Unsupervised Learning",
    "Reinforcement Learning",
    "Conclusion",
  ];

  return (
    <AppLayout>
      <div className="flex flex-1">
        {/* Secondary Sidebar */}
        <div className="flex flex-col w-80">
          <div className="flex h-full min-h-[700px] flex-col justify-between bg-neutral-50 p-4">
            <div className="flex flex-col gap-4">
              <div className="flex flex-col">
                <h1 className="text-[#141414] text-base font-medium leading-normal">
                  Slide Deck Generator
                </h1>
                <p className="text-neutral-500 text-sm font-normal leading-normal">
                  Create professional slide decks from content.
                </p>
              </div>
              <div className="flex flex-col gap-2">
                <button
                  onClick={() => setActiveTab("generator")}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg text-left ${activeTab === "generator" ? "bg-[#ededed]" : ""
                    }`}
                >
                  <p className="text-[#141414] text-sm font-medium leading-normal">
                    Generate Slides
                  </p>
                </button>
                <button
                  onClick={() => setActiveTab("feedback")}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg text-left ${activeTab === "feedback" ? "bg-[#ededed]" : ""
                    }`}
                >
                  <p className="text-[#141414] text-sm font-medium leading-normal">
                    Collect Feedback
                  </p>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex flex-col max-w-[960px] flex-1">
          {activeTab === "generator" ? (
            <>
              {/* Slide Generator View */}
              <div className="flex flex-wrap justify-between gap-3 p-4">
                <p className="text-[#141414] tracking-light text-[32px] font-bold leading-tight min-w-72">
                  Slide Deck Generator
                </p>
              </div>

              {/* Input Fields */}
              <div className="px-4 py-3 space-y-6">
                <div className="flex flex-col gap-2">
                  <label className="text-base font-medium text-[#141414]">Session Topic</label>
                  <input
                    type="text"
                    placeholder="Enter the session topic"
                    className="h-14 px-4 rounded-lg border border-[#dbdbdb] bg-neutral-50 text-base text-[#141414] placeholder:text-neutral-500 outline-none focus:ring-2 focus:ring-[#141414]"
                  />
                </div>

                <div className="flex flex-col gap-2">
                  <label className="text-base font-medium text-[#141414]">Upload Notes</label>
                  <input
                    type="text"
                    placeholder="Upload notes to generate slides"
                    className="h-14 px-4 rounded-lg border border-[#dbdbdb] bg-neutral-50 text-base text-[#141414] placeholder:text-neutral-500 outline-none focus:ring-2 focus:ring-[#141414]"
                  />
                </div>
              </div>

              <div className="px-4 py-3">
                <button className="h-10 px-4 bg-[#141414] text-neutral-50 rounded-lg text-sm font-bold hover:bg-[#141414]/90 transition-colors">
                  Generate Outline
                </button>
              </div>

              {/* AI Generated Outline */}
              <div className="py-5 px-4">
                <h2 className="text-[22px] font-bold text-[#141414] leading-[28px] mb-4">
                  AI-Generated Outline
                </h2>
              </div>

              <div className="space-y-0">
                {outline.map((item, index) => (
                  <div
                    key={index}
                    className="px-4 h-14 flex items-center bg-neutral-50 border-b border-white last:border-b-0"
                  >
                    <p className="text-base text-[#141414] truncate">{item}</p>
                  </div>
                ))}
              </div>

              {/* Slide Preview */}
              <div className="py-5 px-4 mt-6">
                <h2 className="text-[22px] font-bold text-[#141414] leading-[28px] mb-4">
                  Slide Preview
                </h2>
              </div>

              <div className="px-4">
                <div className="flex gap-3 overflow-x-auto pb-4">
                  {slides.map((slide, index) => (
                    <div key={index} className="flex flex-col gap-4 min-w-[160px] flex-1">
                      <img
                        src={slide.image}
                        alt={slide.title}
                        className="w-full h-[90px] object-cover rounded-lg"
                      />
                      <p className="text-base font-medium text-[#141414]">{slide.title}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Styling Template */}
              <div className="py-5 px-4 mt-6">
                <h2 className="text-[22px] font-bold text-[#141414] leading-[28px] mb-4">
                  Styling Template
                </h2>
              </div>

              <div className="px-4 flex flex-wrap gap-3">
                <label className="text-sm font-medium leading-normal flex items-center justify-center rounded-lg border border-[#dbdbdb] px-4 h-11 text-[#141414] has-[:checked]:border-[3px] has-[:checked]:px-3.5 has-[:checked]:border-[#141414] relative cursor-pointer">
                  Academic
                  <input type="radio" className="invisible absolute" name="styling" />
                </label>
                <label className="text-sm font-medium leading-normal flex items-center justify-center rounded-lg border border-[#dbdbdb] px-4 h-11 text-[#141414] has-[:checked]:border-[3px] has-[:checked]:px-3.5 has-[:checked]:border-[#141414] relative cursor-pointer">
                  Minimal
                  <input type="radio" className="invisible absolute" name="styling" />
                </label>
                <label className="text-sm font-medium leading-normal flex items-center justify-center rounded-lg border border-[#dbdbdb] px-4 h-11 text-[#141414] has-[:checked]:border-[3px] has-[:checked]:px-3.5 has-[:checked]:border-[#141414] relative cursor-pointer">
                  Professional
                  <input type="radio" className="invisible absolute" name="styling" />
                </label>
              </div>
            </>
          ) : (
            <>
              {/* Student Feedback View */}
              <div className="flex flex-wrap justify-between gap-3 p-4">
                <p className="text-[#141414] tracking-light text-[32px] font-bold leading-tight min-w-72">
                  Student Feedback
                </p>
              </div>

              <div className="px-4">
                <p className="text-[#141414] text-base font-normal leading-normal pb-3 pt-1">
                  End slide or slide deck footer: Feedback on this presentation
                </p>
              </div>

              <h3 className="text-[#141414] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">
                How was the presentation?
              </h3>

              <div className="flex flex-wrap gap-3 p-4">
                {[1, 2, 3, 4, 5].map((star) => (
                  <label
                    key={star}
                    className="text-sm font-medium leading-normal flex items-center justify-center rounded-lg border border-[#dbdbdb] px-4 h-11 text-[#141414] has-[:checked]:border-[3px] has-[:checked]:px-3.5 has-[:checked]:border-[#141414] relative cursor-pointer"
                  >
                    {star} Star{star !== 1 ? "s" : ""}
                    <input
                      type="radio"
                      className="invisible absolute"
                      name="presentation-feedback"
                    />
                  </label>
                ))}
              </div>

              <h3 className="text-[#141414] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">
                Comments
              </h3>

              <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
                <label className="flex flex-col min-w-40 flex-1">
                  <textarea
                    placeholder="Optional: Add your comments here"
                    className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#141414] focus:outline-0 focus:ring-0 border border-[#dbdbdb] bg-neutral-50 focus:border-[#dbdbdb] min-h-36 placeholder:text-neutral-500 p-[15px] text-base font-normal leading-normal"
                  ></textarea>
                </label>
              </div>

              <div className="flex px-4 py-3 justify-end">
                <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#141414] text-neutral-50 text-sm font-bold leading-normal tracking-[0.015em]">
                  <span className="truncate">Submit Feedback</span>
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </AppLayout>
  );
}
