let pc = new RTCPeerConnection();


async function createOffer() {
    console.log("sending offer request");

    const offerRes = await fetch("/offer", {
        method: "POST", 
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            sdp:"",
            type:"offer",
        }),
    });
    const offer = await offerRes.json();
    console.log("received offer response", offer);

    await pc.setRemoteDescription(new RTCSessionDescription(offer));
    const answer = await pc.createAnswer();
    await pc.setLocalDescription(answer);
}


createOffer()