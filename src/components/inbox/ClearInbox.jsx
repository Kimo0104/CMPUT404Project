import React from "react";
import Button from '@mui/material/Button';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import { deleteInbox } from '../../APIRequests';
export default function ClearInbox(props) {
    // props contains authorId, setInbox
    const [debounce, setDebounce] = React.useState((new Date()).getTime());

    const handleClick = () => {
        const nowTimeMilli = (new Date()).getTime()
        if (nowTimeMilli < debounce + 500) { return; }
        setDebounce(nowTimeMilli);
        deleteInbox(props.authorId);
        props.setInbox([]);
    };
    
    return (
        <Button size="large" variant="contained" onClick={handleClick} endIcon={<DeleteOutlineIcon />}>
            Clear Inbox
        </Button>
    )
}
