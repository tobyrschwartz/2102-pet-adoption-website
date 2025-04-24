import React from 'react';

interface ProfileProps {
    userId: string;
    full_name: string;
    role: string;
}

const Profile: React.FC<ProfileProps> = ({ userId, full_name, role }) => {
    return (
        <div>
            <h1>Profile</h1>
            <p><strong>User ID:</strong> {userId}</p>
            <p><strong>Full Name:</strong> {full_name}</p>
            <p><strong>Role:</strong> {role}</p>
        </div>
    );
};

export default Profile;