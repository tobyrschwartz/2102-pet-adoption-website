import React, { useEffect, useState } from 'react';
import { useUser } from '../context/UserContext';
import { useNavigate } from 'react-router-dom';
interface Questionnaire {
  id: number;
  applicantId: number;
  applicantName: string;
  status: string;
}

interface Response {
    id: number;
    text: string;
    type: string;
    answer: string;
  }

const StaffReviewQuestionnaires: React.FC = () => {
    const { user, isLoading } = useUser();
    const navigate = useNavigate();
    const [questionnaires, setQuestionnaires] = useState<Questionnaire[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedApplicant, setSelectedApplicant] = useState<Questionnaire | null>(null);
    const [responses, setResponses] = useState<Response[]>([]);
    const [modalOpen, setModalOpen] = useState(false);

    useEffect(() => {
        if (isLoading) return;
        if (!user || user.role <= 2) {
            setLoading(false);
            navigate('/unauthorized');
            return;
    }
    const fetchQuestionnaires = async () => {
        try {
        const response = await fetch('http://localhost:5000/api/questionnaires/review', {
            method: 'GET',
            credentials: 'include',
        });

        if (!response.ok) throw new Error('Failed to fetch questionnaires.');

        const data = await response.json();
        setQuestionnaires(data);
        } catch (err) {
        setError('Failed to fetch questionnaires.');
        } finally {
        setLoading(false);
        }
    };

    fetchQuestionnaires();
    }, []);

    const openReviewModal = async (app: Questionnaire) => {
    setSelectedApplicant(app);
    setModalOpen(true);

    try {
        const res = await fetch(`http://localhost:5000/api/questionnaires/${app.applicantId}`, {
        method: 'GET',
        credentials: 'include',
        });

        if (!res.ok) throw new Error('Failed to load responses.');

        const data = await res.json();
        setResponses(data);
    } catch (err) {
        setResponses([]);
    }
    };

    const handleApprove = async (userId: number) => {
    try {
        const res = await fetch(`http://localhost:5000/api/users/${userId}/approve`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        },
        });

        if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || 'Approval failed');
        }

        setQuestionnaires((prev) => prev.filter((q) => q.applicantId !== userId));
        setModalOpen(false);
        alert('Applicant approved!');
    } catch (error: any) {
        alert(`Error: ${error.message}`);
    }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
    <div style={{ padding: '2rem' }}>
        <h1 style={{ fontSize: '1.8rem', marginBottom: '1rem' }}>Open Applications</h1>

        {questionnaires.length === 0 ? (
        <p>No open questionnaires available.</p>
        ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
            <tr>
                <th style={thStyle}>ID</th>
                <th style={thStyle}>Applicant Name</th>
                <th style={thStyle}>Status</th>
                <th style={thStyle}>Action</th>
            </tr>
            </thead>
            <tbody>
            {questionnaires.map((q) => (
                <tr key={q.id}>
                <td>{q.id}</td>
                <td>{q.applicantName}</td>
                <td>{q.status}</td>
                <td style={{ display: 'flex', gap: '0.5rem' }}>
                    <button style={buttonStyle} onClick={() => openReviewModal(q)}>
                    Review
                    </button>
                </td>
                </tr>
            ))}
            </tbody>
        </table>
        )}

        {/* Modal */}
        {modalOpen && selectedApplicant && (
        <div style={modalOverlay}>
            <div style={modalStyle}>
            <h2 style={{color: '#000000'}}>Review: {selectedApplicant.applicantName}</h2>
            <div style={{ marginTop: '1rem' }}>
                {responses.length === 0 ? (
                <p>No responses available.</p>
                ) : (
                <ul>
                    {responses.map((resp, i) => (
                    <li key={i} style={{ marginBottom: '0.5rem' }}>
                        <p style={{ fontWeight: 'bold', marginBottom: '0.25rem', color: '#000000' }}>{resp.text}</p>
                        <p style={{ marginLeft: '1rem', color: '#333' }}>{resp.answer}</p>
                    </li>
                    ))}
                </ul>
                )}
            </div>
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1.5rem', gap: '1rem' }}>
                <button
                style={{ ...buttonStyle, backgroundColor: '#28a745' }}
                onClick={() => handleApprove(selectedApplicant.applicantId)}
                >
                Approve
                </button>
                <button
                style={{ ...buttonStyle, backgroundColor: '#ccc', color: 'black' }}
                onClick={() => setModalOpen(false)}
                >
                Cancel
                </button>
            </div>
            </div>
        </div>
        )}
    </div>
    );
    };

const thStyle: React.CSSProperties = {
  textAlign: 'left',
  borderBottom: '1px solid #ccc',
  paddingBottom: '0.5rem',
};

const buttonStyle: React.CSSProperties = {
  backgroundColor: '#007BFF',
  color: 'white',
  padding: '0.4rem 0.8rem',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
};

const modalOverlay: React.CSSProperties = {
  position: 'fixed',
  top: 0, left: 0, right: 0, bottom: 0,
  backgroundColor: 'rgba(0, 0, 0, 0.6)',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  zIndex: 1000,
};

const modalStyle: React.CSSProperties = {
  backgroundColor: 'white',
  padding: '2rem',
  borderRadius: '8px',
  width: '500px',
  maxHeight: '80vh',
  overflowY: 'auto',
};

export default StaffReviewQuestionnaires;