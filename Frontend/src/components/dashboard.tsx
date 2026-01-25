import { useState, useRef } from "react"
import { MoreVertical, Play, Download, Share2, Upload, FileAudio, X, Loader2 } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { AnimatedThemeToggler } from "./ui/animated-theme-toggler"
import { summarizeAudio } from "@/lib/api"
import type { SummaryResponse } from "@/types/api"


interface DashboardProps {
  selectedCall: string | null
  setSelectedCall: (id: string | null) => void
}

export function Dashboard({ selectedCall, setSelectedCall }: DashboardProps) {
  const [summaryData, setSummaryData] = useState<SummaryResponse | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const allowedExtensions = ['.wav', '.mp3', '.m4a', '.flac', '.ogg']
  const allowedMimeTypes = ['audio/wav', 'audio/mpeg', 'audio/mp4', 'audio/x-m4a', 'audio/flac', 'audio/ogg']

  const handleFileSelect = (file: File) => {
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
    
    if (!allowedExtensions.includes(fileExtension) && !allowedMimeTypes.includes(file.type)) {
      setError(`Invalid file format. Supported formats: ${allowedExtensions.join(', ')}`)
      return
    }

    setSelectedFile(file)
    setError(null)
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      handleFileSelect(file)
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    
    const file = e.dataTransfer.files?.[0]
    if (file) {
      handleFileSelect(file)
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) return

    setIsUploading(true)
    setError(null)

    try {
      const response = await summarizeAudio(selectedFile)
      setSummaryData(response)
      setSelectedFile(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to process audio file')
    } finally {
      setIsUploading(false)
    }
  }

  const clearFile = () => {
    setSelectedFile(null)
    setError(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  return (
    <div className="flex-1 overflow-auto">
      <div className="p-8">
        {/* Header */}
        <div className="mb-8 flex items-start justify-between">
          <div>
            <h2 className="text-3xl font-bold text-foreground mb-2">Call Summary</h2>
            <p className="text-muted-foreground">
              {summaryData ? 'Analysis Complete' : 'Upload an audio file to get started'}
            </p>
          </div>
          <div className="flex gap-2">
            <AnimatedThemeToggler className="pr-4" />
            {summaryData && (
              <>
                <Button variant="outline" size="icon">
                  <Play className="w-4 h-4" />
                </Button>
                <Button variant="outline" size="icon">
                  <Download className="w-4 h-4" />
                </Button>
                <Button variant="outline" size="icon">
                  <Share2 className="w-4 h-4" />
                </Button>
                <Button variant="ghost" size="icon">
                  <MoreVertical className="w-4 h-4" />
                </Button>
              </>
            )}
          </div>
        </div>

        {/* File Upload Section */}
        {!summaryData && (
          <Card className="mb-8 bg-card border-border">
            <CardContent className="pt-6">
              <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                  isDragging
                    ? 'border-primary bg-primary/5'
                    : 'border-muted-foreground/25 hover:border-primary/50'
                }`}
              >
                <FileAudio className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
                <h3 className="text-lg font-semibold mb-2 text-foreground">Upload Audio File</h3>
                <p className="text-sm text-muted-foreground mb-4">
                  Drag and drop your audio file here, or click to browse
                </p>
                <p className="text-xs text-muted-foreground mb-4">
                  Supported formats: WAV, MP3, M4A, FLAC, OGG
                </p>
                
                <input
                  ref={fileInputRef}
                  type="file"
                  accept={allowedExtensions.join(',')}
                  onChange={handleFileChange}
                  className="hidden"
                />
                
                <Button
                  onClick={() => fileInputRef.current?.click()}
                  variant="outline"
                  disabled={isUploading}
                >
                  <Upload className="w-4 h-4 mr-2" />
                  Select File
                </Button>
              </div>

              {selectedFile && (
                <div className="mt-4 p-4 bg-muted rounded-lg flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <FileAudio className="w-5 h-5 text-primary" />
                    <div>
                      <p className="text-sm font-medium text-foreground">{selectedFile.name}</p>
                      <p className="text-xs text-muted-foreground">
                        {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      onClick={handleUpload}
                      disabled={isUploading}
                      size="sm"
                    >
                      {isUploading ? (
                        <>
                          <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                          Processing...
                        </>
                      ) : (
                        'Upload & Analyze'
                      )}
                    </Button>
                    <Button
                      onClick={clearFile}
                      disabled={isUploading}
                      variant="ghost"
                      size="sm"
                    >
                      <X className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              )}

              {error && (
                <div className="mt-4 p-4 bg-destructive/10 border border-destructive/20 rounded-lg">
                  <p className="text-sm text-destructive">{error}</p>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Call Metrics */}
        {summaryData && (
          <>
            <div className="grid grid-cols-4 gap-4 mb-8">
              <Card className="bg-card border-border">
                <CardContent className="pt-6">
                  <p className="text-xs text-muted-foreground uppercase tracking-wide mb-2">Duration</p>
                  <p className="text-2xl font-bold text-foreground">
                    {/* {summaryData.duration ? `${Math.floor(summaryData.duration / 60)}:${String(summaryData.duration % 60).padStart(2, '0')}` : 'N/A'} */}
                    {summaryData.duration_minutes}
                  </p>
                  <p className="text-xs text-muted-foreground mt-2">minutes</p>
                </CardContent>
              </Card>
              <Card className="bg-card border-border">
                <CardContent className="pt-6">
                  <p className="text-xs text-muted-foreground uppercase tracking-wide mb-2">Participants</p>
                  <p className="text-2xl font-bold text-foreground">{summaryData.no_of_participants}</p>
                  <p className="text-xs text-muted-foreground mt-2">people</p>
                </CardContent>
              </Card>
              <Card className="bg-card border-border">
                <CardContent className="pt-6">
                  <p className="text-xs text-muted-foreground uppercase tracking-wide mb-2">Sentiment</p>
                  <p className="text-2xl font-bold text-foreground">{summaryData.sentiment || 'N/A'}</p>
                  <p className="text-xs text-muted-foreground mt-2">overall mood</p>
                </CardContent>
              </Card>
              <Card className="bg-card border-border">
                <CardContent className="pt-6">
                  <p className="text-xs text-muted-foreground uppercase tracking-wide mb-2">Key Topics</p>
                  <p className="text-2xl font-bold text-foreground">{summaryData.key_aspects?.length || 0}</p>
                  <p className="text-xs text-muted-foreground mt-2">identified</p>
                </CardContent>
              </Card>
            </div>

            {/* Tabs */}
            <Tabs defaultValue="summary" className="w-full">
              <TabsList className="bg-muted mb-6">
                <TabsTrigger value="summary">Summary</TabsTrigger>
                <TabsTrigger value="transcript">Transcript</TabsTrigger>
                <TabsTrigger value="insights">Key Insights</TabsTrigger>
              </TabsList>

              <TabsContent value="summary" className="space-y-4">
                <Card className="bg-card border-border">
                  <CardHeader>
                    <CardTitle className="text-base">Executive Summary</CardTitle>
                  </CardHeader>
                  <CardContent className="text-sm text-foreground leading-relaxed space-y-3">
                    <p>{summaryData.summary}</p>
                  </CardContent>
                </Card>
                <Button
                  onClick={() => setSummaryData(null)}
                  variant="outline"
                  className="w-full"
                >
                  <Upload className="w-4 h-4 mr-2" />
                  Upload Another File
                </Button>
              </TabsContent>

              <TabsContent value="transcript" className="space-y-4">
                <Card className="bg-card border-border">
                  <CardContent className="pt-6">
                    <div className="space-y-4 text-sm">
                      <p className="text-foreground whitespace-pre-wrap">
                        {summaryData.transcript || 'Transcript not available'}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="insights" className="space-y-3">
                {summaryData.key_aspects && summaryData.key_aspects.length > 0 ? (
                  summaryData.key_aspects.map((topic, i) => (
                    <Card key={i} className="bg-card border-border">
                      <CardContent className="pt-6 flex items-start gap-3">
                        <div className="w-2 h-2 bg-primary rounded-full mt-1.5 flex-shrink-0"></div>
                        <p className="text-sm text-foreground">{topic}</p>
                      </CardContent>
                    </Card>
                  ))
                ) : (
                  <Card className="bg-card border-border">
                    <CardContent className="pt-6">
                      <p className="text-sm text-muted-foreground">No key topics identified</p>
                    </CardContent>
                  </Card>
                )}
              </TabsContent>
            </Tabs>
          </>
        )}
      </div>
    </div>
  )
}
export default Dashboard