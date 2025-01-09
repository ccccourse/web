const ws = new WebSocket("ws://127.0.0.1:8000/ws");

const localVideo = document.getElementById("localVideo");
const remoteVideo = document.getElementById("remoteVideo");

let localStream;
let peerConnection;
const config = {
    iceServers: [{ urls: "stun:stun.l.google.com:19302" }],
};

// 獲取使用者媒體 (影音串流裝置)
async function startLocalStream() {
    localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    localVideo.srcObject = localStream;
}

// 建立 RTCPeerConnection
function createPeerConnection() {
    peerConnection = new RTCPeerConnection(config);

    // 當 ICE 候選者產生時，通過 WebSocket 傳送候選者
    peerConnection.onicecandidate = (event) => {
        if (event.candidate) {
            ws.send(JSON.stringify({ type: "ice-candidate", candidate: event.candidate }));
        }
    };

    // 當對方設備的媒體流到達時，將其顯示在遠端視訊元素中
    peerConnection.ontrack = (event) => {
        remoteVideo.srcObject = event.streams[0];
    };

    // 將本地媒體流的每個 track 添加到 PeerConnection
    localStream.getTracks().forEach((track) => {
        peerConnection.addTrack(track, localStream);
    });
}

// WebSocket 接收訊息處理
ws.onmessage = async (message) => {
    const data = JSON.parse(message.data);

    if (data.type === "offer") {
        if (!peerConnection) createPeerConnection();

        // 設定遠端描述
        await peerConnection.setRemoteDescription(new RTCSessionDescription(data.offer));
        
        // 創建一個 answer 並設定本地描述
        const answer = await peerConnection.createAnswer();
        await peerConnection.setLocalDescription(answer);
        
        // 將 answer 傳送給其他設備
        ws.send(JSON.stringify({ type: "answer", answer }));
    } else if (data.type === "answer") {
        // 設定遠端描述為 answer
        await peerConnection.setRemoteDescription(new RTCSessionDescription(data.answer));
    } else if (data.type === "ice-candidate") {
        // 收到 ICE 候選者，添加到 PeerConnection
        await peerConnection.addIceCandidate(data.candidate);
    }
};

// 發起通話，創建 offer 並發送
async function startCall() {
    if (!peerConnection) createPeerConnection();

    // 創建 offer
    const offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);
    
    // 發送 offer 給對方
    ws.send(JSON.stringify({ type: "offer", offer }));
}

// 初始化
startLocalStream().then(() => {
    document.body.addEventListener("click", startCall);
});
