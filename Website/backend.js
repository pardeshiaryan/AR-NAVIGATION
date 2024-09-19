const express = require('express');
const session = require('express-session');
const mysql = require('mysql2');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();

app.use(cors({
    origin: ['http://localhost:3000', 'http://127.0.0.1:3000', 'http://127.0.0.1:3001'],
    credentials: true // Allow cookies to be sent across different origins
}));


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.use(session({
    secret: 'yourSecretKey',
    resave: false,
    saveUninitialized: true,
    cookie: { maxAge: 86400000 } // 1 day
}));

const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'K@rtik2004',
    database: 'arcredentials'
});

db.connect(err => {
    if (err) throw err;
    console.log('Connected to SQL database');
});

app.post('/login', (req, res) => {
    const { MoodleId, Password } = req.body;

    const query = 'SELECT * FROM users WHERE MoodleId = ? AND Password = SHA2(?, 256)';
    db.query(query, [MoodleId, Password], (err, result) => {
        if (err) {
            console.error('Database query error:', err);
            return res.json({ success: false, message: 'Internal server error' });
        }
        if (result.length > 0) {
            const user = result[0];
            req.session.authenticated = true;
            req.session.user = user;
            req.session.save(err => { // Ensure session is saved
                if (err) {
                    console.error('Session save error:', err);
                    return res.json({ success: false, message: 'Session save error' });
                }
                console.log('Session data after login:', req.session);
                res.json({ success: true, message: 'Login successful' });
            });
        } else {
            res.json({ success: false, message: 'Invalid Moodle Id or Password' });
        }
    });
});

app.get('/check-auth', (req, res) => {
    if (req.session.authenticated) {
        return res.json({ isAuthenticated: true, user: req.session.user });
    } else {
        return res.json({ isAuthenticated: false });
    }
});


app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});
