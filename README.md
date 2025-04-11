# RAM-based Secure File Sharing (Streamlit Version)

A secure file sharing application that uses RAM for temporary storage and client-side file handling. Files are never stored on the server's disk and are automatically deleted after download or after 1 hour.

## Features

- Secure file sharing using RAM storage
- Client-side file handling
- File encryption using Fernet (symmetric encryption)
- Automatic file deletion after download or timeout
- No database required
- Simple share code system
- Real-time storage statistics

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with:
   ```
   ENCRYPTION_KEY=your-secure-encryption-key-here
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

1. To share a file:
   - Click "Choose a file to share" to select a file
   - The file will be automatically uploaded and encrypted
   - Copy the generated share code
   - Share the code with others

2. To download a file:
   - Enter the share code in the download section
   - Click "Download File"
   - The file will be downloaded to your computer

## Security

- Files are encrypted using Fernet (symmetric encryption) before being stored in RAM
- Files are automatically deleted after download or after 1 hour
- No files are stored on the server's disk
- Share codes are randomly generated and unique

## Deployment on Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Set the following environment variables:
   - `ENCRYPTION_KEY`
5. Deploy!

## Technologies Used

- Framework: Streamlit
- Security: Cryptography (Fernet)
- Storage: Streamlit Session State (RAM)
- Environment Variables: python-dotenv 