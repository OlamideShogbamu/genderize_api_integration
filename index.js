const express = require('express');

const app = express();

//Add CORS headers to responses
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    next();
});

app.get('/api/classify', async (req, res) => {
    const nameRaw = req.query.name;
    const name = nameRaw.trim();
    
    //input validation
    if (name == undefined || name == null || name == '') {
        return res.status(400).json({status: 'error', message: 'Missing or empty name parameter'});
    }

    if (typeof name !== 'string') {
        return res.status(422).json({status: 'error', message: 'Name must be a string'});
    }

    //Call Genderize API
    let apiData;
    try {
        const response = await fetch(`https://api.genderize.io/?name=${name}`);
        apiData = await response.json();
    } catch (error) {
        return res.status(502).json({status: 'error', message: 'Failed to fetch data from Genderize API'});
    }

    //Handle null response and zero count
    if (apiData == null || apiData.count == 0) {
        return res.status(200).json({status: 'error', message: 'No prediction available for the provided name'});
    }

    //process the response
    const gender = apiData.gender;
    const probability = apiData.probability;
    const sample_size = apiData.count;
    const is_confident = probability >= 0.7 && sample_size >= 100;
    const processed_at = new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');

    return res.status(200).json({
        status: 'success', 
        gender: gender, 
        probability: probability, 
        sample_size: sample_size, 
        is_confident: is_confident, 
        processed_at: processed_at
    });
});

app.listen(5000, () => {
    console.log(`Server is running on port 5000`);
});