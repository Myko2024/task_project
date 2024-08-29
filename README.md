# API Testing with Postman
To test the API endpoints of this project using Postman, follow these instructions for each endpoint. 

Run  `docker-compose up` command and check status `http://localhost:8000`

0. Retrieve Token

Endpoint: POST `/api/auth/token/`

Body (JSON):

`
{
    "username": "username",
    "password": "password"
}
`

1. Create a Thread
Endpoint: POST `/api/threads/`

Description: Create a new thread with exactly two participants.

Headers:

Authorization: Bearer `<your_token>`
Body (JSON):

`
{
    "participants": [1, 2]  // Replace with user IDs
}
`

Expected Response:

201 Created for a new thread.
200 OK if the thread already exists.

2. List Threads
Endpoint: GET `/api/threads/list/`

Description: Retrieve a list of threads where the authenticated user is a participant.

Headers:

Authorization: Bearer `<your_token>`
Expected Response:

200 OK with a list of threads.

3. Delete a Thread
Endpoint: DELETE `/api/threads/delete/<thread_id>/`

Description: Delete a thread. Only participants or admin users can delete a thread.

Headers:

Authorization: Bearer `<your_token>`
URL Parameters:

`thread_id`: The ID of the thread to delete.

Expected Response:

204 No Content if the deletion is successful.
403 Forbidden if the user is not authorized to delete the thread.

4. Create a Message
Endpoint: POST `/api/messages/`

Description: Create a new message in a specified thread.

Headers:

Authorization: Bearer <your_token>
Body (JSON):

`
{
    "text": "Your message text",
    "sender": 1, // Replace with sender ID
    "thread": 1  // Replace with thread ID
}
`

Expected Response:

201 Created if the message is successfully created.

5. List Messages
Endpoint: GET `/api/messages/list/<thread_id>/`

Description: Retrieve a list of messages in a specified thread.

Headers:

Authorization: Bearer `<your_token>`
URL Parameters:

`thread_id`: The ID of the thread whose messages you want to list.

Expected Response:

200 OK with a list of messages.

6. Mark Message as Read
Endpoint: PATCH `/api/messages/read/<message_id>/`

Description: Mark a specific message as read.

Headers:

Authorization: Bearer `<your_token>`
URL Parameters:

`message_id`: The ID of the message to mark as read.
Body (JSON):

Empty
Expected Response:

200 OK with the updated message.

7. Get Unread Messages Count
Endpoint: GET `/api/messages/unread-count/`

Description: Retrieve the count of unread messages for the authenticated user.

Headers:

Authorization: Bearer <your_token>
Expected Response:

200 OK with a JSON object containing the unread message count.
Example Response:

`{
    "unread_count": 5
}`

8. List Users
Endpoint: GET `/api/users/`

Description: Retrieve a list of all users.

Headers:

Authorization: Bearer <your_token>
Expected Response:

200 OK with a list of users.
