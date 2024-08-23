const express = require('express');
const cors = require('cors');
const app = express();
const port = 3001;

app.use(cors());
app.use(express.json());

let peopleIn = 0;
let peopleOut = 0;
let peopleInside = 0;

app.get('/api/status', (req, res) => {
    res.json({ peopleIn, peopleOut, peopleInside });
});

app.post('/api/update', (req, res) => {
    const { peopleIn: inCount, peopleOut: outCount, peopleInside: insideCount } = req.body;
    peopleIn = inCount;
    peopleOut = outCount;
    peopleInside = insideCount;
    res.status(200).send('Data updated');
});

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
