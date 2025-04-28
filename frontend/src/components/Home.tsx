import { Link } from "react-router-dom";
import { useUser, roleToText } from "../context/UserContext"; // or whatever your path is

const Home = () => {
    const { user } = useUser();
    return (
        <div style={{ textAlign: "center", padding: "20px" }}>
            {user && (<div style={{ position: "absolute", top: "10px", right: "10px" }}>
                <button
                onClick={() => {
                    const profileContainer = document.getElementById('profile-container');
                    if (profileContainer) {
                        if (profileContainer.innerHTML.trim() !== "") {
                            profileContainer.innerHTML = ""; // Clear the profile if already displayed
                        } else {
                            profileContainer.innerHTML = `
                                <div>
                                    <p><strong>Name:</strong> ${user.full_name}</p>
                                    <p><strong>Role:</strong> ${roleToText[user.role]}</p>
                                </div>
                            `;
                        }
                    }
                }}
                style={{ 
                borderRadius: "20px", 
                padding: "10px 15px", 
                backgroundColor: "#28A745", 
                color: "white", 
                border: "none", 
                cursor: "pointer" 
                }}>
                My Profile
                </button>
            <div id="profile-container" style={{ textAlign: "right", marginTop: "10px" }}></div>
            </div>
            )}
            <h1>Welcome to Pet Adoption</h1>
            <p>Your journey to finding a new friend starts here.</p>
            {!user ? (
                <Link to="/login" style={{ textDecoration: "none" }}>
                    <button style={{ 
                        borderRadius: "20px", 
                        padding: "10px 20px", 
                        backgroundColor: "#007BFF", 
                        color: "white", 
                        border: "none", 
                        cursor: "pointer" 
                    }}>
                        Login
                    </button>
                </Link>
            ) : (
                <Link to="/pets" style={{ textDecoration: "none" }}>
                    <button style={{ 
                        borderRadius: "20px", 
                        padding: "10px 20px", 
                        backgroundColor: "#007BFF", 
                        color: "white", 
                        border: "none", 
                        cursor: "pointer" 
                    }}>
                        See Available Pets
                    </button>
                </Link>
            )}

        </div>
        
        
        
    );
};

export default Home;