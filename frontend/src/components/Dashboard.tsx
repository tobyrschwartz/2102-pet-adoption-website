import React from 'react';
import { useNavigate } from 'react-router-dom';

interface User {
    role: number;
}

const mockUser: User = {
    role: 1, // Replace this with actual user role logic
};

const Dashboard: React.FC = () => {
    const navigate = useNavigate();

    // Check if the user has the required role
    if (mockUser.role !== 2) {
        navigate('/unauthorized'); // Redirect to an unauthorized page
        return null;
    }

    return (
        <div
            style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '50vh',
            }}
        >
            <div style={{ padding: '50px', textAlign: 'center' }}>
                <h1>Admin Dashboard</h1>
                <div style={{ marginTop: '20px' }}>
                    <section style={{ marginBottom: '20px' }}>
                        <h2>User Management</h2>
                        <button style={{ marginRight: '10px' }}>View Users</button>
                        <button>Add User</button>
                    </section>
                    <section style={{ marginBottom: '20px' }}>
                        <h2>Pet Management</h2>
                        <button style={{ marginRight: '10px' }}>View Pets</button>
                        <button>Manage Pets</button>
                    </section>
                    <section>
                        <h2>Applications</h2>
                        <button>Review Applications</button>
                    </section>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;