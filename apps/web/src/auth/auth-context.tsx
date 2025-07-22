import React, {
 useContext,
 createContext,
 useState,
 useEffect,
} from 'react';
import { useUser } from '@clerk/nextjs';
import { UserResource } from '@clerk/types';

interface AuthContextType {
  isSignedIn: boolean;
  user: UserResource | null;
}

const AuthContext = createContext<AuthContextType>({
  isSignedIn: false,
  user: null,
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
isSignedIn: !!localUser,
user: localUser,
};


  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);