# ♟️ Chess Arena

A full-stack real-time multiplayer chess platform featuring a **custom-built chess engine** implemented entirely from scratch—without using libraries. Built with FastAPI, WebSockets, PostgreSQL, SQLAlchemy, and vanilla HTML, CSS, and JavaScript, the application enables authenticated users to play live chess matches, with persistent accounts and automatically updated player statistics.


## Project Highlights

- ♟️ Custom-built chess engine without using libraries such as `python-chess` or `chess.js`
- ⚡ Real-time multiplayer using WebSockets
- 🔐 Secure JWT authentication
- ☁️ Fully deployed full-stack application
- 📊 Persistent player statistics stored in PostgreSQL


## Features

### ♟️ Custom Chess Engine
- Complete chess logic implemented from scratch
- Legal move validation for every piece
- Check and checkmate detection
- Castling support
- En passant support
- Illegal move prevention
- Turn-based gameplay
- Unicode chess pieces

### 🌐 Multiplayer
- Real-time gameplay using WebSockets
- Room-based matchmaking
- Live board synchronization
- Automatic turn management

### 🔐 Authentication
- JWT-based authentication
- Secure login and registration
- Password hashing
- Protected game sessions

### 📊 Player Statistics
- Persistent user accounts
- Win/Loss/Draw tracking
- Automatic stat updates after every completed game

## Tech Stack

### Backend
- FastAPI
- WebSockets
- SQLAlchemy
- PostgreSQL
- JWT Authentication

### Frontend
- HTML
- CSS
- JavaScript

### Deployment
- Railway (Backend & Database)
- GitHub Pages (Frontend)

## Architecture

- FastAPI serves REST APIs and WebSocket connections.
- PostgreSQL stores user accounts and match statistics.
- SQLAlchemy handles database operations.
- JWT secures authenticated requests and game sessions.
- WebSockets synchronize moves between players in real time.
- The chess engine validates every move before updating the board state.


## Future Improvements

- Player vs Bots
- Threefold repetition
- 50-move draw rule
- Insufficient material detection
- Match history
- PGN export
- Elo rating system
- Spectator mode