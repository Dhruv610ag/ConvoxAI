import { useState, useEffect } from "react"
import { Phone, MessageSquare, Plus, Loader2, FileAudio } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { UserProfile } from "@/components/user-profile"
import { getUserAudioFiles, type AudioFileMetadata } from "@/lib/api"
import { useAuth } from "@/contexts/auth-context"


interface SidebarProps {
  activeView: "dashboard" | "chat"
  setActiveView: (view: "dashboard" | "chat") => void
}

export function Sidebar({ activeView, setActiveView }: SidebarProps) {
  const { user } = useAuth()
  const [audioFiles, setAudioFiles] = useState<AudioFileMetadata[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Load audio files when user is authenticated
  useEffect(() => {
    if (user) {
      loadAudioFiles()
    }
  }, [user])

  const loadAudioFiles = async () => {
    if (!user) return

    setIsLoading(true)
    setError(null)
    try {
      const files = await getUserAudioFiles()
      setAudioFiles(files)
    } catch (err) {
      console.error('Failed to load audio files:', err)
      setError('Failed to load recent calls')
    } finally {
      setIsLoading(false)
    }
  }

  const formatTimeAgo = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMins / 60)
    const diffDays = Math.floor(diffHours / 24)

    if (diffMins < 60) return `${diffMins} min ago`
    if (diffHours < 24) return `${diffHours} hours ago`
    if (diffDays === 1) return '1 day ago'
    return `${diffDays} days ago`
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

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
        <Button 
          className="w-full" 
          size="sm" 
          variant="default"
          onClick={() => setActiveView("dashboard")}
        >
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
        <div className="px-4 py-3 flex items-center justify-between">
          <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Recent Calls</p>
          {isLoading && <Loader2 className="w-3 h-3 animate-spin text-muted-foreground" />}
        </div>
        <ScrollArea className="flex-1">
          {error ? (
            <div className="px-4 py-2">
              <p className="text-xs text-destructive">{error}</p>
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={loadAudioFiles}
                className="mt-2 w-full text-xs"
              >
                Retry
              </Button>
            </div>
          ) : audioFiles.length === 0 && !isLoading ? (
            <div className="px-4 py-2">
              <p className="text-xs text-muted-foreground">No calls yet. Upload an audio file to get started!</p>
            </div>
          ) : (
            <div className="px-2 space-y-1">
              {audioFiles.map((file) => (
                <button
                  key={file.id}
                  className="w-full text-left px-3 py-2.5 rounded-md hover:bg-muted transition-colors group"
                  onClick={() => setActiveView("dashboard")}
                >
                  <div className="flex items-start justify-between">
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <FileAudio className="w-3 h-3 text-primary flex-shrink-0" />
                        <p className="text-sm font-medium text-foreground truncate group-hover:text-primary">
                          {file.filename}
                        </p>
                      </div>
                      <p className="text-xs text-muted-foreground">{formatTimeAgo(file.created_at)}</p>
                    </div>
                    <span className="text-xs text-muted-foreground ml-2 flex-shrink-0">
                      {formatFileSize(file.file_size)}
                    </span>
                  </div>
                </button>
              ))}
            </div>
          )}
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
