import { Stack } from "@mui/system";
import ListItem from "./ListItem";

const SearchList = ({ filteredAuthors }) => {
    const filteredListItems = filteredAuthors.map( author => <ListItem key={author.id} author={author}/> );
  
    return (
      <Stack spacing={3}>
        {filteredListItems}
      </Stack>
    );
  
  }

export default SearchList;