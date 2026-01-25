import { useState } from "react"
import { Sidebar } from "@/components/sidebar"
import { Dashboard } from "@/components/dashboard"
import { ChatInterface } from "@/components/chat-interface"

export function CallSummarizer() {
  const [selectedCall, setSelectedCall] = useState<string | null>(null)
  const [activeView, setActiveView] = useState<"dashboard" | "chat">("dashboard")

  return (
    <div className="flex h-full bg-background">
      <Sidebar activeView={activeView} setActiveView={setActiveView} />
      <div className="flex-1 flex flex-col">
        {activeView === "dashboard" ? (
          <Dashboard selectedCall={selectedCall} setSelectedCall={setSelectedCall} />
        ) : (
          <ChatInterface selectedCall={selectedCall} />
        )}
      </div>
    </div>
  )
}
export default CallSummarizer