import * as React from 'react';
import { ListItem, ListItemText, List, Button} from '@mui/material';
import { getFollowRequests, addFollower, removeFollowRequest } from '../../APIRequests'


export default function FriendRequestList(props) {
  const [friendRequests, setFriendRequests] = React.useState([]);

  const handleAccept = async (foreignAuthorId) => {
    const addFollowerResponse = await addFollower(props.authorId, foreignAuthorId);
    if (addFollowerResponse === 200) {
        console.log("Follow request has been approved")
    }
  };

  const handleDeny = async (foreignAuthorId) => {
    const removeFollowRequestResponse = await removeFollowRequest(props.authorId, foreignAuthorId);
    if (removeFollowRequestResponse === 200) {
      console.log("Follow request has been denied")
    }
  };

  React.useEffect(() => {
    async function loadFriendRequests() {
        const friendRequests = await getFollowRequests(props.authorId);
        setFriendRequests(friendRequests)
    }
    loadFriendRequests();
  });

    return (
        <List>
          {friendRequests.map((listitem, index) => (
            <ListItem key={index}>
              <ListItemText>{listitem.requester}</ListItemText>
                <Button sx={{ m: 1 }} color="success" variant="contained" onClick={() => handleAccept(listitem.requester)}>Accept</Button>
                <Button sx={{ m: 1 }} color="error" variant="contained" onClick={() => handleDeny(listitem.requester)}>Deny</Button>
            </ListItem>
          ))}
        </List>
      );
}