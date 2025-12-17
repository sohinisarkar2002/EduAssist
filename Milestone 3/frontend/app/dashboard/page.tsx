import Link from "next/link";
import AppLayout from "@/components/AppLayout";
import { GraduationCap, Book, Users, FileText, Presentation } from "lucide-react";

export default function Page() {
  const tools = [
    {
      title: "Knowledge Assistant",
      description: "Get instant answers to student queries.",
      image: "https://api.builder.io/api/v1/image/assets/TEMP/ff8ac35bba17610bbaef00d2a1a2673a74f8a185?width=332",
      link: "/knowledge-assistant",
    },
    {
      title: "Study Guide Generator",
      description: "Generate comprehensive study guides.",
      image: "https://api.builder.io/api/v1/image/assets/TEMP/475baaa591c5daa5278ef3b2a42ec72f9890ed27?width=332",
      link: "/study-guide",
    },
    {
      title: "Admin Workflow Agent",
      description: "Automate administrative tasks.",
      image: "https://api.builder.io/api/v1/image/assets/TEMP/7447fa5ac6a790380b255201fbd9710106627d37?width=332",
      link: "/admin-workflow",
    },
    {
      title: "Assessment Generator",
      description: "Create assessments quickly.",
      image: "https://api.builder.io/api/v1/image/assets/TEMP/7d3a98010bb014cd3f015ef22832921320f5b20b?width=332",
      link: "/assessment",
    },
    {
      title: "Slide Deck Creator",
      description: "Design engaging slide decks.",
      image: "https://api.builder.io/api/v1/image/assets/TEMP/4f0abf590a8fb876c4c7303fe90ae9ea19393b50?width=332",
      link: "/slides",
    },
  ];

  return (
    <AppLayout>
      <div className="max-w-[960px] mx-auto py-4 px-4 sm:px-6">
        {/* Page Title */}
        <div className="p-4 mb-4">
          <h1 className="text-[32px] font-bold text-[#0D141C] leading-[40px]">Dashboard</h1>
        </div>

        {/* AI Tools Section */}
        <div className="py-5 px-4">
          <h2 className="text-[22px] font-bold text-[#0D141C] leading-[28px] mb-3">AI Tools</h2>
        </div>

        <div className="p-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {tools.map((tool, index) => (
              <Link
                key={index}
                href={tool.link}
                className="flex flex-col gap-3 pb-3 group hover:opacity-80 transition-opacity"
              >
                <img
                  src={tool.image}
                  alt={tool.title}
                  className="w-full aspect-square object-cover rounded-lg"
                />
                <div className="flex flex-col gap-1">
                  <h3 className="text-base font-medium text-[#0D141C]">{tool.title}</h3>
                  <p className="text-sm text-[#4D7399]">{tool.description}</p>
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* Analytics Section */}
        <div className="py-5 px-4 mt-6">
          <h2 className="text-[22px] font-bold text-[#0D141C] leading-[28px] mb-3">Analytics</h2>
        </div>

        <div className="p-4">
          <div className="flex flex-wrap gap-4">
            <div className="flex-1 min-w-[158px] p-6 rounded-lg border border-[#CFDBE8] flex flex-col gap-2">
              <div className="text-base font-medium text-[#0D141C]">Time Saved</div>
              <div className="text-2xl font-bold text-[#0D141C]">25 hours</div>
              <div className="text-base font-medium text-[#088738]">+10%</div>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
