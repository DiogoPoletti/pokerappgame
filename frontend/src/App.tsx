import { Routes, Route } from 'react-router-dom'
import { Box, Container } from '@mui/material'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Training from './pages/Training'
import Reference from './pages/Reference'

function App() {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      <Container maxWidth="lg" sx={{ flex: 1, py: 4 }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/train/:type?" element={<Training />} />
          <Route path="/reference" element={<Reference />} />
        </Routes>
      </Container>
    </Box>
  )
}

export default App
