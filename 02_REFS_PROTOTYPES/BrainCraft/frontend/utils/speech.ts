import { createLogger } from './logger';

const logger = createLogger('speech_utils');

// Check if browser supports speech synthesis
const isSpeechSynthesisSupported = (): boolean => {
  return typeof window !== 'undefined' && 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window;
};

// Speech options interface
export interface SpeechOptions {
  voice?: SpeechSynthesisVoice | null;
  rate?: number; // 0.1 to 10, default 1
  pitch?: number; // 0 to 2, default 1
  volume?: number; // 0 to 1, default 1
  lang?: string; // e.g., 'en-US', 'fr-FR', etc.
}

// Default speech options
const defaultOptions: SpeechOptions = {
  rate: 1,
  pitch: 1,
  volume: 1,
  lang: 'en-US',
};

// Speech synthesis utility class
export class SpeechService {
  private static instance: SpeechService;
  private speaking: boolean = false;
  private queue: string[] = [];
  private options: SpeechOptions;
  private synth: SpeechSynthesis | null = null;
  private voices: SpeechSynthesisVoice[] = [];
  private voicesLoaded: boolean = false;

  private constructor() {
    this.options = { ...defaultOptions };
    
    // Only run this code in the browser
    if (typeof window !== 'undefined' && isSpeechSynthesisSupported()) {
      this.synth = window.speechSynthesis;
      this.loadVoices();
      
      // Some browsers (like Chrome) load voices asynchronously
      if (this.synth && this.voices.length === 0) {
        this.synth.onvoiceschanged = () => this.loadVoices();
      }
    } else {
      logger.warn('Speech synthesis is not supported in this browser or running on server');
    }
  }

  public static getInstance(): SpeechService {
    if (!SpeechService.instance) {
      SpeechService.instance = new SpeechService();
    }
    return SpeechService.instance;
  }

  private loadVoices(): void {
    if (!this.synth) return;
    
    this.voices = this.synth.getVoices();
    this.voicesLoaded = true;
    logger.info(`Loaded ${this.voices.length} voices for speech synthesis`);
  }

  public getVoices(): SpeechSynthesisVoice[] {
    return this.voices;
  }

  public isSupported(): boolean {
    return isSpeechSynthesisSupported();
  }

  public setOptions(options: SpeechOptions): void {
    this.options = { ...this.options, ...options };
  }

  public getDefaultVoice(lang: string = 'en-US'): SpeechSynthesisVoice | null {
    if (!this.voicesLoaded) return null;
    
    // Try to find a voice for the specified language
    const langVoices = this.voices.filter(voice => voice.lang.startsWith(lang.substring(0, 2)));
    
    // Prefer native voices if available
    const nativeVoice = langVoices.find(voice => voice.localService);
    if (nativeVoice) return nativeVoice;
    
    // Otherwise, use any voice for the language
    return langVoices[0] || null;
  }

  public speak(text: string, options?: SpeechOptions): Promise<void> {
    if (!this.isSupported() || !this.synth) {
      logger.error('Speech synthesis not supported');
      return Promise.reject(new Error('Speech synthesis not supported'));
    }

    const mergedOptions = { ...this.options, ...options };
    const utterance = new SpeechSynthesisUtterance(text);
    
    // Apply options
    utterance.rate = mergedOptions.rate || defaultOptions.rate!;
    utterance.pitch = mergedOptions.pitch || defaultOptions.pitch!;
    utterance.volume = mergedOptions.volume || defaultOptions.volume!;
    utterance.lang = mergedOptions.lang || defaultOptions.lang!;
    
    // Set voice if provided
    if (mergedOptions.voice) {
      utterance.voice = mergedOptions.voice;
    } else {
      // Try to find a suitable voice
      const voice = this.getDefaultVoice(utterance.lang);
      if (voice) utterance.voice = voice;
    }

    return new Promise((resolve, reject) => {
      utterance.onend = () => {
        this.speaking = false;
        logger.debug('Speech completed');
        this.processQueue();
        resolve();
      };
      
      utterance.onerror = (event) => {
        this.speaking = false;
        logger.error('Speech synthesis error', event);
        this.processQueue();
        reject(new Error('Speech synthesis error'));
      };

      // If already speaking, add to queue
      if (this.speaking) {
        this.queue.push(text);
        logger.debug('Added speech to queue');
        resolve();
      } else {
        try {
          this.speaking = true;
          logger.debug('Speaking text');
          this.synth.speak(utterance);
          // Some browsers need this to work consistently
          if (this.synth.paused) {
            this.synth.resume();
          }
        } catch (error) {
          this.speaking = false;
          logger.error('Failed to speak', error);
          reject(error);
        }
      }
    });
  }

  private processQueue(): void {
    if (this.queue.length > 0 && !this.speaking) {
      const nextText = this.queue.shift();
      if (nextText) {
        this.speak(nextText);
      }
    }
  }

  public stop(): void {
    if (this.synth) {
      this.synth.cancel();
      this.speaking = false;
      this.queue = [];
      logger.debug('Speech cancelled');
    }
  }

  public pause(): void {
    if (this.synth) {
      this.synth.pause();
      logger.debug('Speech paused');
    }
  }

  public resume(): void {
    if (this.synth) {
      this.synth.resume();
      logger.debug('Speech resumed');
    }
  }
}

// Export a singleton instance - only created client-side
export const speechService = typeof window !== 'undefined' ? SpeechService.getInstance() : null;

// Utility function to play audio from base64 string
export const playAudioFromBase64 = (base64Audio: string): Promise<void> => {
  return new Promise((resolve, reject) => {
    // Check if we're in a browser environment
    if (typeof window === 'undefined') {
      reject(new Error('Audio playback is only available in browser environments'));
      return;
    }
    
    try {
      // Convert base64 to audio
      const audio = new Audio(`data:audio/mp3;base64,${base64Audio}`);
      
      audio.onended = () => {
        logger.debug('Audio playback completed');
        resolve();
      };
      
      audio.onerror = (error) => {
        logger.error('Audio playback error', error);
        reject(error);
      };
      
      logger.debug('Playing audio from base64');
      audio.play().catch(error => {
        logger.error('Failed to play audio', error);
        reject(error);
      });
    } catch (error) {
      logger.error('Error creating audio from base64', error);
      reject(error);
    }
  });
};