import { Routes, Route, useLocation } from 'react-router-dom';
import { useEffect } from 'react'
import { UserProvider } from './context/UserContext'
import Home from './components/Home'
import Login from './components/Login'
import Navbar from './components/Navbar'
import Register from './components/Register'
import Dashboard from './components/AdminDashboard'
import Unauthorized from './components/Unauthorized'
import Logout from './components/Logout'
import './App.css'
import PetsList from './components/Pets'
import AdminApplications from './components/AdminApplications'
import AdminManagePets from './components/AdminManagePets'
import Questionnaire from './components/Questionnaire'
import ConfirmPet from './components/ConfirmPet'
import StaffReviewQuestionnaires from './components/StaffReviewQuestionnaires';
import StaffReviewApplications from './components/StaffReviewApplications';



function App() {
  const location = useLocation();

  const scrollAllowedRoutes = ['/admin/applications', '/questionnaire', '/admin/pets'];

  useEffect(() => {
    if (scrollAllowedRoutes.some(path => location.pathname.startsWith(path))) {
      document.body.style.overflowY = 'auto';
    } else {
      document.body.style.overflow = 'hidden';
    }
  }, [location]);
  return (
    <UserProvider>
      <div>
        <Navbar/>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<Home />} />
          <Route path="/login" element = {<Login />} />
          <Route path="/register" element = {<Register />} />
          <Route path="/admin/dashboard" element={<Dashboard/>} />
          <Route path="*" element={<h1>404 Not Found</h1>} />
          <Route path="/unauthorized" element={<Unauthorized />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/pets" element = {<PetsList />} />
          <Route path="/admin/applications" element={<AdminApplications />} />
          <Route path="/admin/pets" element={<AdminManagePets />} />
          <Route path="/questionnaire" element={<Questionnaire />} />
          <Route path="/confirm" element={<ConfirmPet />} />
          <Route path="/staff/review" element={<StaffReviewQuestionnaires />} />
          <Route path="/staff/applications" element={<StaffReviewApplications />} />
        </Routes>
      </div>
    </UserProvider>
  )
}

export default App