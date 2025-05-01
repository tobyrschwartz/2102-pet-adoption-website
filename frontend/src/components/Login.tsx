import React, {useState, useEffect} from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';

const Login = () => {
  const { setUser } = useUser();
  const { user } = useUser();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const response = await fetch('http://localhost:5000/login', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ email, password }),
    });
    if (response.ok) {
      const data = await response.json();
      setUser({
        full_name: data.full_name,
        email: data.email,
        role: data.role,
        approved: data.approved,
      });
      navigate(data.redirect_url || '/');
    } else {
      const error = await response.json();
      alert(`Login failed: ${error.error}`);
    }
  };

  useEffect(() => {
    if (user) {
      navigate('/');
    }
  }, [user]);
      
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        width: '100vw',
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          width: '100%',
          maxWidth: '400px',
          padding: '1rem',
          boxSizing: 'border-box',
          textAlign: 'center',
          position: 'relative',
        }}
      >
        <img
          src="/images/login_page.png"
          alt="Cute dogs and cats"
          style={{
        width: '200%',
        maxWidth: '1000px',
        height: 'auto',
        borderRadius: '8px',
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -125%)',
        zIndex: -1,
          }}
        />
        <h2 style={{ margin: '1rem 0', position: 'relative', zIndex: 1 }}>
          Login to Adopt
        </h2>
        <form
        onSubmit={handleSubmit}
          style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem',
        alignItems: 'center',
        position: 'relative',
        zIndex: 1,
          }}
        >
          <input
        type="text"
        placeholder="Email"
        name="email"
        onChange={(e) => setEmail(e.target.value)}
        required
        style={inputStyle}/>
          <input
        type="password"
        placeholder="Password"
        name="password"
        onChange={(e) => setPassword(e.target.value)}
        required
        style={inputStyle}/>
          <button type="submit" style={buttonStyle}>
        Login
          </button>
        </form>
      </div>
    </div>
  );
};

const inputStyle: React.CSSProperties = {
  padding: '0.75rem',
  borderRadius: '8px',
  border: '1px solid #ccc',
  fontSize: '1rem',
  width: '100%',
  maxWidth: '300px',
  boxSizing: 'border-box',
};

const buttonStyle: React.CSSProperties = {
  ...inputStyle,
  backgroundColor: '#007BFF',
  color: 'white',
  border: 'none',
  cursor: 'pointer',
};

export default Login;
