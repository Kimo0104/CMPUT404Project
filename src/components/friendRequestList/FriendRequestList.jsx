import * as React from 'react';
import { ListItem, ListItemText, List, Button, Typography} from '@mui/material';
import { getFollowRequests, addFollower, removeFollowRequest, getAuthor } from '../../APIRequests'
import { useNavigate } from 'react-router-dom';
import { userIdContext } from '../../App';


export default function FriendRequestList(props) {
  const userId = React.useContext(userIdContext);

  const [friendRequests, setFriendRequests] = React.useState([]);

  const navigate = useNavigate();

  const handleAccept = async (foreignAuthorId) => {
    const addFollowerResponse = await addFollower(userId, foreignAuthorId);
    if (addFollowerResponse === 200) {
        console.log("Follow request has been approved")
    }
    navigate(0);
  };

  const handleDeny = async (foreignAuthorId) => {
    const removeFollowRequestResponse = await removeFollowRequest(userId, foreignAuthorId);
    if (removeFollowRequestResponse === 200) {
      console.log("Follow request has been denied")
    }
    navigate(0);
  };

  const loadFriendRequests = async () => {
    const friendRequests = await getFollowRequests(userId);
    
    for (let listitem of friendRequests) {
      const author = await getAuthor(listitem.requester)
      listitem.displayName = author.displayName
    }
    setFriendRequests(friendRequests)
  }
  

  React.useEffect(() => {
    loadFriendRequests();
  }, []);

    return (
      <>
        <Typography sx={{ mt: 5 }} variant="h6" component="div">
          Friend Request List:
        </Typography>
        <List>
          {friendRequests.map((listitem, index) => (
            <ListItem key={index} divider={true}>
              <ListItemText  primaryTypographyProps={{ style: { "font-weight": "bold"}  }}>{listitem.displayName}</ListItemText>
                <Button sx={{ m: 1 }} color="success" variant="contained" onClick={() => handleAccept(listitem.requester)}>Accept</Button>
                <Button sx={{ m: 1 }} color="error" variant="contained" onClick={() => handleDeny(listitem.requester)}>Deny</Button>
            </ListItem>
          ))}
        </List>
      </>
      );
}