import { Phone, MessageSquare, Plus } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { UserProfile } from "@/components/user-profile"


interface SidebarProps {
  activeView: "dashboard" | "chat"
  setActiveView: (view: "dashboard" | "chat") => void
}

const recentCalls = [
  { id: "1", name: "Client Meeting", time: "2 hours ago", duration: "45 min" },
  { id: "2", name: "Team Sync", time: "4 hours ago", duration: "30 min" },
  { id: "3", name: "Product Demo", time: "1 day ago", duration: "60 min" },
  { id: "4", name: "Strategy Session", time: "2 days ago", duration: "90 min" },
  { id: "5", name: "Sales Call", time: "3 days ago", duration: "25 min" },
]

export function Sidebar({ activeView, setActiveView }: SidebarProps) {
  return (
    <aside className="w-64 bg-card border-r border-border flex flex-col h-full">
      {/* Header */}
      <div className="p-6 border-b border-border">
        <div className="flex items-center gap-2 mb-6">
          <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
            <Phone className="w-4 h-4 text-primary-foreground" />
          </div>
          <h1 className="text-lg font-semibold text-foreground">CallSum</h1>
        </div>
        <Button className="w-full" size="sm" variant="default">
          <Plus className="w-4 h-4 mr-2" />
          New Call
        </Button>
      </div>

      {/* Navigation */}
      <div className="px-4 py-4 border-b border-border flex gap-2">
        <button
          onClick={() => setActiveView("dashboard")}
          className={`flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
            activeView === "dashboard" ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:bg-muted"
          }`}
        >
          <Phone className="w-4 h-4" />
          Dashboard
        </button>
        <button
          onClick={() => setActiveView("chat")}
          className={`flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
            activeView === "chat" ? "bg-primary text-primary-foreground" : "text-muted-foreground hover:bg-muted"
          }`}
        >
          <MessageSquare className="w-4 h-4" />
          Chat
        </button>
      </div>

      {/* Recent Calls */}
      <div className="flex-1 flex flex-col">
        <div className="px-4 py-3">
          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Recent Calls</p>
        </div>
        <ScrollArea className="flex-1">
          <div className="px-2 space-y-1">
            {recentCalls.map((call) => (
              <button
                key={call.id}
                className="w-full text-left px-3 py-2.5 rounded-md hover:bg-muted transition-colors group"
              >
                <div className="flex items-start justify-between">
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium text-foreground truncate group-hover:text-primary">{call.name}</p>
                    <p className="text-xs text-muted-foreground">{call.time}</p>
                  </div>
                  <span className="text-xs text-muted-foreground ml-2 flex-shrink-0">{call.duration}</span>
                </div>
              </button>
            ))}
          </div>
        </ScrollArea>
      </div>

      {/* Footer - User Profile */}
      <div className="p-4 border-t border-border">
        <UserProfile />
      </div>
    </aside>
  )
}
export default Sidebar
