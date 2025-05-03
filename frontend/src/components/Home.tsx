import { Link } from "react-router-dom";
import { useUser, roleToText } from "../context/UserContext";
import './Home.css';

const Home = () => {
    const { user } = useUser();

    const handleProfileToggle = () => {
        const profileContainer = document.getElementById('profile-container');
        if (user && profileContainer) {
            if (profileContainer.innerHTML.trim() !== "") {
                profileContainer.innerHTML = "";
            } else {
                profileContainer.innerHTML = `
                    <div>
                        <p><strong>Name:</strong> ${user.full_name}</p>
                        <p><strong>Role:</strong> ${roleToText[user.role]}</p>
                        <p><strong>Approval Status:</strong> ${user.approved ? "Approved" : "Not Approved"}</p>
                    </div>
                `;
            }
        }
    };

    return (
        <div className="home-container">
            {user && (
                <div className="profile-toggle">
                    <button className="profile-btn" onClick={handleProfileToggle}>
                        My Profile
                    </button>
                    <div id="profile-container" className="profile-container"></div>
                </div>
            )}
            <div className="home-content">
                <h1>Welcome to Pet Adoption</h1>
                <p>Your journey to finding a new friend starts here.</p>
                {user && !user.approved && (
                    <p className="approval-warning">
                        Your account has not been approved for adoption yet.
                    </p>
                )}
                {!user ? (
                    <Link to="/login" className="home-link">
                        <button className="home-button">Login</button>
                    </Link>
                ) : (
                    <Link to="/pets" className="home-link">
                        <button className="home-button">See Available Pets</button>
                    </Link>
                )}
            </div>
        </div>
    );
};

export default Home;
