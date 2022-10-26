import * as React from 'react';
import Button from '@mui/material/Button';

import { checkFollowStatus } from '../../APIRequests'

const handleClick = () => {
    // Do Something
  };

export default function Follow(props) {
  const [following, setFollowing] = React.useState(-1);

    React.useEffect(() => {
        async function loadAuthor() {
            const following = await checkFollowStatus("2", "1");
            console.log(following)
            setFollowing(following)
        }
        loadAuthor();
      });
      
    return (
        <div>
            {
                following !== 2 && (
                (following === 0) ? <Button size="large" onClick={handleClick}>Request to follow </Button> :
                <Button size="large" onClick={handleClick}>Follow Request has been sent</Button>)
            }
           

        </div>
    )
}