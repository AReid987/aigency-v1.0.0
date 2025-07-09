---
Title: SystematicDesign
date: 2024-12-09
page-type: Project
Categories: PKM, Design, DesignSystems, AtomicDesignPrinciples
tags:
  - AtomicDesign
  - AtomicDesignPrinciples
  - AtomicDesignSystem
  - blackNoir
  - DesignSystem
  - phi
  - golden-ratio
  - fibonacci
---

---
## Table of Contents
- [[#BlackNoir Fundamentals|BlackNoir Fundamentals]]
	- [[#BlackNoir Fundamentals#Generative Design Systems|Generative Design Systems]]
	- [[#BlackNoir Fundamentals#Ideation|Ideation]]
		- [[#Ideation#Philosophy|Philosophy]]
		- [[#Ideation#Goals|Goals]]
		- [[#Ideation#Processes|Processes]]
		- [[#Ideation#Result|Result]]
	- [[#BlackNoir Fundamentals#Visualization|Visualization]]
		- [[#Visualization#1. Overall System Flow|1. Overall System Flow]]
		- [[#Visualization#2. Brand Color Selection Process|2. Brand Color Selection Process]]
		- [[#Visualization#3. Color Palette Generation|3. Color Palette Generation]]
		- [[#Visualization#4. Typography Scale Generation|4. Typography Scale Generation]]
		- [[#Visualization#5. Spatial System Generation|5. Spatial System Generation]]
	- [[#BlackNoir Fundamentals#Mathematical Models and Formulas|Mathematical Models and Formulas]]
		- [[#Mathematical Models and Formulas#Golden Ratio|Golden Ratio]]
		- [[#Mathematical Models and Formulas#Fibonacci Sequence|Fibonacci Sequence]]
		- [[#Mathematical Models and Formulas#Geometric Progression|Geometric Progression]]
		- [[#Mathematical Models and Formulas#Modular Scale|Modular Scale]]
		- [[#Mathematical Models and Formulas#Triadic Harmony|Triadic Harmony]]
		- [[#Mathematical Models and Formulas#Complimentary Colors|Complimentary Colors]]
		- [[#Mathematical Models and Formulas#Analogous Colors|Analogous Colors]]
		- [[#Mathematical Models and Formulas#Tetradic Harmony|Tetradic Harmony]]
		- [[#Mathematical Models and Formulas#Split Complementary|Split Complementary]]
	- [[#BlackNoir Fundamentals#User Interface Design|User Interface Design]]
		- [[#User Interface Design#Questionaire|Questionaire]]
		- [[#User Interface Design#Layout|Layout]]
		- [[#User Interface Design#Feedback Mechanisms|Feedback Mechanisms]]
		- [[#User Interface Design#Conditional Logic|Conditional Logic]]
		- [[#User Interface Design#Color Selection|Color Selection]]
	- [[#BlackNoir Fundamentals#II. Mathematical Models and Algorithms|II. Mathematical Models and Algorithms]]
		- [[#II. Mathematical Models and Algorithms#Color Palette Generation|Color Palette Generation]]
		- [[#II. Mathematical Models and Algorithms#Typography Scale Generation|Typography Scale Generation]]
		- [[#II. Mathematical Models and Algorithms#Spatial System Generation|Spatial System Generation]]
	- [[#BlackNoir Fundamentals#III. Design Token Generation and Output|III. Design Token Generation and Output]]
		- [[#III. Design Token Generation and Output#Color Palettes|Color Palettes]]
		- [[#III. Design Token Generation and Output#Typography Scales|Typography Scales]]
		- [[#III. Design Token Generation and Output#Spatial Systems|Spatial Systems]]
		- [[#III. Design Token Generation and Output#Output Formats|Output Formats]]
	- [[#BlackNoir Fundamentals#IV. Technology Stack|IV. Technology Stack]]
		- [[#IV. Technology Stack#Frontend|Frontend]]
		- [[#IV. Technology Stack#Backend|Backend]]
		- [[#IV. Technology Stack#Database|Database]]
	- [[#BlackNoir Fundamentals#V. Implementation Steps|V. Implementation Steps]]
		- [[#V. Implementation Steps#Questionnaire Design|Questionnaire Design]]
		- [[#V. Implementation Steps#Algorithm Implementation|Algorithm Implementation]]
		- [[#V. Implementation Steps#Design Token Management|Design Token Management]]
		- [[#V. Implementation Steps#UI/UX Prototyping|UI/UX Prototyping]]
		- [[#V. Implementation Steps#Backend Development|Backend Development]]
		- [[#V. Implementation Steps#Integration With Design Tools|Integration With Design Tools]]
- [[#Index|Index]]
	- [[#Index#[[🏠Home]]|[[🏠Home]]]]
	- [[#Index#[[PARA]]|[[PARA]]]]
	- [[#Index#[[Omnivore]]|[[Omnivore]]]]
	- [[#Index#[[Data]]|[[Data]]]]
	- [[#Index#[[DailyNotes]]|[[DailyNotes]]]]
	- [[#Index#[[Excalidraw]]|[[Excalidraw]]]]
---
## BlackNoir Fundamentals
### Generative Design Systems
> **"In nature nothing is created and nothing is destroyed, but everything is transformed."** - Antoine Laurent Delavosier
### Ideation 
2024-12-08
#### Philosophy
- Mathematical Systems, and Systems derived from Nature can be utilized as a guideline for creating design systems which are inherently enjoyable, appealing, and aesthetically pleasing to Users.
- An Intuitive interface can be provided to a user, enabling the co creation of a well-architected #DesignSystem, regardless of their level of Design expertise
- #fibonacci #phi #golden-ratio #AtomicDesignPrinciples
#### Goals
- Develop a system to enable a user to create a #DesignSystem with low friction
- Optimize #UX, reduce time and effort to reach successful output 
#### Processes
- Collaborate with an #Agent to generate an #AtomicDesignSystem
- Leverage an #agentic system to guide the user through a series of questions to inform the generation of design tokens
- Results of turns will iteratively generate #AtomicDesign elements 
#### Result
- At the conclusion of a session, the partial or completed #DesignSystem will be available for use. 
### Visualization
- #Diagrams generated collaboratively with #Khoj
#### 1. Overall System Flow

```mermaid
graph TD
    A[User Input: Brand Information] -- Determined? --> B{Brand Color?};
    B -- Yes --> C[Color Palette Generation];
    B -- No --> D[Brand Color Selection Process];
    D --> C;
    C --> E[Typography Scale Generation];
    E --> F[Spatial System Generation];
    F --> G[Atomic Design System Complete];
```
#### 2. Brand Color Selection Process
```mermaid
graph TD 
	A[Questionnaire: Brand Personality, Target Audience, Mission, Values, etc.] --> B(Psychological Color Associations); 
	B --> C["Primary Brand Color Selection (Hex Code Input)"];
```
#### 3. Color Palette Generation
```mermaid
graph TD 
	A["Input: Primary Brand Color (Hex Code)"] --> B{Mathematical Model Selection}; 
	B --> GR[Golden Ratio] --> C["Color Palette Output (Primary, Secondary, Accent, Neutral)"]; 
	B --> TH[Triadic Harmony] --> C; 
	B --> CP[Complementary] --> C; 
	B --> AG[Analogous] --> C; 
	B --> TT[Tetradic] --> C; 
	B --> SC[Split Complementary] --> C;
```

#### 4. Typography Scale Generation

```mermaid
graph TD 
	A["Input: Base Font Size (px)"] --> B{Mathematical Model Selection}; 
	B -- Fibonacci Sequence --> C["Typography Scale Output (Font Sizes)"]; 
	B -- "Geometric Progression (e.g., \(1.2^n\))" --> C; 
	B -- Modular Scale --> C;
```
#### 5. Spatial System Generation

```mermaid
graph TD
	A["Input: Base Spacing Unit (px)"] --> B{Mathematical Model Selection};
	B -- Fibonacci Sequence --> C["Spatial System Output (Spacing Units)"]; 
	B -- Modular Scale --> C; 
	B -- Golden Ratio --> C;
```

### Mathematical Models and Formulas
#### Golden Ratio:
- ( \phi = \frac{1 + \sqrt{5}}{2} \approx 1.618 ) 
- This ratio can be used to create harmonious proportions in #colorPalettes and #spatialSystems. 
- For color generation, you could use it to determine the luminance or saturation differences between colors. 
- For spacing, it can define the ratio between different spacing units.
    
#### Fibonacci Sequence:
- (0, 1, 1, 2, 3, 5, 8, 13, ...) 
- Each number is the sum of the two preceding ones. 
- This sequence can be used to create visually pleasing scales for #typography and #spacing. 
- For example, font sizes could be based on Fibonacci numbers.
    
#### Geometric Progression:
- (a, ar, ar^2, ar^3, ...) 
- where (a) is the first term and (r) is the common ratio. 
- This can be used to create a smooth, visually consistent #typography scale. 
- A common ratio of around 1.2 is often used.
    
#### Modular Scale:
- A system for creating harmonious scales based on a base unit and a ratio. 
- It's often used for #typography and #spacing. 
- Various ratios can be used, including the #GoldenRatio or other aesthetically pleasing ratios.
    
#### - Triadic Harmony: 
- A color scheme using three colors evenly spaced around the color wheel.
    
#### Complementary Colors:
- Colors opposite each other on the color wheel.
    
#### Analogous Colors:
- Colors adjacent to each other on the color wheel.
    
#### Tetradic Harmony:
- A color scheme using four colors, two pairs of complementary colors.
    
#### Split Complementary:
- A color scheme using a base color and the two colors adjacent to its complement.
### User Interface (UI) Design:**
#### Questionnaire:
- The questionnaire will be the core of the application. It will use a combination of question types, including:
    
    - Multiple-choice questions (radio buttons, checkboxes)
    - Rating scales (e.g., 1-5 stars, Likert scales)
    - Open-ended questions (text fields)
    - Color pickers (allowing users to select their preferred colors)
    - File uploads (for logos, mood boards, etc.)
#### Layout: 
- The layout will follow best practices for online questionnaires:
    
    - Clear and concise questions, avoiding jargon.
    - Logical grouping of questions into sections.
    - Progress indicators to show the user's progress.
    - Responsive design to adapt to different screen sizes.
    - Real-time validation to provide immediate feedback on user input.
    - Confirmation messages after each section or the entire questionnaire.
#### Feedback Mechanisms:
    
##### Real-time validation: 
- Error messages will appear immediately if the user enters invalid data.
##### Progress indicators: 
- A progress bar will show the user how far they are through the questionnaire.
##### Confirmation messages: 
 - A confirmation message will appear after each section or the entire questionnaire is completed.
##### Conditional Logic: 
- The questionnaire will use conditional logic to dynamically adjust the questions based on the user's previous answers. 
- This will ensure that only relevant questions are asked, improving the user experience and efficiency.
    
##### Color Selection:
- The app will include color pickers that allow users to select colors directly, or it will suggest colors based on their answers. 
- The color pickers should support hex codes, RGB, and HSL values.
### II. Mathematical Models and Algorithms

- The system will automatically select the most appropriate mathematical model based on the user's responses to the questionnaire. 
- This selection will be handled behind the scenes, without requiring the user to make any choices. 
- The models will include:
#### Color Palette Generation
- Golden Ratio
- Triadic Harmony
- Complementary Colors
- Analogous Colors
- Tetradic Harmony
- Split Complementary
#### Typography Scale Generation
- Fibonacci Sequence
- Geometric Progression
- Modular Scale
#### Spatial System Generation
- Fibonacci Sequence
- Modular Scale
- Golden Ratio
### III. Design Token Generation and Output
The generated design system will include:
#### Color Palettes
- Primary, secondary, accent, and neutral palettes 
- expressed in hex, RGB, HSL, and design tokens 
- following best practices from sources like Tokens Studio and Google Material 3
#### Typography Scales
- A range of font sizes based on the chosen mathematical model.
#### Spatial Systems
- A set of spacing units for consistent spacing throughout the design.
#### Output Formats
##### Downloadable files: 
- The design system will be available for download in various formats (e.g., JSON, CSS, SCSS).
##### Embedded preview: 
- A preview of the generated design system will be displayed within the web app.
##### Micro-frontend: 
- The generated design system could be packaged as a micro-frontend for easy integration into other applications.
##### Storybook: 
- A Storybook project could be generated to showcase the components of the design system.
##### Supernova: 
- A Supernova project could be generated to further streamline the design system's implementation.
### IV. Technology Stack
#### Frontend
- React, Next.js (or similar framework)
#### Backend
- #Nodejs, Express (or similar framework)
#### Database
- MongoDB (or similar NoSQL database)
### V. Implementation Steps
#### Questionnaire Design
- We need to create a detailed questionnaire with specific questions and question types. 
- This will require further research into best practices for brand information gathering.
#### Algorithm Implementation
- The algorithms for generating color palettes, typography scales, and spacing systems need to be implemented.
#### Design Token Management
- A system for managing and organizing design tokens needs to be developed.
#### UI/UX Prototyping
- A prototype of the web app should be created to test the user experience.
#### Backend Development
- The backend infrastructure needs to be built to handle data storage and processing.
#### Integration With Design Tools
- Explore the feasibility of integrating the generated design system with Figma, Storybook, and Supernova.

---

## Diagrams II
### Diagram 1: Overall System Flow

```mermaid
graph TD
	A["User Input:"] -- "Brand Information" --> B[Questionnaire] 
	B[Questionnaire] --> C[Data Processing]
	B[Questionnare] --> D[Model Selection];
	C --> E[Atomic Design System Generation]; 
	D --> E{Output Selection}; 
	E -- Downloadable Files --> F["Downloadable Files"]; 
	D -- Embedded Preview --> F[Embedded Preview in App]; 
	D -- Micro-frontend --> G[Micro-frontend Package]; 
	D -- Storybook --> H[Storybook Project]; 
	
```

### Diagram 2: Questionnaire (Simplified)

```mermaid
graph TD
	A[Start] --> B(Brand Information Questions); 
	B --> C(Target Audience Questions); 
	C --> D(Brand Personality Questions); 
	D --> E(Color Preferences Questions); 
	E --> F("File Uploads (Optional)"); 
	F --> G[End];
```

### Diagram 3: Data Processing & Model Selection

```mermaid
graph TD
	A[User Input Data] --> B("Algorithm Selection (LLM or Script)"); 
	B -- Golden Ratio Selected --> C[Golden Ratio Based Generation]; 
	B -- Triadic Harmony Selected --> D[Triadic Harmony Based Generation];     B -- Other Model Selected --> E[Other Model Based Generation]; 
	C --> F[Design Tokens]; D --> F; 
	E --> F; 
	F --> G[Generated Design System Data];
```

### Diagram 4: Atomic Design System Generation

```mermaid
graph LR
	A[Generated Design System Data] --> B(Color Palette Generation); 
	B --> C(Typography Scale Generation); 
	C --> D(Spacing System Generation); 
	D --> E[Complete Atomic Design System];
```

### Diagram 5: Output Formats

```mermaid
graph LR
	A[Complete Atomic Design System] --> B(Downloadable Files); 
	A --> C(Embedded Preview); A --> D(Micro-frontend); 
	A --> E(Storybook); 
	A --> F(Supernova);
```

---
## Detailed Questionnaire Design (Next Step 1):

- This is crucial for the app's success. 
- We need to define specific questions categorized into logical sections. 
- Consider these sections and example questions:

### Brand Overview:
#### Company Name: (Text field)
##### Brand Mission Statement: (Text area)
- Target Audience Description: (Text area) 
	- _Consider adding demographic questions here (age range, location, etc.)_
- Competitors: (Text field, allow multiple entries)
- Brand Personality (multiple choice, select all that apply): 
	- _e.g., Modern, Classic, Playful, Sophisticated, Minimalist, Bold_
- Industry: (Dropdown menu)
- Brand Voice: (Dropdown menu or multiple choice) 
	- _e.g., Formal, Informal, Humorous, Serious_
##### Existing Brand Assets (optional): 
- Logo upload, mood board upload, color palette upload (if available)

### **Color Preferences:**
    
##### Preferred Color Palette (optional): 
- Color picker(s) allowing multiple color selections.
##### Color Associations (multiple choice): 
- e.g., What colors do you associate with your brand? (List of colors with checkboxes)_
##### Color Avoidances (optional): 
- Color picker(s) or text field for specifying colors to avoid.

### **Typography Preferences:**
    
##### - Preferred Font Styles (optional):
- Dropdown menu(s) or text field(s) for specifying preferred font families (serif, sans-serif, etc.).
##### Examples of Typography you like (optional): 
- URL or image upload.
##### **Visual Style Preferences:**
    
- Visual Style Inspiration (optional): URL or image upload.
- Describe your ideal visual style: (Text area)

---

### **II. Algorithm Implementation (Next Step 2):**

This requires a skilled developer. The algorithms will need to:

#### 1. **Process Questionnaire Data:** 
- Extract relevant information from the user's responses.
#### 2. **Model Selection:** 
- Determine the most appropriate mathematical model for color palette, typography, and spacing based on the extracted data. 
- This might involve a rule-based system or a machine learning model (more complex).
#### 3. **Design Token Generation:** 
- Generate design tokens based on the chosen models. 
- This will involve calculations based on the selected mathematical models
- Golden Ratio, Fibonacci sequence, etc.
#### 4. **Output Formatting:** 
- Format the generated design tokens into the chosen output formats (JSON, CSS, SCSS, etc.).

### **III. Design Token Management (Next Step 3):**

This involves creating a system to:

#### **Organize Tokens:** 
- Structure the design tokens logically (e.g., by category: colors, typography, spacing).
#### **Version Control:** 
- Implement version control for design tokens to track changes and allow for rollback.
#### **Documentation:** 
- Generate clear documentation for the design tokens.

### **IV. UI/UX Prototyping (Next Step 4):**

- Before full development, create a prototype to test the user flow and UI design. 
- Tools like Figma or Adobe XD are suitable for this.

### **V. Backend Development (Next Step 5):**

The backend will handle:

#### **Data Storage:** 
- Store user responses and generated design systems.
#### **Algorithm Execution:** 
- Run the algorithms to generate design systems.
#### **API:** 
- Provide an API for the frontend to interact with.

### **VI. Integration with Design Tools (Next Step 6):**
- Investigate APIs or plugins for Figma, Storybook, and Supernova
- Explore seamless integration. 
- This is a more advanced step and might be tackled later.

#### **Technology Stack Considerations:**

- Your suggested stack (React, Next.js, Node.js, Express, MongoDB) is a good starting point. 
- Consider these points:

#### **Frontend Framework:** 
- React and Next.js are excellent choices for a modern web application.
#### **Backend Framework:** 
- Node.js and Express are a solid combination for a scalable backend.
#### **Database:** 
- MongoDB is suitable for storing semi-structured data like user responses and design tokens. 
- However, a relational database might be considered if you anticipate complex relationships between data points.

---

## **Next Steps for Immediate Action:**

#### 1. **Refine the Questionnaire:** 
- Complete the detailed questionnaire design with specific questions and question types.
#### 2. **Choose a Prototyping Tool:** 
-  Select a prototyping tool (Figma, Adobe XD, etc.) and start creating a prototype.
#### 5. **Identify Core Algorithms:** 
-  Focus on implementing the core algorithms for color palette generation, typography scale generation, and spacing system generation. 
-  Start with simpler algorithms and gradually add more complexity.

---

To move forward effectively, let's break down the next steps with more detail and address potential challenges:

## **I. Detailed Questionnaire Design (Next Step 1):**

- This is crucial for the app's success. 
- We need to define specific questions categorized into logical sections. 
- Consider these sections and example questions:

### **Brand Overview:**
    
#### Company Name: (Text field)
#### Brand Mission Statement: (Text area)
#### Target Audience Description: (Text area) 
- _Consider adding demographic questions here (age range, location, etc.)_
#### Competitors: (Text field, allow multiple entries)
#### Brand Personality 
- (multiple choice, select all that apply): 
- _e.g., Modern, Classic, Playful, Sophisticated, Minimalist, Bold_
#### Industry: (Dropdown menu)
#### Brand Voice: (Dropdown menu or multiple choice) 
- _e.g., Formal, Informal, Humorous, Serious_
#### Existing Brand Assets (optional): 
- Logo upload
- mood board upload
- color palette upload (if available)
#### **Color Preferences:**
    
##### Preferred Color Palette (optional): 
- Color picker(s) allowing multiple color selections.
##### Color Associations (multiple choice): 
- _e.g., What colors do you associate with your brand? (List of colors with checkboxes)_
/h5 Color Avoidances (optional): 
- Color picker(s) or text field for specifying colors to avoid.
### **Typography Preferences:**
    
#### Preferred Font Styles (optional): 
- Dropdown menu(s) or text field(s) 
- for specifying preferred font families (serif, sans-serif, etc.).
- Examples of Typography you like (optional): URL or image upload.
#### **Visual Style Preferences:**
    
##### Visual Style Inspiration (optional): URL or image upload.
##### Describe your ideal visual style: (Text area)

### **II. Algorithm Implementation (Next Step 2):**

- his requires a skilled developer. 
- The algorithms will need to:

#### 1. **Process Questionnaire Data:** 
- Extract relevant information from the user's responses.
#### 2. **Model Selection:** 
- Determine the most appropriate mathematical model for 
	- color palette
	- typography
	- spacing 
- based on the extracted data. 
- This might involve a rule-based system or a machine learning model (more complex).
#### 3. **Design Token Generation:** 
- Generate design tokens based on the chosen models. 
- This will involve calculations based on the selected mathematical models 
- Golden Ratio, Fibonacci sequence, etc.
#### 4. **Output Formatting:** 
- Format the generated design tokens into the chosen output formats (JSON, CSS, SCSS, etc.).

### **III. Design Token Management (Next Step 3):**

This involves creating a system to:

#### **Organize Tokens:** 
- Structure the design tokens logically (e.g., by category: colors, typography, spacing).
#### **Version Control:** 
- Implement version control for design tokens to track changes and allow for rollback.
#### **Documentation:** 
- Generate clear documentation for the design tokens.

### **IV. UI/UX Prototyping (Next Step 4):**

- Before full development, create a prototype to test the user flow and UI design. 
- Tools like Figma or Adobe XD are suitable for this.

### **V. Backend Development (Next Step 5):**

The backend will handle:

#### **Data Storage:** 
- Store user responses and generated design systems.
#### **Algorithm Execution:** 
- Run the algorithms to generate design systems.
#### **API:** 
- Provide an API for the frontend to interact with.

### **VI. Integration with Design Tools (Next Step 6):**

- Investigate APIs or plugins for Figma, Storybook, and Supernova to explore seamless integration. 
- This is a more advanced step and might be tackled later.
- 
### **Technology Stack Considerations:**

Your suggested stack (React, Next.js, Node.js, Express, MongoDB) is a good starting point. 

Consider these points:

#### **Frontend Framework:** 
- React and Next.js are excellent choices for a modern web application.
#### **Backend Framework:** 
- Node.js and Express are a solid combination for a scalable backend.
#### **Database:** 
- MongoDB is suitable for storing semi-structured data like user responses and design tokens. 
- However, a relational database might be considered if you anticipate complex relationships between data points.

### **Next Steps for Immediate Action:**

1. **Refine the Questionnaire:** Complete the detailed questionnaire design with specific questions and question types.
2. **Choose a Prototyping Tool:** Select a prototyping tool (Figma, Adobe XD, etc.) and start creating a prototype.
3. **Identify Core Algorithms:** Focus on implementing the core algorithms for color palette generation, typography scale generation, and spacing system generation. Start with simpler algorithms and gradually add more complexity.
---

## Systematic Brand Color Palettes

Once you have a primary brand color, you can use several methods to generate a harmonious color palette using these color schemes
- Golden Ratio
- Triadic Harmony
- Complementary Colors
- Tetradic Harmony
- Split Complementary 

The methods below assume you're working in a color space like 
- HSL (Hue, Saturation, Lightness) 
- HSV (Hue, Saturation, Value) 
which are better suited for these calculations than RGB. 
Many online tools and libraries allow you to convert between color spaces.

### **I. Using a Color Wheel and Color Harmony Rules:**

- This is the most intuitive approach. 
- Most online color palette generators 
	- (like those listed in the previous internet data) 
	- allow you to select a color harmony rule 
	- automatically generate the remaining colors.

#### 1. **Input your primary color:** 
- Enter primary brand color's values into color palette generator.
	- hex code
	- RGB
	- HSL values 
#### 2. **Select the desired harmony:** 
- Choose the harmony rule from the generator's options
	- Triadic
	- Complementary
	- Tetradic
	- Split Complementary
- The generator will 
	- calculate and display other colors in the palette 
	- based on the selected harmony rule.

###  **II. Manual Calculation (More Advanced):**

- This approach requires 
	- understanding color theory 
	- some mathematical calculations. 
- It's best done with programming or a spreadsheet.

#### **A. Triadic Harmony:**

- A triadic harmony uses three colors evenly spaced around the color wheel 
- 120 degrees apart

##### 1. **Determine the hue:** 
- Find the hue of your primary color (H in HSL or HSV).
##### 2. **Calculate the other hues:** 
- Add 120 and 240 degrees to the primary hue. 
- If the result exceeds 360, subtract 360. 
- This gives you the hues of the other two colors.
##### 3. **Adjust saturation and lightness/value:** 
- You can adjust all three colors fine-tune the palette
	- saturation (S)  
	- lightness/value (L/V) 
	- Keep the saturation relatively consistent for a balanced palette.

#### **B. Complementary Colors:**

- Directly opposite each other on the color wheel 
- 180 degrees apart).

##### 1. **Determine the hue:**
- Find the hue of your primary color.
##### 2. **Calculate the complementary hue:** 
- Add 180 degrees to the primary hue. 
- If the result exceeds 360, subtract 360.
##### 3. **Adjust saturation and lightness/value:**
- Adjust S and L/V as needed.

#### **C. Tetradic Harmony:**

- A tetradic harmony uses four colors, two complementary pairs.

##### 1. **Find the complementary hue:** 
- As in the complementary color method 
- find the hue 180 degrees from your primary color.
##### 2. **Find adjacent colors:** 
- Find hues 90 degrees away from primary and complementary hues. 
- This will give you four colors forming two complementary pairs.
##### 3. **Adjust saturation and lightness/value:** 
- Adjust S and L/V as needed.

#### **D. Split Complementary Colors:**

- A split-complementary palette uses the primary color and the two colors adjacent to its complement.

##### 1. **Find the complementary hue:** 
- As in the complementary color method, 
- find the hue 180 degrees from your primary color.
##### 2. **Find adjacent colors:** 
- Find the hues 30 degrees on either side of the complementary hue. 
- This gives you three colors.
##### 3. **Adjust saturation and lightness/value:** 
- Adjust S and L/V as needed.

#### **E. Applying the Golden Ratio:**

- The Golden Ratio (approximately 1.618) 
- can be applied in several ways:

##### 1. **Hue Spacing:** 
- Instead of fixed intervals (120, 180 degrees)
- use the Golden Ratio to determine the spacing between hues. 
- This is more complex and requires iterative calculations.
##### 2. **Saturation/Lightness/Value Ratios:** 
- Use the Golden Ratio to determine the ratios of 
	- saturation and lightness/value 
	- between colors in your palette. 
- For example, you might have a 
	- primary color with 100% saturation
	- a secondary color with 61.8% saturation (100/1.618)
	- and a tertiary color with 38.2% saturation (61.8/1.618).

### **III. Using Software/Libraries:**

- Many programming languages have libraries that handle 
	- color manipulation 
	- color harmony calculations. 
- These libraries can simplify the process significantly.
- For example, in JavaScript, you could use a library like chroma.js.

#### **Example (Conceptual using JavaScript and chroma.js):**

- This is a simplified example and would need adaptation 
- based on your specific needs and the chosen library.

```javascript
// Assuming you have your primary color in hex format
const primaryColorHex = '#FF6347'; // Tomato

// Using chroma.js (you'll need to include the library)
const primaryColor = chroma(primaryColorHex);

// Complementary color
const complementaryColor = primaryColor.complement();

// Triadic colors (simplified - you might need more precise calculations)
const triadicColor1 = primaryColor.rotate(120);
const triadicColor2 = primaryColor.rotate(240);

// Output the hex codes
console.log("Primary:", primaryColor.hex());
console.log("Complementary:", complementaryColor.hex());
console.log("Triadic 1:", triadicColor1.hex());
console.log("Triadic 2:", triadicColor2.hex());

// ... similar calculations for tetradic and split complementary ...
```

- adjust saturation and lightness/value to achieve the desired aesthetic. 
- Experimentation is key to finding the best palette for your brand.
- Using online tools is often the easiest approach for beginners
- manual calculation or using libraries provides more control for advanced users.

---


---
## Index
### [[🏠Home]]
### [[PARA]]
### [[Omnivore]]
### [[Data]]
### [[DailyNotes]]
### [[Excalidraw]]

