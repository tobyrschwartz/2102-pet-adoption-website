import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './components/Home'
import Login from './components/Login'
import Navbar from './components/Navbar'
import Register from './components/Register'
import Dashboard from './components/Dashboard'
import Unauthorized from './components/Unauthorized'
import './App.css'
import PetsList from './components/Pets'

function App() {
  return (
    <Router>
      <div>
        <Navbar/>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<Home />} />
          <Route path="/login" element = {<Login />} />
          <Route path="/register" element = {<Register />} />
          <Route path="/dashboard" element={<Dashboard/>} />
          <Route path="*" element={<h1>404 Not Found</h1>} />
          <Route path="/unauthorized" element={<Unauthorized />} />
          <Route path="/pets" element = {<PetsList />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
