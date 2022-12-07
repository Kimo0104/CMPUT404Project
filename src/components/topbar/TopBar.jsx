import * as React from 'react';
import { styled, alpha } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import InputBase from '@mui/material/InputBase';
import SearchIcon from '@mui/icons-material/Search';
import { QueryContext, ShowSearchContext } from '../home/Home';
import { Navigate, useNavigate } from 'react-router-dom';
import { Button } from '@mui/material';

const SearchInput = () => {

  const { setShowSearch } = React.useContext(ShowSearchContext);
  const { setQuery } = React.useContext(QueryContext);

  const navigate = useNavigate();

  const [searchValue, setSearchValue] = React.useState("");

  const handleChange = (e) => {
    setSearchValue(e.target.value);
  }

  const handleSubmit = (e) => {
    // Enter is pressed
    e.preventDefault();
    

    setShowSearch("true");
    setQuery([searchValue, 1]);
    localStorage.setItem("showSearch", "true");
    localStorage.setItem("query", [searchValue, 1]);
    //navigate(`/search?query=${searchValue}`);
    if (window.location.href.split("/")[-1] == "manage") {
      navigate("/home");
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <StyledInputBase 
        onChange={handleChange}
        placeholder="Search Users"
        inputProps={{ 'aria-label': 'search' }}
      />
    </form>
  );

}

const Search = styled("div")(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha(theme.palette.common.white, 0.15),
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.white, 0.25),
  },
  marginLeft: 0,
  width: '100%',
  [theme.breakpoints.up('sm')]: {
    marginLeft: theme.spacing(1),
    width: 'auto',
  },
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    // vertical padding + font size from searchIcon
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create('width'),
    width: '100%',
    [theme.breakpoints.up('sm')]: {
      width: '12ch',
      '&:focus': {
        width: '20ch',
      },
    },
  },
  
}));

export default function SearchAppBar() {
  let navigate = useNavigate();

  function handleLogout() {
    localStorage.clear();
    navigate("/");
  }
  
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ flexGrow: 1, display: { xs: 'none', sm: 'block' }, cursor:'pointer' }}
            align = "justify"
            onClick={()=> {
              navigate("/home");
              navigate(0);
            }}
          >
            Social Distribution
          </Typography>
          <Button variant="contained" onClick={handleLogout}>Logout</Button>
          <Search>
            <SearchIconWrapper>
              <SearchIcon />
            </SearchIconWrapper>
            <SearchInput/>
          </Search>
        </Toolbar>
      </AppBar>
    </Box>
  );
}
