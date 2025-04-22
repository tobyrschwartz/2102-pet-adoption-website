const Login = () => {
    return (
        <div className="login-container">
        <div className="login-box">
          <img
            src="/images/login-pets.png"
            alt="Cute dogs and cats"
            className="login-image"
          />
          <h2>Login to Adopt</h2>
          <form className="login-form">
            <input type="text" placeholder="Username" name="username" required />
            <input type="password" placeholder="Password" name="password" required />
            <button type="submit">Login</button>
          </form>
        </div>
      </div>
    );
};
export default Login;