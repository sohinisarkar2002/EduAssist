"use client";

import AppLayout from "@/components/AppLayout";
import { useState } from "react";

export default function Assessment() {
  const [difficultyLevel, setDifficultyLevel] = useState(50);
  const [activeTab, setActiveTab] = useState<"assessment" | "feedback">("assessment");

  const questions = [
    { question: "Explain the concept of recursion with an example.", marks: "5" },
    { question: "What are the differences between arrays and linked lists?", marks: "4" },
    { question: "Describe the time complexity of binary search.", marks: "3" },
    { question: "Implement a function to reverse a string.", marks: "6" },
    { question: "Discuss the advantages and disadvantages of using a hash table.", marks: "4" },
  ];

  const feedbackQuestions = [
    { id: 1, question: "How clear was the assessment?" },
    { id: 2, question: "How relevant were the questions?" },
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
                  Assessment Generator
                </h1>
                <p className="text-neutral-500 text-sm font-normal leading-normal">
                  Create and manage assessments with AI assistance.
                </p>
              </div>
              <div className="flex flex-col gap-2">
                <button
                  onClick={() => setActiveTab("assessment")}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg text-left ${activeTab === "assessment" ? "bg-[#ededed]" : ""
                    }`}
                >
                  <p className="text-[#141414] text-sm font-medium leading-normal">
                    Generate Assessment
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
          {activeTab === "assessment" ? (
            <>
              {/* Assessment Generator View */}
              <div className="flex flex-wrap justify-between gap-3 p-4">
                <p className="text-[#141414] tracking-light text-[32px] font-bold leading-tight min-w-72">
                  Automated Assessment Generator
                </p>
              </div>

              {/* Assessment Configuration */}
              <h3 className="text-[#141414] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">
                Assessment Configuration
              </h3>

              {/* Topic Selector */}
              <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
                <label className="flex flex-col min-w-40 flex-1">
                  <select className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#141414] focus:outline-0 focus:ring-0 border border-[#dbdbdb] bg-neutral-50 focus:border-[#dbdbdb] h-14 placeholder:text-neutral-500 p-[15px] text-base font-normal leading-normal appearance-none bg-[length:20px_20px] bg-[position:calc(100%-12px)_center] bg-no-repeat cursor-pointer"
                    style={{
                      backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='24px' height='24px' fill='rgb(115,115,115)' viewBox='0 0 256 256'%3e%3cpath d='M181.66,170.34a8,8,0,0,1,0,11.32l-48,48a8,8,0,0,1-11.32,0l-48-48a8,8,0,0,1,11.32-11.32L128,212.69l42.34-42.35A8,8,0,0,1,181.66,170.34Zm-96-84.68L128,43.31l42.34,42.35a8,8,0,0,0,11.32-11.32l-48-48a8,8,0,0,0-11.32,0l-48,48A8,8,0,0,0,85.66,85.66Z'%3e%3c/path%3e%3c/svg%3e")`
                    }}
                  >
                    <option value="one">Select Topic</option>
                    <option value="two">Data Structures</option>
                    <option value="three">Algorithms</option>
                  </select>
                </label>
              </div>

              {/* Difficulty Level Slider */}
              <div className="px-4">
                <div className="relative flex w-full flex-col items-start justify-between gap-3 p-4">
                  <div className="flex w-full shrink-[3] items-center justify-between">
                    <p className="text-[#141414] text-base font-medium leading-normal">
                      Difficulty Level
                    </p>
                    <p className="text-[#141414] text-sm font-normal leading-normal md:hidden">
                      {difficultyLevel}
                    </p>
                  </div>
                  <div className="flex h-4 w-full items-center gap-4">
                    <div className="flex h-1 flex-1 rounded-sm bg-[#dbdbdb] relative">
                      <div
                        className="h-full rounded-sm bg-[#141414]"
                        style={{ width: `${difficultyLevel}%` }}
                      ></div>
                      <div
                        className="absolute -top-1.5"
                        style={{ left: `${difficultyLevel}%` }}
                      >
                        <div className="relative -left-2">
                          <div className="size-4 rounded-full bg-[#141414] cursor-pointer"></div>
                        </div>
                      </div>
                    </div>
                    <p className="text-[#141414] text-sm font-normal leading-normal hidden md:block">
                      {difficultyLevel}
                    </p>
                  </div>
                </div>
              </div>

              {/* Number of Questions Input */}
              <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
                <label className="flex flex-col min-w-40 flex-1">
                  <input
                    type="text"
                    placeholder="Number of Questions"
                    className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#141414] focus:outline-0 focus:ring-0 border border-[#dbdbdb] bg-neutral-50 focus:border-[#dbdbdb] h-14 placeholder:text-neutral-500 p-[15px] text-base font-normal leading-normal"
                  />
                </label>
              </div>

              {/* Generate Button */}
              <div className="flex px-4 py-3 justify-end">
                <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#141414] text-neutral-50 text-sm font-bold leading-normal tracking-[0.015em]">
                  <span className="truncate">Generate Questions</span>
                </button>
              </div>

              {/* Generated Questions */}
              <h3 className="text-[#141414] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">
                Generated Questions
              </h3>

              {/* Questions Table */}
              <div className="px-4 py-3">
                <div className="flex overflow-hidden rounded-lg border border-[#dbdbdb] bg-neutral-50">
                  <table className="flex-1">
                    <thead>
                      <tr className="bg-neutral-50">
                        <th className="px-4 py-3 text-left text-[#141414] w-[400px] text-sm font-medium leading-normal">
                          Question
                        </th>
                        <th className="px-4 py-3 text-left text-[#141414] w-[400px] text-sm font-medium leading-normal">
                          Marks
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {questions.map((item, index) => (
                        <tr key={index} className="border-t border-t-[#dbdbdb]">
                          <td className="h-[72px] px-4 py-2 w-[400px] text-neutral-500 text-sm font-normal leading-normal">
                            {item.question}
                          </td>
                          <td className="h-[72px] px-4 py-2 w-[400px] text-neutral-500 text-sm font-normal leading-normal">
                            {item.marks}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
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

              {feedbackQuestions.map((feedback) => (
                <div key={feedback.id}>
                  <h3 className="text-[#141414] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">
                    {feedback.question}
                  </h3>

                  {/* Feedback Textarea */}
                  <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
                    <label className="flex flex-col min-w-40 flex-1">
                      <textarea
                        placeholder={`Please provide your feedback for: ${feedback.question}`}
                        className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#141414] focus:outline-0 focus:ring-0 border border-[#dbdbdb] bg-neutral-50 focus:border-[#dbdbdb] min-h-36 placeholder:text-neutral-500 p-[15px] text-base font-normal leading-normal"
                      ></textarea>
                    </label>
                  </div>

                  {/* Star Rating */}
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
                          name={`feedback-${feedback.id}`}
                        />
                      </label>
                    ))}
                  </div>
                </div>
              ))}
            </>
          )}
        </div>
      </div>
    </AppLayout>
  );
}
