const Login = () => {
  return (
    <div
      className="login-container"
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
      }}
    >
      <div
        className="login-box"
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
        }}
      >
        <img
          src="/images/login_page.png"
          alt="Cute dogs and cats"
          className="login-image"
          style={{
        width: '150%',
        height: '150%',
        backdropFilter: 'blur(15px)',
        borderRadius: '8px',
          }}
        />
        <h2>Login to Adopt</h2>
        <form
          className="login-form"
          style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem',
        alignItems: 'center',
          }}
        >
          <input
        type="text"
        placeholder="Username"
        name="username"
        required
        style={{
          padding: '0.75rem',
          borderRadius: '8px',
          border: '1px solid #ccc',
          fontSize: '1rem',
          width: '100%',
          maxWidth: '300px',
        }}
          />
          <input
        type="password"
        placeholder="Password"
        name="password"
        required
        style={{
          padding: '0.75rem',
          borderRadius: '8px',
          border: '1px solid #ccc',
          fontSize: '1rem',
          width: '100%',
          maxWidth: '300px',
        }}
          />
          <button
        type="submit"
        style={{
          padding: '0.75rem',
          borderRadius: '8px',
          border: 'none',
          backgroundColor: '#007BFF',
          color: 'white',
          fontSize: '1rem',
          cursor: 'pointer',
          width: '100%',
          maxWidth: '300px',
        }}
          >
        Login
          </button>
        </form>
      </div>
    </div>
  );
};
export default Login;