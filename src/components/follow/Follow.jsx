import Button from '@mui/material/Button';

const handleClick = () => {
    // Do Something
  };

export default function Follow() {
    return (
        <div>
            <Button size="large" onClick={handleClick}>
                Follow
            </Button>
        </div>
    )
}