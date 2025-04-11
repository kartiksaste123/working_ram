const express = require('express');
const cors = require('cors');
const CryptoJS = require('crypto-js');
const { nanoid } = require('nanoid');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// In-memory storage
const fileStorage = new Map();
const ENCRYPTION_KEY = process.env.ENCRYPTION_KEY || 'your-secret-key';

// Helper function to encrypt data
const encryptData = (data) => {
    return CryptoJS.AES.encrypt(data, ENCRYPTION_KEY).toString();
};

// Helper function to decrypt data
const decryptData = (encryptedData) => {
    const bytes = CryptoJS.AES.decrypt(encryptedData, ENCRYPTION_KEY);
    return bytes.toString(CryptoJS.enc.Utf8);
};

// Upload endpoint
app.post('/api/upload', (req, res) => {
    try {
        const { fileData, fileName } = req.body;
        if (!fileData || !fileName) {
            return res.status(400).json({ error: 'File data and name are required' });
        }

        // Generate a unique code
        const shareCode = nanoid(10);
        
        // Encrypt the file data
        const encryptedData = encryptData(fileData);
        
        // Store in RAM
        fileStorage.set(shareCode, {
            fileName,
            data: encryptedData,
            timestamp: Date.now()
        });

        // Set timeout to delete after 1 hour
        setTimeout(() => {
            fileStorage.delete(shareCode);
        }, 3600000); // 1 hour

        res.json({ shareCode });
    } catch (error) {
        console.error('Upload error:', error);
        res.status(500).json({ error: 'Failed to process file' });
    }
});

// Download endpoint
app.get('/api/download/:shareCode', (req, res) => {
    try {
        const { shareCode } = req.params;
        const fileData = fileStorage.get(shareCode);

        if (!fileData) {
            return res.status(404).json({ error: 'File not found or expired' });
        }

        // Decrypt the data
        const decryptedData = decryptData(fileData.data);

        res.json({
            fileName: fileData.fileName,
            fileData: decryptedData
        });

        // Delete the file after successful download
        fileStorage.delete(shareCode);
    } catch (error) {
        console.error('Download error:', error);
        res.status(500).json({ error: 'Failed to process file' });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
}); 