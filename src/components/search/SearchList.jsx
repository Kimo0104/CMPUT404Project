import { Stack } from "@mui/system";
import ListItem from "./ListItem";

const SearchList = ({ filteredAuthors }) => {
    var key = 0;
    const filteredListItems = filteredAuthors.map( author => <ListItem key={key++} author={author}/> );
  
    return (
      <Stack spacing={3}>
        {filteredListItems}
      </Stack>
    );
  
  }

export default SearchList;