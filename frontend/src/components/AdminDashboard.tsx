import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';

const Dashboard: React.FC = () => {
    const { user } = useUser();
    const isStaff = user && user.role >= 2; 
    const isAdmin = user && user.role === 3; 
    const navigate = useNavigate();
    const [openApplications, setOpenApplications] = useState<number>(0);

    useEffect(() => {

        if (!isStaff) {
            navigate('/unauthorized');
        }
        // Fetch the amount of open applications from the backend
        const fetchOpenApplications = async () => {
            try {
                const response = await fetch('/api/applications/count?status=open');
                const data = await response.json();
                setOpenApplications(data.count);
            } catch (error) {
                console.error('Error fetching open applications:', error);
            }
        };

        fetchOpenApplications();
    }, [user, isStaff]);

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
                        <button 
                        onClick={() => navigate('/admin/users')}
                        style={{ marginRight: '10px' }}>View Users</button>
                        {isAdmin && <button>Add User</button>}
                    </section>
                    <section style={{ marginBottom: '20px' }}>
                        <h2>Pet Management</h2>
                        <button 
                        onClick={() => navigate('/pets')}
                        style={{ marginRight: '10px' }}>View Pets</button>
                        <button
                        onClick={() => navigate('/admin/pets')}>Manage Pets</button>
                    </section>
                    <section>
                        <h2>Applications</h2>
                        <p>There are {openApplications} open applications.</p>
                        <button
                        onClick={() => navigate('/staff/review')}>
                            Review Applications
                            </button>
                        {isAdmin && (
                            <button
                            onClick={() => navigate('/admin/applications')}
                            style={{ marginLeft: '10px' }}>Manage Applications</button>
                        )}
                    </section>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;