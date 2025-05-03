import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';

const Dashboard: React.FC = () => {
    const { user, isLoading } = useUser();
    const isStaff = user && user.role >= 2; 
    const isAdmin = user && user.role === 3; 
    const navigate = useNavigate();
    const [openQuestionnaires, setOpenQuestionnaires] = useState<number>(0);

    useEffect(() => {
        if (isLoading) return;
        if (!isStaff) {
            navigate('/unauthorized');
        }
        // Fetch the amount of open questionnaires from the backend
        const fetchOpenQuestionnaires = async () => {
            try {
                const response = await fetch('/api/questionnaires/count?status=open');
                const data = await response.json();
                setOpenQuestionnaires(data.count);
            } catch (error) {
                console.error('Error fetching open questionnaires:', error);
            }
        };

        fetchOpenQuestionnaires();
    }, [user, isStaff, navigate]);

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
                        <h2>Pet Management</h2>
                        <button 
                        onClick={() => navigate('/pets')}
                        style={{ marginRight: '10px' }}>View Pets</button>
                        <button
                        onClick={() => navigate('/admin/pets')}>Manage Pets</button>
                    </section>
                    <section>
                        <h2>Questionnaires</h2>
                        <p>There are {openQuestionnaires} open questionnaires.</p>
                        <button
                        onClick={() => navigate('/staff/review')}>
                            Review Questionnaires
                            </button>
                        {isAdmin && (
                            <button
                            onClick={() => navigate('/admin/applications')}
                            style={{ marginLeft: '10px' }}>Manage Questionnaires</button>
                        )}
                    </section>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;