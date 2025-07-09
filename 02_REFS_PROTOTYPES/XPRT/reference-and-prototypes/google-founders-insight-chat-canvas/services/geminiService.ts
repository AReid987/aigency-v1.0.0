
import { GoogleGenAI, Chat, GenerateContentResponse, Part } from "@google/genai";
import { GEMINI_MODEL_TEXT_CHAT, SYSTEM_PROMPT_INIT } from '../constants';
import { UploadedFile } from "../types";

const API_KEY = process.env.API_KEY;

if (!API_KEY) {
  console.error("API_KEY for Gemini is not set in environment variables.");
  // In a real app, you might want to throw an error or disable AI features.
}

const ai = new GoogleGenAI({ apiKey: API_KEY || "MISSING_API_KEY" }); // Fallback to prevent crash if key is missing

let chat: Chat | null = null;

const getChatSession = (): Chat => {
  if (!chat) {
    chat = ai.chats.create({
      model: GEMINI_MODEL_TEXT_CHAT,
      config: {
        systemInstruction: SYSTEM_PROMPT_INIT,
      },
      // history: [] // Optionally load history
    });
  }
  return chat;
};

export const sendMessageToGemini = async (
  messageText: string,
  uploadedFile?: UploadedFile,
  currentArtifacts?: {name: string, type: string}[]
): Promise<string> => {
  if (!API_KEY) return "Error: API Key for Gemini is not configured.";

  const chatSession = getChatSession();
  
  const messageParts: Part[] = [];
  
  let fullPromptText = messageText;
  if (currentArtifacts && currentArtifacts.length > 0) {
    const artifactList = currentArtifacts.map(a => `${a.name} (${a.type})`).join(', ');
    fullPromptText += `\n\n(Context: Current artifacts on graph: [${artifactList}])`;
  }
  messageParts.push({ text: fullPromptText });

  if (uploadedFile) {
    if (uploadedFile.type.startsWith('image/')) {
      messageParts.push({
        inlineData: {
          mimeType: uploadedFile.type,
          data: uploadedFile.base64Data,
        },
      });
    } else {
      // For non-image files, we can include their name/type and perhaps a snippet if possible,
      // or instruct the user to paste content. Here, just noting it.
      messageParts.push({ text: `\n(User has also uploaded a file: ${uploadedFile.name}, type: ${uploadedFile.type}. Analyze its name and type if relevant, or ask user to paste content if needed.)` });
    }
  }
  
  try {
    // Fix: chat.sendMessage expects the content (string or Part[]) under the 'message' key.
    const response: GenerateContentResponse = await chatSession.sendMessage({ message: messageParts });
    return response.text;
  } catch (error) {
    console.error("Error sending message to Gemini:", error);
    // Check for specific Gemini error types if available
    if (error instanceof Error) {
        return `Error interacting with AI: ${error.message}`;
    }
    return "Error interacting with AI. Please check console for details.";
  }
};

export const resetChat = () => {
  chat = null; // This will cause getChatSession to create a new chat instance
};

// Helper to convert File to UploadedFile format
export const fileToUploadedFile = async (file: File): Promise<UploadedFile> => {
  const base64EncodedDataPromise = new Promise<string>((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      if (reader.result) {
        resolve((reader.result as string).split(',')[1]);
      } else {
        reject(new Error("File reading failed"));
      }
    };
    reader.onerror = (error) => reject(error);
    reader.readAsDataURL(file);
  });
  
  return {
    name: file.name,
    type: file.type,
    base64Data: await base64EncodedDataPromise,
  };
};