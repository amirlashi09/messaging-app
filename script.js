let localStream;
let remoteStream;
let peerConnection;

const callButton = document.getElementById('call-button');
const hangupButton = document.getElementById('hangup-button');
const chatBox = document.getElementById('chat-box');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const welcomeContainer = document.getElementById('welcome-container');
const chatContainer = document.getElementById('chat-container');
const startButton = document.getElementById('start-button');
const nameInput = document.getElementById('name-input');

let userName = '';

// زمانی که دکمه شروع فشرده شود
startButton.addEventListener('click', () => {
    userName = nameInput.value;
    if (userName) {
        welcomeContainer.style.display = 'none';
        chatContainer.style.display = 'block';
    } else {
        alert('لطفاً نام خود را وارد کنید.');
    }
});

// تنظیمات ICE
const iceConfiguration = {
    iceServers: [
        { urls: 'stun:stun.l.google.com:19302' } // STUN server
    ]
};

// زمانی که دکمه تماس فشرده شود
callButton.addEventListener('click', async () => {
    localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    const videoElement = document.createElement('video');
    videoElement.srcObject = localStream;
    videoElement.play();
    document.body.appendChild(videoElement); // نمایش ویدیو محلی

    peerConnection = new RTCPeerConnection(iceConfiguration);
    
    localStream.getTracks().forEach(track => peerConnection.addTrack(track, localStream));
    
    peerConnection.onicecandidate = (event) => {
        if (event.candidate) {
            // ارسال candidate به سمت دیگر (نیاز به سرور برای ارسال)
        }
    };

    peerConnection.ontrack = (event) => {
        remoteStream = event.streams[0];
        const remoteVideo = document.createElement('video');
        remoteVideo.srcObject = remoteStream;
        remoteVideo.play();
        document.body.appendChild(remoteVideo); // نمایش ویدیو از طرف دیگر
    };

    const offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);
    // ارسال offer به سمت دیگر (نیاز به سرور برای ارسال)
});

// زمانی که دکمه پایان تماس فشرده شود
hangupButton.addEventListener('click', () => {
    peerConnection.close();
});

// ارسال پیام
sendButton.addEventListener('click', () => {
    const message = messageInput.value;
    if (message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message';
        messageElement.textContent = userName + ': ' + message; // نمایش نام کاربر در کنار پیام
        chatBox.appendChild(messageElement);
        messageInput.value = ''; // پاک کردن ورودی بعد از ارسال پیام
        chatBox.scrollTop = chatBox.scrollHeight; // پیمایش به پایین
    }
});
