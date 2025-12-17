import AppLayout from "@/components/AppLayout";

export default function Analytics() {
  const weeklyData = [
    { day: "Mon", height: "80%" },
    { day: "Tue", height: "40%" },
    { day: "Wed", height: "70%" },
    { day: "Thu", height: "100%" },
    { day: "Fri", height: "80%" },
    { day: "Sat", height: "80%" },
    { day: "Sun", height: "20%" },
  ];

  const featureUsage = [
    { name: "Q&A", width: "0%" },
    { name: "Grading", width: "60%" },
    { name: "Feedback", width: "80%" },
    { name: "Resource Sharing", width: "60%" },
  ];

  return (
    <AppLayout showSidebar={false}>
      <div className="flex justify-center w-full">
        <div className="flex flex-col w-full">
          {/* Title Section */}
          <div className="flex flex-wrap justify-between gap-3 p-4">
            <div className="flex min-w-72 flex-col gap-3">
              <p className="text-[#0d141b] tracking-light text-[32px] font-bold leading-tight">
                Dashboard
              </p>
              <p className="text-[#4c739a] text-sm font-normal leading-normal">
                Track your progress and impact with the AI Teaching Assistant.
              </p>
            </div>
          </div>

          {/* Weekly Time Saved */}
          <h2 className="text-[#0d141b] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">
            Weekly Time Saved
          </h2>
          <div className="flex flex-wrap gap-4 px-4 py-6">
            <div className="flex min-w-72 flex-1 flex-col gap-2 rounded-lg border border-[#cfdbe7] p-6">
              <p className="text-[#0d141b] text-base font-medium leading-normal">
                Time Saved (Hours)
              </p>
              <p className="text-[#0d141b] tracking-light text-[32px] font-bold leading-tight truncate">
                15
              </p>
              <p className="text-[#4c739a] text-base font-normal leading-normal">Last 7 Days</p>
              <div className="grid min-h-[180px] grid-flow-col gap-6 grid-rows-[1fr_auto] items-end justify-items-center px-3">
                {weeklyData.map((item) => (
                  <div key={item.day} className="contents">
                    <div
                      className="border-[#4c739a] bg-[#e7edf3] border-t-2 w-full"
                      style={{ height: item.height }}
                    ></div>
                    <p className="text-[#4c739a] text-[13px] font-bold leading-normal tracking-[0.015em]">
                      {item.day}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Feature Usage */}
          <h2 className="text-[#0d141b] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">
            Feature Usage
          </h2>
          <div className="flex flex-wrap gap-4 px-4 py-6">
            <div className="flex min-w-72 flex-1 flex-col gap-2 rounded-lg border border-[#cfdbe7] p-6">
              <p className="text-[#0d141b] text-base font-medium leading-normal">Feature Usage</p>
              <p className="text-[#0d141b] tracking-light text-[32px] font-bold leading-tight truncate">
                120
              </p>
              <p className="text-[#4c739a] text-base font-normal leading-normal">Last 7 Days</p>
              <div className="grid min-h-[180px] gap-x-4 gap-y-6 grid-cols-[auto_1fr] items-center py-3">
                {featureUsage.map((item) => (
                  <div key={item.name} className="contents">
                    <p className="text-[#4c739a] text-[13px] font-bold leading-normal tracking-[0.015em]">
                      {item.name}
                    </p>
                    <div className="h-full flex-1">
                      <div
                        className="border-[#4c739a] bg-[#e7edf3] border-r-2 h-full"
                        style={{ width: item.width }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Overall Performance Impact */}
          <h2 className="text-[#0d141b] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">
            Overall Performance Impact
          </h2>
          <div className="flex flex-wrap gap-4 p-4">
            <div className="flex min-w-[158px] flex-1 flex-col gap-2 rounded-lg p-6 border border-[#cfdbe7]">
              <p className="text-[#0d141b] text-base font-medium leading-normal">
                Tasks Completed
              </p>
              <p className="text-[#0d141b] tracking-light text-2xl font-bold leading-tight">250</p>
            </div>
            <div className="flex min-w-[158px] flex-1 flex-col gap-2 rounded-lg p-6 border border-[#cfdbe7]">
              <p className="text-[#0d141b] text-base font-medium leading-normal">Feedback Given</p>
              <p className="text-[#0d141b] tracking-light text-2xl font-bold leading-tight">180</p>
            </div>
            <div className="flex min-w-[158px] flex-1 flex-col gap-2 rounded-lg p-6 border border-[#cfdbe7]">
              <p className="text-[#0d141b] text-base font-medium leading-normal">
                Resources Shared
              </p>
              <p className="text-[#0d141b] tracking-light text-2xl font-bold leading-tight">50</p>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
