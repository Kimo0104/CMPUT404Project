import * as React from 'react';
import Button from '@mui/material/Button';

import { checkFollowStatus, requestToFollow, removeFollower } from '../../APIRequests'

export default function Follow(props) {
    const [following, setFollowing] = React.useState(-1);
    
    const handleRequestToFollow = async () => {
        // Request to follow another user
        const reqToFollow = await requestToFollow(props.authorId, props.foreignAuthorId);
        if (reqToFollow === 200) {
            setFollowing(1)
        }
    };
    
    const unfollow = async () => {
        // Unfollow another user
        const reqToUnfollow = await removeFollower(props.authorId, props.foreignAuthorId);
        if (reqToUnfollow === 200) {
            setFollowing(0)
        }
    };
    
    React.useEffect(() => {
        async function loadAuthor() {
            const following = await checkFollowStatus(props.authorId, props.foreignAuthorId);
            setFollowing(following)
        }
        loadAuthor();
      });

      const requestToFollowButton = <Button size="large" onClick={handleRequestToFollow}>Request to follow</Button> 
      const followRequestHasBeenSentButton = <Button size="large">Follow Request has been sent</Button> 
      const unfollowButton = <Button size="large" onClick={unfollow}>Unfollow</Button> 
      
    return (
        <div>

            {
                following === 0 && requestToFollowButton
            }

            {
                following === 1 && followRequestHasBeenSentButton
            }

            {
                following === 2 && unfollowButton
            }
           
        </div>
    )
}