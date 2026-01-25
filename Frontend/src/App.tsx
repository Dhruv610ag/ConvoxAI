import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/auth-context';
import { AuthPage } from './components/auth/auth-page';
import { ProtectedRoute } from './components/protected-route';
import CallSummarizer from "./components/call-summarizer"
import { AnimatedThemeToggler } from "./components/ui/animated-theme-toggler"
import { PublicRoute } from './components/public-route';


function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
  <Route
    path="/auth"
    element={
      <PublicRoute>
        <AuthPage />
      </PublicRoute>
    }
  />

  <Route
    path="/"
    element={
      <ProtectedRoute>
        <main className="h-screen bg-background">
          <CallSummarizer />
        </main>
      </ProtectedRoute>
    }
  />

  <Route path="*" element={<Navigate to="/auth" replace />} />
</Routes>
      </Router>
    </AuthProvider>
  )
}

export default App