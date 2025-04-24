import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './components/Home'
import Login from './components/Login'
import Navbar from './components/Navbar'
import Register from './components/Register'
import './App.css'

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
        </Routes>
      </div>
    </Router>
  )
}

export default App
