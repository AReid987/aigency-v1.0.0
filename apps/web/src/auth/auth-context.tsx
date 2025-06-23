import {
 useContext,
 createContext,
 useState,
 useEffect,
} from 'react';
import { useUser } from '@clerk/nextjs';
import { User as UserResource } from '@clerk/nextjs';
import { Clerk } from '@clerk/backend';

interface AuthContextType {
  isSignedIn: boolean;
  user: UserResource | null;
  clerk: any;
}

const AuthContext = createContext<AuthContextType>({
  isSignedIn: false,
  user: null,
  clerk: null,
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
 const { isSignedIn, user, isLoaded } = useUser();
 const [localUser, setLocalUser] = useState<UserResource | null>(null);

 useEffect(() => {
  if (isSignedIn && isLoaded) {
   setLocalUser(user || null);
    } else {
      setLocalUser(null);
    }
  }, [isSignedIn, user, isLoaded]);
const value: AuthContextType = {
const value: AuthContextType = {
const value: AuthContextType = {
isSignedIn: !!localUser,
user: localUser,
clerk: clerk || null,
};


  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);