const Login = () => {
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
        placeholder="Username"
        name="username"
        required
        style={inputStyle}
          />
          <input
        type="password"
        placeholder="Password"
        name="password"
        required
        style={inputStyle}
          />
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
