import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
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

function App() {
  return (
    <UserProvider>
    <Router>
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
        </Routes>
      </div>
    </Router>
    </UserProvider>
  )
}

export default App
