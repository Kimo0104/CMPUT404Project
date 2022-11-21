import * as React from 'react';
import { styled, alpha } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import InputBase from '@mui/material/InputBase';
import MenuIcon from '@mui/icons-material/Menu';
import SearchIcon from '@mui/icons-material/Search';
import { useNavigate } from 'react-router-dom';
import { useSearchParams } from 'react-router-dom';
import { QueryContext, ShowSearchContext } from '../home/Home';

const SearchInput = () => {

  const { setShowSearch } = React.useContext(ShowSearchContext);
  const { setQuery } = React.useContext(QueryContext);

  const [searchValue, setSearchValue] = React.useState("");
  const [searchParams, setSearchParams] = useSearchParams();

  const navigate = useNavigate();

  const handleChange = (e) => {
    setSearchValue(e.target.value);
  }

  const handleSubmit = (e) => {
    // Enter is pressed
    e.preventDefault();
    
    setShowSearch(true);
    setQuery([searchValue, 1]);
    localStorage.setItem("showSearch", true);
    localStorage.setItem("query", [searchValue, 1]);
    //navigate(`/search?query=${searchValue}`);
    //navigate(0);
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
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="open drawer"
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ flexGrow: 1, display: { xs: 'none', sm: 'block' } }}
            align = "justify"
          >
            Social Distribution
          </Typography>
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
