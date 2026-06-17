import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { DemoProvider } from './lib/demo-store';
import { BackNavigationProvider } from './lib/back-navigation';
import { FeedPage } from './pages/FeedPage';
import { ReelsPage } from './pages/ReelsPage';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { ReporterPage } from './pages/ReporterPage';
import { AdminPage } from './pages/AdminPage';
import { TrackPage } from './pages/TrackPage';
import { ProfilePage } from './pages/ProfilePage';
import { PostDetailPage } from './pages/PostDetailPage';
import { SearchPage } from './pages/SearchPage';

export default function App() {
  return (
    <DemoProvider>
      <BrowserRouter>
        <BackNavigationProvider>
          <Routes>
            <Route path="/" element={<FeedPage />} />
            <Route path="/reels" element={<ReelsPage />} />
            <Route path="/reporter" element={<ReporterPage />} />
            <Route path="/admin" element={<AdminPage />} />
            <Route path="/track" element={<TrackPage />} />
            <Route path="/search" element={<SearchPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/post/:id" element={<PostDetailPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BackNavigationProvider>
      </BrowserRouter>
    </DemoProvider>
  );
}
