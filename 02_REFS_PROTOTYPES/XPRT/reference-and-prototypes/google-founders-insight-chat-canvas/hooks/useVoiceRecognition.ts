
import { useState, useEffect, useCallback } from 'react';

interface SpeechRecognition extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  start: () => void;
  stop: () => void;
  onresult: (event: any) => void; // Simplified for brevity
  onerror: (event: any) => void;
  onend: () => void;
}

declare global {
  interface Window {
    SpeechRecognition: any; //typeof SpeechRecognition;
    webkitSpeechRecognition: any; //typeof SpeechRecognition;
  }
}

const useVoiceRecognition = (onResult: (transcript: string) => void) => {
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState<SpeechRecognition | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const SpeechRecognitionAPI = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognitionAPI) {
      setError("Voice recognition is not supported by your browser.");
      return;
    }
    const recogInstance = new SpeechRecognitionAPI();
    recogInstance.continuous = false;
    recogInstance.interimResults = false;
    recogInstance.lang = 'en-US';

    recogInstance.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      onResult(transcript);
      setIsListening(false); 
    };

    recogInstance.onerror = (event: any) => {
      console.error("Voice recognition error", event.error);
      setError(`Voice recognition error: ${event.error}`);
      setIsListening(false);
    };
    
    recogInstance.onend = () => {
        setIsListening(false);
    };

    setRecognition(recogInstance);

    return () => {
      if (recogInstance) {
        recogInstance.stop();
      }
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [onResult]); // onResult might change if it's not memoized, be careful

  const startListening = useCallback(() => {
    if (recognition && !isListening) {
      try {
        recognition.start();
        setIsListening(true);
        setError(null);
      } catch (e) {
        console.error("Error starting recognition: ", e);
        setError("Failed to start voice recognition.");
        setIsListening(false);
      }
    }
  }, [recognition, isListening]);

  const stopListening = useCallback(() => {
    if (recognition && isListening) {
      recognition.stop();
      setIsListening(false);
    }
  }, [recognition, isListening]);

  return { isListening, startListening, stopListening, error, supported: !!recognition };
};

export default useVoiceRecognition;
