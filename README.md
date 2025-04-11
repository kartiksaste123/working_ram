# RAM-based Secure File Sharing

A secure file sharing application that uses RAM for temporary storage and client-side file handling. Files are never stored on the server's disk and are automatically deleted after download or after 1 hour.

## Features

- Secure file sharing using RAM storage
- Client-side file handling
- File encryption
- Automatic file deletion after download or timeout
- No database required
- Simple share code system

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   cd client
   npm install
   ```

3. Create a `.env` file in the root directory with:
   ```
   PORT=3000
   ENCRYPTION_KEY=your-secure-encryption-key-here
   ```

4. Start the backend server:
   ```bash
   npm start
   ```

5. Start the frontend development server:
   ```bash
   cd client
   npm start
   ```

## Usage

1. To share a file:
   - Click "Choose File" to select a file
   - Click "Share File"
   - Copy the generated share code
   - Share the code with others

2. To download a file:
   - Enter the share code
   - Click "Download File"
   - The file will be downloaded to your computer

## Security

- Files are encrypted before being stored in RAM
- Files are automatically deleted after download or after 1 hour
- No files are stored on the server's disk
- Share codes are randomly generated and unique

## Deployment

This application can be deployed on Render:

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the following environment variables:
   - `PORT`
   - `ENCRYPTION_KEY`
4. Set the build command: `cd client && npm install && npm run build`
5. Set the start command: `npm start`

## Technologies Used

- Backend: Node.js, Express
- Frontend: React
- Security: CryptoJS
- Storage: In-memory Map 