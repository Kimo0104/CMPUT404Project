import React from 'react'
import Inbox from '../stream/Inbox'

export default function Home() {
  return (
    <div>
      Home
      <Inbox authorId={2}/>
    </div>
  )
}
