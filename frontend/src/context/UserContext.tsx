import { createContext, useContext, useEffect, useState } from "react";

export enum Role {
    USER = 1,
    STAFF = 2,
    ADMIN = 3,
}

export const roleToText: Record<Role, string> = {
    [Role.USER]: "User",
    [Role.STAFF]: "Staff",
    [Role.ADMIN]: "Admin",
};

type User = {
    full_name: string;
    email: string;
    role: Role;
    approved?: boolean;
};

interface UserContextType {
    user: User | null;
    setUser: (user: User | null) => void;
    isLoading: boolean; // Add isLoading state
}

const UserContext = createContext<UserContextType>({
    user: null,
    setUser: () => {},
    isLoading: true, // Initially loading
});

export const UserProvider = ({ children }: { children: React.ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const res = await fetch("http://localhost:5000/api/me", {
                    credentials: "include",
                });
                const data = await res.json();

                if (data.logged_in) {
                    const { email, full_name, role, approved } = data;
                    setUser({ full_name, email, role: role as Role, approved });
                } else {
                    setUser(null); // Ensure user is null if not logged in
                }
            } catch (err) {
                console.error("Failed to fetch user:", err);
                setUser(null); // Handle errors by setting user to null
            } finally {
                setIsLoading(false); // Set loading to false regardless of outcome
            }
        };

        fetchUser();
    }, []);

    const value: UserContextType = {
        user,
        setUser,
        isLoading,
    };

    return (
        <UserContext.Provider value={value}>
            {children}
        </UserContext.Provider>
    );
};

export const useUser = () => useContext(UserContext);