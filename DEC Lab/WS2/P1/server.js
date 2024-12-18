const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

io.on('connection', (socket) => {
    console.log('A user connected');

    socket.on('set username', (username) => {
      socket.username = username || `User${Math.floor(Math.random() * 1000)}`; // Assign username or default
      console.log(`${socket.username} joined`);
      
      io.emit('chat notification', `${socket.username} joined the chat`);
    });
  
    socket.on('chat message', (msg) => {
      const messageData = {
        username: socket.username || 'Anonymous',
        message: msg,
      };
  
      io.emit('chat message', messageData);
    });
  
    socket.on('disconnect', () => {
      if (socket.username) {
        console.log(`${socket.username} disconnected`);
  
        io.emit('chat notification', `${socket.username} left the chat`);
      }
    });
  });
  

const PORT = process.env.PORT || 8080;
server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
