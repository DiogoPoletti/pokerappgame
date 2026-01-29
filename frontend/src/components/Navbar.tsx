import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material'
import { useNavigate, useLocation } from 'react-router-dom'
import CasinoIcon from '@mui/icons-material/Casino'
import HomeIcon from '@mui/icons-material/Home'
import SchoolIcon from '@mui/icons-material/School'
import MenuBookIcon from '@mui/icons-material/MenuBook'

function Navbar() {
  const navigate = useNavigate()
  const location = useLocation()

  const navItems = [
    { label: 'Dashboard', path: '/', icon: <HomeIcon /> },
    { label: 'Train', path: '/train', icon: <SchoolIcon /> },
    { label: 'Reference', path: '/reference', icon: <MenuBookIcon /> },
  ]

  return (
    <AppBar position="static" sx={{ bgcolor: 'background.paper' }}>
      <Toolbar>
        <CasinoIcon sx={{ mr: 1, color: 'primary.main' }} />
        <Typography
          variant="h6"
          component="div"
          sx={{ flexGrow: 0, mr: 4, fontWeight: 700 }}
        >
          Poker Trainer
        </Typography>
        
        <Box sx={{ flexGrow: 1, display: 'flex', gap: 1 }}>
          {navItems.map((item) => (
            <Button
              key={item.path}
              color="inherit"
              startIcon={item.icon}
              onClick={() => navigate(item.path)}
              sx={{
                bgcolor: location.pathname === item.path ? 'rgba(76, 175, 80, 0.2)' : 'transparent',
                '&:hover': {
                  bgcolor: 'rgba(76, 175, 80, 0.1)',
                },
              }}
            >
              {item.label}
            </Button>
          ))}
        </Box>
      </Toolbar>
    </AppBar>
  )
}

export default Navbar
