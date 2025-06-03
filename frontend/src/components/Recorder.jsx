import { useState, useRef } from "react";

export default function Recorder({ onExchange, user }) {
  const [recording, setRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  const startRecording = async () => {
    if (!user) {
      console.error("User is not authenticated.");
      alert("Please log in to start recording.");
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);

      mediaRecorderRef.current.ondataavailable = (e) => {
        chunksRef.current.push(e.data);
      };

      mediaRecorderRef.current.onstop = async () => {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        chunksRef.current = [];
        try {
          // Step 1: Transcribe audio
          const formData = new FormData();
          formData.append("file", blob, "recording.mp3");
          const transcribeRes = await fetch("https://ai-voice-journaling.onrender.com/api/v1/transcribe", {
            method: "POST",
            body: formData,
          });
          if (!transcribeRes.ok) throw new Error(`Transcription failed: ${transcribeRes.statusText}`);
          const transcribedData = await transcribeRes.json();

          // Step 2: Analyze emotions
          const analyzeRes = await fetch("https://ai-voice-journaling.onrender.com/api/v1/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              text: transcribedData.text,
              user_id: user.id,
              conversation: [
                { role: "user", content: transcribedData.text }
              ]
            }),
          });
          if (!analyzeRes.ok) throw new Error(`Analysis failed: ${analyzeRes.statusText}`);
          const analyzedData = await analyzeRes.json();

          // Step 3: Respond with insights
          const respondRes = await fetch("https://ai-voice-journaling.onrender.com/api/v1/respond", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              user_id: user.id,
              conversation: [
                { role: "user", content: transcribedData.text },
                { role: "assistant", content: `I noticed these emotions: ${analyzedData.emotions.join(", ")}.` },
              ],
            }),
          });
          if (!respondRes.ok) throw new Error(`Response generation failed: ${respondRes.statusText}`);
          const responseData = await respondRes.json();

          onExchange(transcribedData.text, responseData.reply, analyzedData.emotions);
        } catch (error) {
          console.error("Error in workflow:", error);
        }
      };

      mediaRecorderRef.current.start();
      setRecording(true);
    } catch (error) {
      console.error("Error accessing microphone:", error);
      alert("Unable to access microphone. Please check your browser settings.");
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setRecording(false);
  };

  return (
    <div className="flex flex-col items-center p-4">
      <button
        onClick={recording ? stopRecording : startRecording}
        className={`
          w-16 h-16 rounded-full flex items-center justify-center 
          shadow-md transition-all focus:outline-none 
          ${recording 
            ? "bg-red-500 text-white scale-105" 
            : "bg-green-500 text-white hover:scale-105"
          }
        `}
      >
        {recording ? (
          <span className="text-2xl ">■</span>
        ) : (
          <span className="text-2xl">●</span>
        )}
      </button>
      <div className="mt-2 text-gray-500 text-sm ">
        {recording ? "Recording..." : "Press to record"}
      </div>
    </div>
  );
}