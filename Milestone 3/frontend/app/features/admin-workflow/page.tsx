"use client";

import AppLayout from "@/components/AppLayout";
import { Inbox, File, Send, Archive, Trash } from "lucide-react";

export default function AdminWorkflow() {
  const sidebarItems = [
    { label: "Inbox", icon: Inbox, active: true },
    { label: "Drafts", icon: File, active: false },
    { label: "Sent", icon: Send, active: false },
    { label: "Archived", icon: Archive, active: false },
    { label: "Deleted", icon: Trash, active: false },
  ];

  return (
    <AppLayout>
      <div className="flex flex-1">
        {/* Secondary Sidebar */}
        <div className="layout-content-container flex flex-col w-80">
          <div className="flex h-full min-h-[700px] flex-col justify-between bg-slate-50 p-4">
            <div className="flex flex-col gap-4">
              <div className="flex flex-col gap-2">
                {sidebarItems.map((item, index) => {
                  const Icon = item.icon;
                  return (
                    <div
                      key={index}
                      className={`flex items-center gap-3 px-3 py-2 rounded-lg ${item.active ? "bg-[#e7edf3]" : ""
                        }`}
                    >
                      <div className="text-[#0d141b]">
                        <Icon className="w-6 h-6" />
                      </div>
                      <p className="text-[#0d141b] text-sm font-medium leading-normal">
                        {item.label}
                      </p>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
          {/* Title */}
          <div className="flex flex-wrap justify-between gap-3 p-4">
            <p className="text-[#0d141b] tracking-light text-[32px] font-bold leading-tight min-w-72">
              Extension Requests
            </p>
          </div>

          {/* Request Header */}
          <div className="flex items-center gap-4 bg-slate-50 px-4 min-h-[72px] py-2 justify-between">
            <div className="flex flex-col justify-center">
              <p className="text-[#0d141b] text-base font-medium leading-normal line-clamp-1">
                Student: Alex Chen
              </p>
              <p className="text-[#4c739a] text-sm font-normal leading-normal line-clamp-2">
                Assignment 2 - Deadline Extension
              </p>
            </div>
            <div className="shrink-0">
              <p className="text-[#4c739a] text-sm font-normal leading-normal">2d ago</p>
            </div>
          </div>

          {/* Request Summary */}
          <h2 className="text-[#0d141b] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">
            Request Summary
          </h2>
          <p className="text-[#0d141b] text-base font-normal leading-normal pb-3 pt-1 px-4">
            Alex Chen, a student in your class, has requested an extension for Assignment 2 due
            to a family emergency. They have attached supporting documentation. The student's
            current grade in the course is a B+, and they have not requested any extensions
            previously.
          </p>

          {/* AI Recommendation */}
          <h2 className="text-[#0d141b] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">
            AI Recommendation
          </h2>
          <p className="text-[#0d141b] text-base font-normal leading-normal pb-3 pt-1 px-4">
            Based on the student's academic history, the provided documentation, and the course
            extension policy, the AI recommends approving the extension request.
          </p>

          {/* Draft Email */}
          <h2 className="text-[#0d141b] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">
            Draft Email
          </h2>
          <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
            <label className="flex flex-col min-w-40 flex-1">
              <p className="text-[#0d141b] text-base font-medium leading-normal pb-2">
                Email Preview
              </p>
              <textarea
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#0d141b] focus:outline-0 focus:ring-0 border border-[#cfdbe7] bg-slate-50 focus:border-[#cfdbe7] min-h-36 placeholder:text-[#4c739a] p-[15px] text-base font-normal leading-normal"
                placeholder="Email content..."
                defaultValue="Dear Alex,

Thank you for reaching out regarding your request for an extension on Assignment 2. After reviewing your situation and the supporting documentation you provided, I am pleased to approve your extension request.

You will have an additional 7 days to complete and submit the assignment. The new deadline is [date].

Please let me know if you need any additional support or have questions about the assignment.

Best regards,
[Your Name]"
              />
            </label>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-stretch">
            <div className="flex flex-1 gap-3 flex-wrap px-4 py-3 justify-end">
              <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#e7edf3] text-[#0d141b] text-sm font-bold leading-normal tracking-[0.015em]">
                <span className="truncate">Deny</span>
              </button>
              <button className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 bg-[#1380ec] text-slate-50 text-sm font-bold leading-normal tracking-[0.015em]">
                <span className="truncate">Approve</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
