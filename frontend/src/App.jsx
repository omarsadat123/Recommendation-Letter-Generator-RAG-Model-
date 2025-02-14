import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import FileUpload from './FileUpload'
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Emni from './Emni'

function App() {
  const [count, setCount] = useState(0)

  return (
    <Router>
      <Routes>
        <Route path="/" element={<FileUpload />} />
        <Route path="/try" element={<Emni/>} />
      </Routes>
    </Router>
  )
}

export default App
