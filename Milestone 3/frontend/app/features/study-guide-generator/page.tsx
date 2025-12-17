"use client";

import AppLayout from "@/components/AppLayout";
import { useState } from "react";

export default function ContentTagger() {
  const [activeTab, setActiveTab] = useState<"tagger" | "feedback">("tagger");

  const priorities = [
    { topic: "Introduction to AI", priority: "High Priority" },
    { topic: "Machine Learning Basics", priority: "Medium Priority" },
    { topic: "Deep Learning Concepts", priority: "High Priority" },
    { topic: "Advanced AI Techniques", priority: "Low Priority" },
    { topic: "Conclusion and Q&A", priority: "Medium Priority" },
  ];

  const heatmapTopics = [
    "Introduction to AI",
    "Machine Learning Basics",
    "Deep Learning Concepts",
    "Advanced AI Techniques",
    "Conclusion and Q&A",
  ];

  const heatmapTimestamps = ["0:00", "5:00", "10:00", "15:00", "20:00", "25:00"];

  const heatmapData = [
    [10, 15, 20, 18, 12, 8],
    [5, 25, 35, 40, 38, 30],
    [8, 20, 45, 60, 65, 55],
    [15, 30, 50, 70, 75, 80],
    [20, 25, 30, 35, 40, 45],
  ];

  const getHeatmapColor = (value: number) => {
    if (value < 20) return "bg-green-100";
    if (value < 40) return "bg-yellow-100";
    if (value < 60) return "bg-orange-200";
    return "bg-red-300";
  };

  return (
    <AppLayout>
      <div className="flex flex-1">
        {/* Secondary Sidebar */}
        <div className="flex flex-col w-80">
          <div className="flex h-full min-h-[700px] flex-col justify-between bg-slate-50 p-4">
            <div className="flex flex-col gap-4">
              <div className="flex flex-col">
                <h1 className="text-[#0d141b] text-base font-medium leading-normal">
                  Content Priority Tagger
                </h1>
                <p className="text-[#4c739a] text-sm font-normal leading-normal">
                  Tag and organize lecture content by priority.
                </p>
              </div>
              <div className="flex flex-col gap-2">
                <button
                  onClick={() => setActiveTab("tagger")}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg text-left ${activeTab === "tagger" ? "bg-[#e7edf3]" : ""
                    }`}
                >
                  <p className="text-[#0d141b] text-sm font-medium leading-normal">
                    Tag Content
                  </p>
                </button>
                <button
                  onClick={() => setActiveTab("feedback")}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg text-left ${activeTab === "feedback" ? "bg-[#e7edf3]" : ""
                    }`}
                >
                  <p className="text-[#0d141b] text-sm font-medium leading-normal">
                    Collect Feedback
                  </p>
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex flex-col max-w-[960px] flex-1">
          {activeTab === "tagger" ? (
            <>
              {/* Content Priority Tagger View */}
              <div className="flex flex-wrap justify-between gap-3 p-4">
                <p className="text-[#0d141b] tracking-light text-[32px] font-bold leading-tight min-w-72">
                  Content Priority Tagger
                </p>
              </div>

              {/* Upload Section */}
              <div className="flex flex-col p-4">
                <div className="flex flex-col items-center gap-6 rounded-lg border-2 border-dashed border-[#cfdbe7] px-6 py-14">
                  <div className="flex max-w-[480px] flex-col items-center gap-2">
                    <p className="text-[#0d141b] text-lg font-bold leading-tight tracking-[-0.015em] max-w-[480px] text-center">
                      Upload Lecture Video
                    </p>
                    <p className="text-[#0d141b] text-sm font-normal leading-normal max-w-[480px] text-center">
                      Drag and drop or browse
                    </p>
                  </div>
                  <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#e7edf3] text-[#0d141b] text-sm font-bold leading-normal tracking-[0.015em]">
                    <span className="truncate">Upload</span>
                  </button>
                </div>
              </div>

              {/* Timeline Section */}
              <h2 className="text-[#0d141b] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">
                Timeline with Priority Tags
              </h2>

              {/* Timeline Grid */}
              <div className="grid grid-cols-[40px_1fr] gap-x-2 px-4">
                {priorities.map((item, index) => (
                  <div key={item.topic} className="contents">
                    {index === 0 ? (
                      <div className="flex flex-col items-center gap-1 pt-3">
                        <div className="text-[#0d141b]">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="24px"
                            height="24px"
                            fill="currentColor"
                            viewBox="0 0 256 256"
                          >
                            <path d="M232,128a104,104,0,0,1-208,0c0-41,23.81-78.36,60.66-95.27a8,8,0,0,1,6.68,14.54C60.15,61.59,40,93.27,40,128a88,88,0,0,0,176,0c0-34.73-20.15-66.41-51.34-80.73a8,8,0,0,1,6.68-14.54C208.19,49.64,232,87,232,128Z" />
                          </svg>
                        </div>
                        {index < priorities.length - 1 && (
                          <div className="w-[1.5px] bg-[#cfdbe7] h-2 grow"></div>
                        )}
                      </div>
                    ) : index === priorities.length - 1 ? (
                      <div className="flex flex-col items-center gap-1 pb-3">
                        <div className="w-[1.5px] bg-[#cfdbe7] h-2"></div>
                        <div className="text-[#0d141b]">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="24px"
                            height="24px"
                            fill="currentColor"
                            viewBox="0 0 256 256"
                          >
                            <path d="M232,128a104,104,0,0,1-208,0c0-41,23.81-78.36,60.66-95.27a8,8,0,0,1,6.68,14.54C60.15,61.59,40,93.27,40,128a88,88,0,0,0,176,0c0-34.73-20.15-66.41-51.34-80.73a8,8,0,0,1,6.68-14.54C208.19,49.64,232,87,232,128Z" />
                          </svg>
                        </div>
                      </div>
                    ) : (
                      <div className="flex flex-col items-center gap-1">
                        <div className="w-[1.5px] bg-[#cfdbe7] h-2"></div>
                        <div className="text-[#0d141b]">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="24px"
                            height="24px"
                            fill="currentColor"
                            viewBox="0 0 256 256"
                          >
                            <path d="M232,128a104,104,0,0,1-208,0c0-41,23.81-78.36,60.66-95.27a8,8,0,0,1,6.68,14.54C60.15,61.59,40,93.27,40,128a88,88,0,0,0,176,0c0-34.73-20.15-66.41-51.34-80.73a8,8,0,0,1,6.68-14.54C208.19,49.64,232,87,232,128Z" />
                          </svg>
                        </div>
                        <div className="w-[1.5px] bg-[#cfdbe7] h-2 grow"></div>
                      </div>
                    )}
                    <div className="flex flex-1 flex-col py-3">
                      <p className="text-[#0d141b] text-base font-medium leading-normal">
                        {item.topic}
                      </p>
                      <p className="text-[#4c739a] text-base font-normal leading-normal">
                        {item.priority}
                      </p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Generated Study Guide */}
              <h2 className="text-[#0d141b] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">
                Generated Study Guide
              </h2>
              <p className="text-[#0d141b] text-base font-normal leading-normal pb-3 pt-1 px-4">
                Based on the lecture video and priority tags, a study guide has been generated to
                help students focus on key concepts and areas of high importance. This guide
                includes summaries, key terms, and practice questions.
              </p>

              {/* Confusion Heatmap */}
              <h2 className="text-[#0d141b] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">
                Confusion Heatmap
              </h2>
              <div className="flex px-4 py-3 overflow-x-auto">
                <div className="flex flex-col gap-2 min-w-full">
                  {/* Legend */}
                  <div className="flex gap-4 text-sm text-[#4c739a] mb-2">
                    <div className="flex items-center gap-2">
                      <div className="w-4 h-4 bg-green-100 rounded"></div>
                      <span>Low (0-20)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-4 h-4 bg-yellow-100 rounded"></div>
                      <span>Medium (20-40)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-4 h-4 bg-orange-200 rounded"></div>
                      <span>High (40-60)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-4 h-4 bg-red-300 rounded"></div>
                      <span>Very High (60+)</span>
                    </div>
                  </div>

                  {/* Heatmap Table */}
                  <div className="overflow-x-auto border border-[#cfdbe7] rounded-lg">
                    <table className="border-collapse">
                      <thead>
                        <tr>
                          <th className="bg-slate-100 px-4 py-2 text-left text-sm font-medium text-[#0d141b] border-b border-r border-[#cfdbe7] w-40">
                            Topic
                          </th>
                          {heatmapTimestamps.map((time) => (
                            <th
                              key={time}
                              className="bg-slate-100 px-3 py-2 text-center text-xs font-medium text-[#0d141b] border-b border-r border-[#cfdbe7] w-16"
                            >
                              {time}
                            </th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {heatmapTopics.map((topic, topicIndex) => (
                          <tr key={topic}>
                            <td className="px-4 py-2 text-sm text-[#0d141b] border-b border-r border-[#cfdbe7] font-medium bg-slate-50">
                              {topic}
                            </td>
                            {heatmapData[topicIndex].map((value, timeIndex) => (
                              <td
                                key={`${topicIndex}-${timeIndex}`}
                                className={`px-3 py-3 text-center text-xs font-semibold text-[#0d141b] border-b border-r border-[#cfdbe7] ${getHeatmapColor(
                                  value
                                )}`}
                              >
                                {value}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>

                  <p className="text-xs text-[#4c739a] mt-2">
                    Confusion Level: Displays student confusion scores (0-100) at different
                    timestamps throughout the lecture
                  </p>
                </div>
              </div>
            </>
          ) : (
            <>
              {/* Student Feedback View */}
              <div className="flex flex-wrap justify-between gap-3 p-4">
                <p className="text-[#0d141b] tracking-light text-[32px] font-bold leading-tight min-w-72">
                  Student Feedback
                </p>
              </div>

              <h2 className="text-[#0d141b] text-lg font-bold leading-tight tracking-[-0.015em] px-4 text-left pb-2 pt-4">
                Rate this study guide ⭐️⭐️⭐️⭐️⭐️
              </h2>
              <div className="flex px-4 py-3 justify-start">
                <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#e7edf3] text-[#0d141b] text-sm font-bold leading-normal tracking-[0.015em]">
                  <span className="truncate">Feedback for TA</span>
                </button>
              </div>

              <h3 className="text-[#0d141b] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">
                Was this helpful?
              </h3>
              <div className="flex flex-wrap gap-3 p-4">
                <label className="text-sm font-medium leading-normal flex items-center justify-center rounded-lg border border-[#cfdbe7] px-4 h-11 text-[#0d141b] has-[:checked]:border-[3px] has-[:checked]:px-3.5 has-[:checked]:border-[#1380ec] relative cursor-pointer">
                  Yes
                  <input
                    type="radio"
                    className="invisible absolute"
                    name="helpful-feedback"
                  />
                </label>
                <label className="text-sm font-medium leading-normal flex items-center justify-center rounded-lg border border-[#cfdbe7] px-4 h-11 text-[#0d141b] has-[:checked]:border-[3px] has-[:checked]:px-3.5 has-[:checked]:border-[#1380ec] relative cursor-pointer">
                  No
                  <input
                    type="radio"
                    className="invisible absolute"
                    name="helpful-feedback"
                  />
                </label>
              </div>

              <h3 className="text-[#0d141b] text-lg font-bold leading-tight tracking-[-0.015em] px-4 pb-2 pt-4">
                What could be improved?
              </h3>
              <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
                <label className="flex flex-col min-w-40 flex-1">
                  <textarea
                    placeholder="Enter your feedback here"
                    className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#0d141b] focus:outline-0 focus:ring-0 border border-[#cfdbe7] bg-slate-50 focus:border-[#cfdbe7] min-h-36 placeholder:text-[#4c739a] p-[15px] text-base font-normal leading-normal"
                  ></textarea>
                </label>
              </div>
            </>
          )}
        </div>
      </div>
    </AppLayout>
  );
}
