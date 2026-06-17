import {
  createContext, useCallback, useContext, useEffect, useRef, type ReactNode,
} from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { App } from '@capacitor/app';
import { Capacitor } from '@capacitor/core';

type BackHandler = () => boolean;

interface BackNavigationContextValue {
  registerBackHandler: (handler: BackHandler | null) => void;
  goBack: () => void;
}

const BackNavigationContext = createContext<BackNavigationContextValue | null>(null);

const ROOT_TABS = new Set(['/', '/reels', '/reporter', '/search', '/profile', '/admin', '/track']);

export function BackNavigationProvider({ children }: { children: ReactNode }) {
  const navigate = useNavigate();
  const location = useLocation();
  const pageHandler = useRef<BackHandler | null>(null);
  const lastBackAt = useRef(0);

  const registerBackHandler = useCallback((handler: BackHandler | null) => {
    pageHandler.current = handler;
  }, []);

  const goBack = useCallback(() => {
    if (pageHandler.current?.()) return;

    const idx = window.history.state?.idx ?? 0;
    if (idx > 0) {
      navigate(-1);
      return;
    }

    if (location.pathname !== '/') {
      navigate('/');
      return;
    }

    if (Capacitor.isNativePlatform()) {
      const now = Date.now();
      if (now - lastBackAt.current < 2000) {
        void App.exitApp();
      } else {
        lastBackAt.current = now;
      }
    }
  }, [location.pathname, navigate]);

  useEffect(() => {
    if (!Capacitor.isNativePlatform()) return;

    const sub = App.addListener('backButton', () => {
      goBack();
    });

    return () => {
      void sub.then(l => l.remove());
    };
  }, [goBack]);

  return (
    <BackNavigationContext.Provider value={{ registerBackHandler, goBack }}>
      {children}
    </BackNavigationContext.Provider>
  );
}

export function useBackNavigation() {
  const ctx = useContext(BackNavigationContext);
  if (!ctx) throw new Error('useBackNavigation must be used within BackNavigationProvider');
  return ctx;
}

/** Register a page-level back action (e.g. previous reel). Return true if handled. */
export function usePageBackHandler(handler: BackHandler, deps: unknown[]) {
  const { registerBackHandler } = useBackNavigation();

  useEffect(() => {
    registerBackHandler(handler);
    return () => registerBackHandler(null);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
}

export function isRootTab(pathname: string) {
  return ROOT_TABS.has(pathname);
}
