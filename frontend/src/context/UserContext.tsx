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
const UserContext = createContext<{
    user: User | null;
    setUser: (user: User | null) => void;
}>({
    user: null,
    setUser: () => {},
});

export const UserProvider = ({ children }: { children: React.ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);

    // Fetch user info once on load
    useEffect(() => {
        fetch("http://localhost:5000/api/me", {
        credentials: "include",
        })
        .then((res) => res.json())
        .then((data) => {
            if (data.logged_in) {
                const { email, full_name, role, approved} = data;
                setUser({ full_name, email , role: role as Role, approved});
              }
        })
        .catch((err) => console.error("Failed to fetch user:", err));
    }, []);

    return (
        <UserContext.Provider value={{ user, setUser }}>
        {children}
        </UserContext.Provider>
    );
};

export const useUser = () => useContext(UserContext);