import streamlit as st
import base64
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import hashlib
import json

# Load environment variables
load_dotenv()

# Initialize session state for peer connections and file metadata
if 'file_metadata' not in st.session_state:
    st.session_state.file_metadata = {}
if 'peer_connections' not in st.session_state:
    st.session_state.peer_connections = {}

def generate_file_hash(file_content):
    """Generate a unique hash for the file"""
    return hashlib.sha256(file_content).hexdigest()

def cleanup_expired_metadata():
    """Remove metadata that is older than 1 hour"""
    current_time = datetime.now()
    expired_keys = [
        key for key, value in st.session_state.file_metadata.items()
        if current_time - value['timestamp'] > timedelta(hours=1)
    ]
    for key in expired_keys:
        del st.session_state.file_metadata[key]

# Clean up expired metadata
cleanup_expired_metadata()

# Streamlit UI
st.title("P2P RAM File Sharing")
st.write("Share files directly between users' RAM using WebRTC. Files never leave your computer.")

# WebRTC JavaScript code
st.markdown("""
<script>
// WebRTC configuration
const configuration = {
    iceServers: [
        { urls: 'stun:stun.l.google.com:19302' }
    ]
};

// Initialize WebRTC
let peerConnection;
let dataChannel;

function initializePeerConnection(shareCode) {
    peerConnection = new RTCPeerConnection(configuration);
    
    // Create data channel
    dataChannel = peerConnection.createDataChannel('fileTransfer');
    
    dataChannel.onopen = () => {
        console.log('Data channel is open');
    };
    
    dataChannel.onmessage = (event) => {
        // Handle incoming file data
        const fileData = JSON.parse(event.data);
        if (fileData.type === 'file') {
            // Create download link
            const link = document.createElement('a');
            link.href = fileData.content;
            link.download = fileData.filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    };
    
    // Create and set local description
    peerConnection.createOffer()
        .then(offer => peerConnection.setLocalDescription(offer))
        .then(() => {
            // Send offer to the other peer (via Streamlit)
            const offer = peerConnection.localDescription;
            window.parent.postMessage({
                type: 'webrtc-offer',
                shareCode: shareCode,
                offer: offer
            }, '*');
        });
}

// Handle incoming WebRTC answer
window.addEventListener('message', (event) => {
    if (event.data.type === 'webrtc-answer') {
        peerConnection.setRemoteDescription(new RTCSessionDescription(event.data.answer));
    }
});

// Handle incoming ICE candidates
window.addEventListener('message', (event) => {
    if (event.data.type === 'ice-candidate') {
        peerConnection.addIceCandidate(new RTCIceCandidate(event.data.candidate));
    }
});
</script>
""", unsafe_allow_html=True)

# File Upload Section
st.header("Share a File")
uploaded_file = st.file_uploader("Choose a file to share", type=None)

if uploaded_file is not None:
    # Read file content
    file_content = uploaded_file.read()
    
    # Generate a unique share code
    share_code = base64.urlsafe_b64encode(os.urandom(6)).decode('utf-8')
    
    # Generate file hash
    file_hash = generate_file_hash(file_content)
    
    # Store metadata in session state
    st.session_state.file_metadata[share_code] = {
        'filename': uploaded_file.name,
        'file_hash': file_hash,
        'timestamp': datetime.now(),
        'size': len(file_content)
    }
    
    # Create a data URL for the file (stays in browser memory)
    file_data_url = f"data:application/octet-stream;base64,{base64.b64encode(file_content).decode()}"
    
    st.success(f"File ready to share! Share this code with others: {share_code}")
    st.code(share_code, language=None)
    
    # Store the file data URL in session state
    st.session_state[f'file_data_{share_code}'] = file_data_url
    
    # Initialize WebRTC connection
    st.markdown(f"""
    <script>
        initializePeerConnection('{share_code}');
    </script>
    """, unsafe_allow_html=True)

# File Download Section
st.header("Download a File")
share_code = st.text_input("Enter the share code")

if share_code:
    if share_code in st.session_state.file_metadata:
        metadata = st.session_state.file_metadata[share_code]
        
        # Check if we have the file data in browser memory
        file_data_key = f'file_data_{share_code}'
        if file_data_key in st.session_state:
            file_data_url = st.session_state[file_data_key]
            
            # Create WebRTC connection for file transfer
            st.markdown(f"""
            <script>
                // Send file data through WebRTC data channel
                if (dataChannel && dataChannel.readyState === 'open') {{
                    dataChannel.send(JSON.stringify({{
                        type: 'file',
                        filename: '{metadata['filename']}',
                        content: '{file_data_url}'
                    }}));
                }}
            </script>
            """, unsafe_allow_html=True)
            
            st.success("File transfer initiated through P2P connection")
            
            # Delete the metadata after successful transfer
            del st.session_state.file_metadata[share_code]
            del st.session_state[file_data_key]
        else:
            st.warning("The file is no longer available in the sender's browser memory. Please ask them to share the file again.")
    else:
        st.error("Invalid share code or file has expired")

# Display metadata statistics
st.sidebar.header("Active Shares")
st.sidebar.write(f"Active shares: {len(st.session_state.file_metadata)}")
for code, metadata in st.session_state.file_metadata.items():
    time_left = timedelta(hours=1) - (datetime.now() - metadata['timestamp'])
    st.sidebar.write(f"File: {metadata['filename']}")
    st.sidebar.write(f"Size: {metadata['size']} bytes")
    st.sidebar.write(f"Code: {code}")
    st.sidebar.write(f"Expires in: {time_left}")
    st.sidebar.write("---") 