import React, {useState} from 'react';
import { useNavigate } from 'react-router-dom';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [full_name, setFullName] = useState('');
  const [phone, setPhone] = useState('');

  const navigate = useNavigate();
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const response = await fetch('http://localhost:5000/register', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password, full_name, phone }),
    });
    if (response.ok) {
      navigate('/home');
    } else {
      const error = await response.json();
      alert(`Login failed: ${error.message}`);
    }
  };
      
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
        transform: 'translate(-50%, -150%)',
        zIndex: -1,
          }}
        />
        <h2 style={{ margin: '1rem 0', position: 'relative', zIndex: 1 }}>
          Welcome! Please register to adopt.
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
        placeholder="Full Name"
        name="fullName"
        onChange={(e) => setFullName(e.target.value)}
        required
        style={inputStyle}/>
            <input
        type="tel"
        placeholder="Phone Number (123-456-7890)"
        name="phone"
        onChange={(e) => setPhone(e.target.value)}
        pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"
        required
        style={inputStyle}/>
          <input
        type="email"
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
        Create Account
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

export default Register;
