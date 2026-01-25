import { useState } from "react"
import { Send, Paperclip, Mic } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"

interface ChatInterfaceProps {
  selectedCall: string | null
}

const chatMessages = [
  {
    id: 1,
    role: "assistant",
    content:
      "Hi! I'm your Call Analysis Assistant. Ask me anything about the recent call summary, transcripts, or action items.",
    timestamp: "10:30 AM",
  },
  {
    id: 2,
    role: "user",
    content: "What were the main topics discussed?",
    timestamp: "10:32 AM",
  },
  {
    id: 3,
    role: "assistant",
    content:
      "The call covered three main areas:\n1. Q1 performance metrics review\n2. Feature roadmap discussion\n3. Budget allocation decisions\n\nWould you like more details on any of these topics?",
    timestamp: "10:32 AM",
  },
]

export function ChatInterface({ selectedCall }: ChatInterfaceProps) {
  const [messages, setMessages] = useState(chatMessages)
  const [input, setInput] = useState("")

  const handleSend = () => {
    if (!input.trim()) return

    const newMessage = {
      id: messages.length + 1,
      role: "user",
      content: input,
      timestamp: new Date().toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" }),
    }

    setMessages([...messages, newMessage])
    setInput("")
  }

  return (
    <div className="flex-1 flex flex-col h-full">
      {/* Header */}
      <div className="border-b border-border p-6">
        <h2 className="text-xl font-bold text-foreground">Call Analysis Chat</h2>
        <p className="text-sm text-muted-foreground mt-1">Ask questions about your calls</p>
      </div>

      {/* Messages */}
      <ScrollArea className="flex-1 p-6">
        <div className="space-y-4 max-w-2xl mx-auto">
          {messages.map((message) => (
            <div key={message.id} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
              <div
                className={`max-w-md px-4 py-3 rounded-lg ${
                  message.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted text-foreground"
                }`}
              >
                <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
                <p
                  className={`text-xs mt-2 ${
                    message.role === "user" ? "text-primary-foreground/70" : "text-muted-foreground"
                  }`}
                >
                  {message.timestamp}
                </p>
              </div>
            </div>
          ))}
        </div>
      </ScrollArea>

      {/* Input */}
      <div className="border-t border-border p-6">
        <div className="max-w-2xl mx-auto">
          <div className="flex gap-3">
            <Button variant="ghost" size="icon" className="text-muted-foreground">
              <Paperclip className="w-4 h-4" />
            </Button>
            <div className="flex-1 flex gap-2">
              <Input
                placeholder="Ask about the call..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleSend()}
                className="bg-muted border-0 text-foreground placeholder:text-muted-foreground"
              />
              <Button variant="ghost" size="icon" className="text-muted-foreground">
                <Mic className="w-4 h-4" />
              </Button>
            </div>
            <Button
              onClick={handleSend}
              disabled={!input.trim()}
              className="bg-primary text-primary-foreground hover:bg-primary/90"
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
export default ChatInterface