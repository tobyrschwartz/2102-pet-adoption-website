import React, { useEffect, useState } from 'react';
import { useUser } from '../context/UserContext';
import { useNavigate } from 'react-router-dom';

interface Application {
  id: number;
  application_id: number;
  applicantId: number;
  applicantName: string;
  status: string;
  pet_id: number;
  submitted_at: string;
  updated_at?: string;
  reviewed_at?: string;
  reviewer_id?: number;
}

interface Response {
  text: string;
  type: string;
  answer: string;
}
console.log('StaffReviewApplications rendered');

const StaffReviewApplications: React.FC = () => {
  const { user, isLoading } = useUser();

  const navigate = useNavigate();
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedApplicant, setSelectedApplicant] = useState<Application | null>(null);
  const [appDetails, setAppDetails] = useState<Application | null>(null);
  const [responses, setResponses] = useState<Response[]>([]);

    useEffect(() => {

        if (isLoading) {
            console.log('Loading user data...');
            setLoading(true);
            return; // Wait for user loading to finish
        }
        if (!user) {
            console.error('Unauthorized access: User not logged in.');
            setLoading(false);
            navigate('/unauthorized');
            return;
        }

        if (user.role <= 2) {
            console.error('Unauthorized access: User is not staff or admin.');
            setLoading(false);
            navigate('/unauthorized');
            return;
        }

        const fetchApplications = async () => {
            try {
                const res = await fetch('http://localhost:5000/api/applications', {
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                    },
                });
                if (!res.ok) throw new Error('Failed to fetch applications.');
                const data = await res.json();
                setApplications(data);
            } catch (err) {
                setError('Error fetching applications.');
            } finally {
                setLoading(false);
            }
        };

        fetchApplications();
}, [user]);

  const openReviewModal = async (app: Application) => {
    setSelectedApplicant(app);
    setModalOpen(true);
    try {
      const res = await fetch(`http://localhost:5000/api/applications/${app.id}`, {
        credentials: 'include',
      });
      if (!res.ok) throw new Error('Failed to load details');
      const data = await res.json();
      setAppDetails({
        application_id: data.application.application_id,
        pet_id: data.application.pet_id,
        reviewed_at: data.application.reviewed_at,
        reviewer_id: data.application.reviewer_id,
        status: data.application.status,
        submitted_at: data.application.submitted_at,
        updated_at: data.application.updated_at,
        applicantId: data.application.user_id,
        applicantName: app.applicantName,
        id: app.id, // Retaining the original ID
      });
      setResponses(
        data.responses.map((resp: any) => ({
          text: resp.question_text,
          type: 'text',
          answer: resp.answer_text,
        }))
      );
    } catch {
      setAppDetails(null);
      setResponses([]);
    }
  };

  const handleApprove = async (userId: number) => {
    try {
      const res = await fetch(`http://localhost:5000/api/applications/${appDetails?.application_id}`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: 'Approved'}),
      });

      if (!res.ok) throw new Error('Failed to approve application.');

      setApplications(prev => prev.filter(app => app.applicantId !== userId));
      setModalOpen(false);
      alert('Application approved!');
    } catch (err: any) {
      alert(`Error: ${err.message}`);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (

    <div style={{ padding: '2rem' }}>
      <h1 style={{ fontSize: '1.8rem', marginBottom: '1rem' }}>Open Applications</h1>
      {applications.length === 0 ? (
        <p>No applications available.</p>
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
            {applications.map(app => (
              <tr key={app.id}>
                <td>{app.id}</td>
                <td>{app.applicantName}</td>
                <td>{app.status}</td>
                <td>
                  <button style={buttonStyle} onClick={() => openReviewModal(app)}>
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
            <h2 style={{ color: '#000000' }}>
              Application #{appDetails?.application_id} – {selectedApplicant.applicantName}
            </h2>
            {appDetails && (
              <div style={{ color: '#333', fontSize: '0.95rem', marginTop: '1rem' }}>
                <p style={{color: '#000000'}}>
                  <strong>Pet ID:</strong> {appDetails.pet_id}</p>
                <p style={{color: '#000000'}}>
                  <strong>Status:</strong> {appDetails.status}</p>
                <p style={{color: '#000000'}}>
                  <strong>Submitted:</strong> {new Date(appDetails.submitted_at).toLocaleString()}</p>
                {appDetails.reviewed_at && (
                  <p><strong>Reviewed:</strong> {new Date(appDetails.reviewed_at).toLocaleString()}</p>
                )}
              </div>
            )}

            <div style={{ marginTop: '1rem' }}>
              <h3>Questionnaire</h3>
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
  top: 0,
  left: 0,
  right: 0,
  bottom: 0,
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

export default StaffReviewApplications;
