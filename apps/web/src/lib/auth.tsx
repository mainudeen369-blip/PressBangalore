import { useDemo } from './demo-store';

export function useAuth() {
  const demo = useDemo();
  return {
    user: demo.currentUser,
    loading: demo.loading,
    login: demo.login,
    logout: demo.logout,
    refreshUser: async () => {},
    setUser: () => {},
  };
}
