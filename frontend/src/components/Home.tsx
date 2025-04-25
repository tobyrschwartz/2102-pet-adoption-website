import { Link } from "react-router-dom";
import ItemList from './ItemList';

const Home = () => {
    return (
        
        <div style={{ textAlign: "center", padding: "20px" }}>
            <div style={{ position: "absolute", top: "10px", right: "10px" }}>
            <button
            onClick={() => {
                const profileContainer = document.getElementById('profile-container');
                if (profileContainer) {
                    if (profileContainer.innerHTML.trim() !== "") {
                        profileContainer.innerHTML = ""; // Clear the profile if already displayed
                    } else {
                        const userId = localStorage.getItem('userId');
                        const full_name = localStorage.getItem('full_name');
                        const role = localStorage.getItem('role');
                        if (userId && full_name && role) {
                            profileContainer.innerHTML = `
                                <div>
                                    <p><strong>Name:</strong> ${full_name}</p>
                                    <p><strong>Role:</strong> ${role}</p>
                                </div>
                            `;
                        } else {
                            profileContainer.innerHTML = `
                                <div>
                                    <p><strong>Name:</strong> Guest</p>
                                    <p><strong>Role:</strong> Guest</p>
                                </div>
                            `;
                        }
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
            <h1>Welcome to Pet Adoption</h1>
            <p>Your journey to finding a new friend starts here.</p>
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

            <hr style={{marginTop: '30px', marginBottom: '20px'}} />
            <div style={{ textAlign: 'center' }}> 
                <h2>Data from Backend (Steel Thread Example):</h2>
                <ItemList />
            </div>

        </div>
        
        
        
    );
};

export default Home;