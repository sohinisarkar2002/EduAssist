import AppLayout from "@/components/AppLayout";
import { Search, HelpCircle } from "lucide-react";

export default function KnowledgeAssistant() {
  const recentQuestions = [
    {
      question: "What is quantum entanglement?",
      answer: "The concept of 'quantum entanglement' refers to a physical phenomenon where two or more particles become linked in such a way that they share the same fate, even when separated by large distances. This means that the quantum state of each particle cannot be described independently of the state of the others, even if the particles are far apart. When you measure a property of one particle, you instantly know the corresponding property of the other particle, regardless of the distance between them. This is because the particles are entangled, and their fates are intertwined. This concept is fundamental to quantum mechanics and has been experimentally verified. It's important to note that entanglement does not allow for faster-than-light communication, as the measurement outcome on one particle is random and cannot be controlled to send a specific message.",
      confidence: "High",
      timeAgo: "2 hours ago",
    },
    {
      question: "Explain the Central Limit Theorem.",
      answer: "The 'Central Limit Theorem' (CLT) is a fundamental concept in probability theory and statistics. It states that the distribution of the sum (or average) of a large number of independent, identically distributed random variables will be approximately normally distributed, regardless of the original distribution of the variables. This holds true as long as the random variables have a finite variance. In simpler terms, if you repeatedly sample from any population (with a finite variance) and calculate the mean of each sample, the distribution of these sample means will tend towards a normal distribution as the sample size increases. The CLT is crucial because it allows us to make inferences about population parameters (like the mean) even when we don't know the exact distribution of the population, as long as we have a sufficiently large sample size.",
      confidence: "Medium",
      timeAgo: "4 hours ago",
    },
    {
      question: "What is the Traveling Salesman Problem?",
      answer: "The 'Traveling Salesman Problem' (TSP) is a classic optimization problem in computer science and operations research. It asks the following question: Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city? This problem is NP-hard, meaning that there is no known efficient algorithm to find the optimal solution for large instances of the problem. However, there are various heuristic and approximation algorithms that can find good solutions in a reasonable amount of time. The TSP has many practical applications, such as in logistics, transportation, and circuit board design, where finding the most efficient route is crucial.",
      confidence: "Low",
      timeAgo: "6 hours ago",
    },
  ];

  return (
    <AppLayout>
      <div className="flex h-[calc(100vh-57px)]">
        {/* Main Content */}
        <div className="flex-1 flex flex-col max-w-[920px] mx-auto w-full p-4 sm:p-6 overflow-auto">
          {/* Title */}
          <div className="p-4 mb-4">
            <h1 className="text-[32px] font-bold text-[#0D141C] leading-[40px]">
              AI Knowledge Assistant
            </h1>
          </div>

          {/* Search Bar */}
          <div className="px-4 pb-3">
            <div className="flex items-center bg-[#E8EDF2] rounded-lg overflow-hidden">
              <div className="flex items-center justify-center px-4">
                <Search className="w-6 h-6 text-[#4D7399]" />
              </div>
              <input
                type="text"
                placeholder="Search student questions"
                className="flex-1 py-3 px-2 bg-transparent text-base text-[#4D7399] placeholder:text-[#4D7399] outline-none"
              />
            </div>
          </div>

          {/* Recent Questions */}
          <div className="py-5 px-4">
            <h2 className="text-[22px] font-bold text-[#0D141C] leading-[28px]">Recent Questions</h2>
          </div>

          {/* Questions List */}
          <div className="flex flex-col gap-0">
            {recentQuestions.map((item, index) => (
              <div key={index} className="px-4 py-3 bg-[#F7FAFC] flex gap-4 items-start">
                <div className="w-12 h-12 rounded-lg bg-[#E8EDF2] flex items-center justify-center flex-shrink-0">
                  <HelpCircle className="w-6 h-6 text-[#0D141C]" />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-base font-medium text-[#0D141C] mb-1">{item.question}</h3>
                  <p className="text-sm text-[#4D7399] leading-[21px] mb-1">{item.answer}</p>
                  <p className="text-sm text-[#4D7399]">Confidence: {item.confidence}</p>
                </div>
                <div className="flex-shrink-0 text-sm text-[#4D7399]">{item.timeAgo}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Sidebar */}
        <div className="hidden xl:block w-[360px] border-l border-[#E5E8EB] bg-white">
          <div className="p-4 sticky top-0">
            <div className="py-5 px-4">
              <h2 className="text-[22px] font-bold text-[#0D141C] leading-[28px] mb-4">AI Response</h2>
            </div>
            <div className="px-4 pb-3">
              <p className="text-base text-[#0D141C] leading-6">
                The concept of 'quantum entanglement' refers to a physical phenomenon where two or more
                particles become linked in such a way that they share the same fate, even when separated
                by large distances. This means that the quantum state of each particle cannot be described
                independently of the state of the others, even if the particles are far apart. When you
                measure a property of one particle, you instantly know the corresponding property of the
                other particle, regardless of the distance between them. This is because the particles are
                entangled, and their fates are intertwined. This concept is fundamental to quantum
                mechanics and has been experimentally verified. It's important to note that entanglement
                does not allow for faster-than-light communication, as the measurement outcome on one
                particle is random and cannot be controlled to send a specific message.
              </p>
            </div>

            <div className="py-5 px-4">
              <h3 className="text-[22px] font-bold text-[#0D141C] leading-[28px] mb-4">Citations</h3>
            </div>

            <div className="space-y-0">
              <div className="px-4 py-3 bg-[#F7FAFC] flex items-center gap-4">
                <div className="w-10 h-10 rounded-lg bg-[#E8EDF2] flex items-center justify-center flex-shrink-0">
                  <FileText className="w-6 h-6 text-[#0D141C]" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-base text-[#0D141C] truncate">
                    Quantum Mechanics: Concepts and Applications by Dr. Anya Sharma
                  </p>
                </div>
              </div>
              <div className="px-4 py-3 bg-[#F7FAFC] flex items-center gap-4">
                <div className="w-10 h-10 rounded-lg bg-[#E8EDF2] flex items-center justify-center flex-shrink-0">
                  <FileText className="w-6 h-6 text-[#0D141C]" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-base text-[#0D141C] truncate">
                    Experimental Verification of Quantum Entanglement by Dr. Ben Carter
                  </p>
                </div>
              </div>
            </div>

            <div className="py-5 px-4">
              <h3 className="text-[22px] font-bold text-[#0D141C] leading-[28px] mb-4">
                Analytics Summary
              </h3>
            </div>

            <div className="px-4 flex flex-wrap gap-4">
              <div className="flex-1 min-w-[158px] p-6 rounded-lg border border-[#CFDBE8]">
                <div className="text-base font-medium text-[#0D141C] mb-2">Total Questions</div>
                <div className="text-2xl font-bold text-[#0D141C]">120</div>
              </div>
              <div className="flex-1 min-w-[158px] p-6 rounded-lg border border-[#CFDBE8]">
                <div className="text-base font-medium text-[#0D141C] mb-2">Answered</div>
                <div className="text-2xl font-bold text-[#0D141C]">105</div>
              </div>
              <div className="flex-1 min-w-[158px] p-6 rounded-lg border border-[#CFDBE8]">
                <div className="text-base font-medium text-[#0D141C] mb-2">Unanswered</div>
                <div className="text-2xl font-bold text-[#0D141C]">15</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}

function FileText(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg width="17" height="20" viewBox="0 0 17 20" fill="none" xmlns="http://www.w3.org/2000/svg" {...props}>
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M16.2806 5.46938L11.0306 0.219375C10.8899 0.0787585 10.699 -0.000156403 10.5 0H1.5C0.671573 0 0 0.671573 0 1.5V18C0 18.8284 0.671573 19.5 1.5 19.5H15C15.8284 19.5 16.5 18.8284 16.5 18V6C16.5002 5.80103 16.4212 5.61015 16.2806 5.46938ZM11.25 2.56031L13.9397 5.25H11.25V2.56031ZM15 18H1.5V1.5H9.75V6C9.75 6.41421 10.0858 6.75 10.5 6.75H15V18Z"
        fill="currentColor"
      />
    </svg>
  );
}
