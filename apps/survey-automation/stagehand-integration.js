/**
 * Stagehand Integration for Survey Automation
 * This provides browser viewing and AI-powered automation capabilities
 */

import { Stagehand } from "@browserbase/stagehand";

class SurveyStagehandManager {
    constructor(options = {}) {
        this.stagehand = new Stagehand({
            apiKey: process.env.BROWSERBASE_API_KEY,
            projectId: process.env.BROWSERBASE_PROJECT_ID,
            enableRecording: true,
            enableLiveView: true,
            headless: false, // Keep visible for viewing
            ...options
        });
        
        this.isInitialized = false;
        this.currentSession = null;
    }

    async initialize() {
        if (!this.isInitialized) {
            await this.stagehand.init();
            this.isInitialized = true;
            console.log("Stagehand initialized successfully");
        }
    }

    async startSurveySession(surveyUrl, userProfile) {
        await this.initialize();
        
        console.log(`Starting survey session for: ${surveyUrl}`);
        
        // Navigate to survey
        await this.stagehand.page.goto(surveyUrl);
        
        // Get live view URL for dashboard
        const liveViewUrl = await this.stagehand.getLiveViewUrl();
        console.log(`Live view available at: ${liveViewUrl}`);
        
        this.currentSession = {
            url: surveyUrl,
            profile: userProfile,
            liveViewUrl: liveViewUrl,
            startTime: new Date(),
            status: 'active'
        };
        
        return this.currentSession;
    }

    async fillSurveyWithAI(instructions) {
        if (!this.currentSession) {
            throw new Error("No active survey session");
        }

        // Use Stagehand's AI to understand and fill the survey
        const result = await this.stagehand.act({
            action: "fill_survey",
            instructions: instructions
        });

        return result;
    }

    async fillSurveyManually(fieldMappings) {
        if (!this.currentSession) {
            throw new Error("No active survey session");
        }

        // Manual field filling for precise control
        for (const [selector, value] of Object.entries(fieldMappings)) {
            await this.stagehand.page.fill(selector, value);
            await this.randomDelay();
        }
    }

    async randomDelay(min = 1000, max = 3000) {
        const delay = Math.random() * (max - min) + min;
        await new Promise(resolve => setTimeout(resolve, delay));
    }

    async takeScreenshot() {
        if (!this.currentSession) {
            throw new Error("No active survey session");
        }

        const screenshot = await this.stagehand.page.screenshot({
            fullPage: true,
            type: 'png'
        });

        return screenshot;
    }

    async getSessionRecording() {
        if (!this.currentSession) {
            throw new Error("No active survey session");
        }

        // Get the session recording URL
        const recordingUrl = await this.stagehand.getRecordingUrl();
        return recordingUrl;
    }

    async endSession() {
        if (this.currentSession) {
            const recording = await this.getSessionRecording();
            const endTime = new Date();
            
            const sessionSummary = {
                ...this.currentSession,
                endTime: endTime,
                duration: endTime - this.currentSession.startTime,
                recording: recording,
                status: 'completed'
            };

            await this.stagehand.close();
            this.currentSession = null;
            
            return sessionSummary;
        }
    }

    getLiveViewUrl() {
        return this.currentSession?.liveViewUrl || null;
    }

    getSessionStatus() {
        return this.currentSession || { status: 'inactive' };
    }
}

// Example usage for your survey automation
async function runSurveyWithStagehand(surveyConfig, userProfile) {
    const manager = new SurveyStagehandManager();
    
    try {
        // Start session
        const session = await manager.startSurveySession(surveyConfig.url, userProfile);
        console.log(`Live view: ${session.liveViewUrl}`);
        
        // Option 1: AI-powered automation
        await manager.fillSurveyWithAI(`
            Fill out this survey as a ${userProfile.age}-year-old from ${userProfile.location}.
            Use realistic answers that match the profile.
            Take your time and behave naturally.
        `);
        
        // Option 2: Manual field mapping (more precise)
        await manager.fillSurveyManually({
            'input[name="name"]': userProfile.name,
            'input[name="email"]': userProfile.email,
            'select[name="age_range"]': userProfile.ageRange,
            'textarea[name="comments"]': userProfile.comments
        });
        
        // Take screenshot for verification
        const screenshot = await manager.takeScreenshot();
        
        // End session and get recording
        const summary = await manager.endSession();
        
        return {
            success: true,
            session: summary,
            screenshot: screenshot
        };
        
    } catch (error) {
        console.error("Survey automation failed:", error);
        await manager.endSession();
        return {
            success: false,
            error: error.message
        };
    }
}

export { SurveyStagehandManager, runSurveyWithStagehand };
