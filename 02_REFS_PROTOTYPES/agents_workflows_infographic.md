<!DOCTYPE html>

<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Evolution of User Interaction</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
<style>
body {
font-family: 'Inter', sans-serif;
}
.chart-container {
position: relative;
width: 100%;
max-width: 400px;
margin-left: auto;
margin-right: auto;
height: 300px;
max-height: 400px;
}
.flow-line {
position: relative;
width: 2px;
background-color: #0d9488;
margin: 0 auto;
}
.flow-line::after {
content: '';
position: absolute;
bottom: -1px;
left: 50%;
transform: translateX(-50%);
width: 0;
height: 0;
border-left: 6px solid transparent;
border-right: 6px solid transparent;
border-top: 8px solid #0d9488;
}
.h-flow-line {
position: relative;
height: 2px;
background-color: #0d9488;
flex-grow: 1;
}
.h-flow-line::after {
content: '';
position: absolute;
top: 50%;
right: -1px;
transform: translateY(-50%);
width: 0;
height: 0;
border-top: 6px solid transparent;
border-bottom: 6px solid transparent;
border-left: 8px solid #0d9488;
}
.radial-line {
position: absolute;
background-color: #0ea5e9;
transform-origin: left center;
}
</style>
</head>
<body class="bg-slate-100 text-slate-800">
<!--
Narrative Plan:
The infographic tells a story about the evolution of user interaction in applications, starting from personalized but guided experiences (Adaptive Onboarding), moving to scripted interactions (Dialogue Trees), and culminating in intelligent, autonomous systems (AI Agents). The visual narrative progresses from structured, linear diagrams to a more dynamic, radial representation, highlighting the increasing sophistication.

```
    Color Palette Chosen: "Brilliant Blues" and complementary teals.
    - Primary Text: #1e293b (slate-800)
    - Accent Blue: #0ea5e9 (sky-500)
    - Accent Teal: #0d9488 (teal-600)
    - Background: #f1f5f9 (slate-100)
    - Card Background: #ffffff (white)

    Visualization Choices:
    1. Adaptive Onboarding Dashboard:
       - Goal: Organize
       - Chosen Visualization: HTML/CSS Flow Chart
       - Justification: A flowchart is ideal for showing the step-by-step process of how user data is used to create a personalized dashboard. This method uses styled divs and borders to create a clear visual flow without relying on images or prohibited libraries. CONFIRMED: NO SVG/MERMAID.
    2. Dialogue Trees/Flows:
       - Goal: Organize
       - Chosen Visualization: HTML/CSS Tree Diagram
       - Justification: This visually represents the rigid, branching nature of a dialogue tree, effectively communicating the concept of pre-determined paths. It's built with HTML/CSS to adhere to constraints. CONFIRMED: NO SVG/MERMAID.
    3. AI Agent System:
       - Goal: Inform and Organize
       - Chosen Visualization: HTML/CSS Radial Diagram & Chart.js Donut Chart
       - Justification: The radial diagram shows the interconnected, non-linear functions of an AI agent (Perception, Decision, Action), contrasting it with the previous linear diagrams. The Donut chart provides a powerful, single data point to "Inform" the user of the AI's high effectiveness in a visually engaging way using Chart.js on a Canvas element. CONFIRMED: NO SVG/MERMAID.

    Constraint Confirmation:
    - NEITHER Mermaid JS NOR SVG were used in this document. All diagrams are built with HTML and Tailwind CSS. Charts are rendered on HTML Canvas elements by Chart.js.
-->

<div class="container mx-auto max-w-5xl p-4 sm:p-6 md:p-8">

    <header class="text-center mb-12">
        <h1 class="text-4xl md:text-5xl font-black text-slate-900 mb-2">The Evolution of User Interaction</h1>
        <p class="text-lg text-slate-600">From Guided Setups to Intelligent Agents</p>
    </header>

    <main>
        <section id="adaptive-onboarding" class="mb-12">
            <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8">
                <h2 class="text-3xl font-bold text-sky-600 mb-4 flex items-center">
                    <span class="text-4xl mr-4">🚀</span> Adaptive Onboarding Dashboard
                </h2>
                <p class="text-slate-600 mb-8 text-lg">
                    The first step beyond a one-size-fits-all introduction is creating a personalized welcome mat for new users. An adaptive dashboard doesn't just show a generic tutorial; it intelligently curates the initial experience based on who the user is and what they need, making the app feel helpful and intuitive from the very first moment.
                </p>

                <div class="text-center">
                    <div class="inline-block bg-sky-100 text-sky-800 rounded-lg px-4 py-2 font-bold shadow-sm">User Provides Input</div>
                    <div class="flow-line h-8"></div>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-center mb-6">
                        <div class="bg-slate-100 p-4 rounded-lg shadow-sm">
                            <p class="font-bold text-slate-700">Grade Level</p>
                            <p class="text-2xl">📚</p>
                        </div>
                        <div class="bg-slate-100 p-4 rounded-lg shadow-sm">
                            <p class="font-bold text-slate-700">Subjects of Interest</p>
                            <p class="text-2xl">🔬</p>
                        </div>
                        <div class="bg-slate-100 p-4 rounded-lg shadow-sm">
                            <p class="font-bold text-slate-700">Learning Style</p>
                            <p class="text-2xl">🎨</p>
                        </div>
                    </div>
                    <div class="flow-line h-8"></div>
                    <div class="inline-block bg-teal-100 text-teal-800 rounded-lg px-4 py-2 font-bold shadow-sm">Adaptive Engine Processes Data</div>
                    <div class="flow-line h-8"></div>
                    <div class="bg-white border-2 border-teal-500 p-6 rounded-lg shadow-inner">
                        <h3 class="text-xl font-bold text-teal-700">Personalized Dashboard is Generated</h3>
                        <p class="text-slate-500 mt-2">The user sees exactly what they need to know, without being overwhelmed by irrelevant features. This creates a smooth, efficient, and welcoming start to their journey.</p>
                    </div>
                </div>
            </div>
        </section>
        
        <section id="dialogue-trees" class="mb-12">
            <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8">
                <h2 class="text-3xl font-bold text-sky-600 mb-4 flex items-center">
                    <span class="text-4xl mr-4">🌳</span> Dialogue Trees & Flows
                </h2>
                <p class="text-slate-600 mb-8 text-lg">
                    To guide users through specific tasks, applications often use dialogue trees. These are essentially pre-written scripts that map out a conversation. While effective for simple, predictable workflows like booking an appointment or answering FAQs, they lack the flexibility to handle the unpredictable nature of human conversation.
                </p>
                
                <div class="flex flex-col items-center p-4">
                    <div class="bg-sky-100 text-sky-800 rounded-lg p-4 font-bold shadow-sm mb-4">Node: "What subject do you need help with?"</div>
                    <div class="w-full flex justify-center items-stretch h-20">
                        <div class="border-l-2 border-t-2 border-teal-500 w-1/3 rounded-tl-xl"></div>
                        <div class="border-t-2 border-teal-500 w-px"></div>
                        <div class="border-r-2 border-t-2 border-teal-500 w-1/3 rounded-tr-xl"></div>
                    </div>
                    <div class="w-full grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
                        <div class="bg-slate-100 p-4 rounded-lg shadow-sm">
                            <p class="font-bold text-teal-700">Branch: Math</p>
                            <p class="text-slate-500 text-sm">Leads to math tutors.</p>
                        </div>
                         <div class="bg-slate-100 p-4 rounded-lg shadow-sm">
                            <p class="font-bold text-teal-700">Branch: Science</p>
                            <p class="text-slate-500 text-sm">Leads to science tutors.</p>
                        </div>
                         <div class="bg-slate-100 p-4 rounded-lg shadow-sm">
                            <p class="font-bold text-teal-700">Branch: English</p>
                            <p class="text-slate-500 text-sm">Leads to English tutors.</p>
                        </div>
                    </div>
                    <div class="mt-8 bg-amber-100 border-l-4 border-amber-500 text-amber-800 p-4 rounded-r-lg w-full max-w-md">
                        <p><span class="font-bold">Challenge:</span> This rigid structure fails when a user asks something unexpected, like "My homework on fractions is too hard." It can't understand intent, only keywords.</p>
                    </div>
                </div>
            </div>
        </section>

        <section id="ai-agent" class="mb-12">
            <div class="bg-white rounded-2xl shadow-lg p-6 md:p-8">
                 <h2 class="text-3xl font-bold text-sky-600 mb-4 flex items-center">
                    <span class="text-4xl mr-4">🧠</span> AI Agent Matching System
                </h2>
                <p class="text-slate-600 mb-8 text-lg">
                    This is the leap from a scripted interaction to an intelligent one. An AI agent is a smart, autonomous program that doesn't just follow a script—it perceives its environment, makes complex decisions, and acts to achieve a goal. For matching students and tutors, it's like having a tireless, expert matchmaker working 24/7.
                </p>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
                    <div class="relative flex items-center justify-center h-80">
                       <div class="absolute w-40 h-40 bg-sky-500 text-white rounded-full flex flex-col items-center justify-center text-center p-4 shadow-2xl z-10">
                           <p class="font-black text-2xl">AI Agent</p>
                           <p class="text-xs">The Core</p>
                       </div>

                       <div class="absolute top-1/2 left-1/2 w-72 h-72">
                            <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-48 h-48 rounded-full border-2 border-dashed border-slate-300"></div>
                            <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-72 h-72 rounded-full border-2 border-dashed border-slate-300"></div>
                            <div class="absolute top-1/2 left-1/2 w-36 h-0.5 radial-line" style="transform: rotate(0deg) translateX(10px);"></div>
                            <div class="absolute top-1/2 left-1/2 w-36 h-0.5 radial-line" style="transform: rotate(120deg) translateX(10px);"></div>
                            <div class="absolute top-1/2 left-1/2 w-36 h-0.5 radial-line" style="transform: rotate(240deg) translateX(10px);"></div>

                           <div class="absolute top-1/2 left-1/2 transform -translate-y-1/2" style="transform: translate(100px, -110px);">
                               <div class="bg-teal-100 text-teal-800 p-3 rounded-lg shadow-md text-center">
                                   <p class="font-bold">Perception</p>
                                   <p class="text-xs">Gathers data</p>
                               </div>
                           </div>
                           <div class="absolute top-1/2 left-1/2 transform -translate-y-1/2" style="transform: translate(100px, 110px);">
                               <div class="bg-teal-100 text-teal-800 p-3 rounded-lg shadow-md text-center">
                                   <p class="font-bold">Action</p>
                                   <p class="text-xs">Connects users</p>
                               </div>
                           </div>
                           <div class="absolute top-1/2 left-1/2 transform -translate-x-full -translate-y-1/2" style="transform: translateX(-190px);">
                               <div class="bg-teal-100 text-teal-800 p-3 rounded-lg shadow-md text-center">
                                   <p class="font-bold">Decision</p>
                                   <p class="text-xs">Finds best match</p>
                               </div>
                           </div>
                       </div>
                    </div>

                    <div>
                        <h3 class="font-bold text-xl text-slate-800 mb-4">Why is an AI Agent Superior?</h3>
                        <p class="text-slate-600 mb-6">
                            An AI agent transcends the limitations of dialogue trees by handling complexity and ambiguity. It learns from every interaction to continuously improve its matching algorithm.
                        </p>
                        <div class="chart-container">
                            <canvas id="aiEffectivenessChart"></canvas>
                        </div>
                        <p class="text-center text-sm text-slate-500 mt-2">Represents the high success rate of AI-powered matching in finding a compatible and effective tutor.</p>
                    </div>
                </div>
            </div>
        </section>
    </main>
    
    <footer class="text-center mt-12 text-slate-500 text-sm">
        <p>Infographic created to demonstrate modern application design principles.</p>
    </footer>

</div>

<script>
    function wrapLabels(label) {
        const max = 16;
        if (typeof label !== 'string' || label.length <= max) {
            return label;
        }
        const words = label.split(' ');
        const lines = [];
        let currentLine = '';
        for (const word of words) {
            if ((currentLine + ' ' + word).trim().length > max) {
                lines.push(currentLine.trim());
                currentLine = word;
            } else {
                currentLine = (currentLine + ' ' + word).trim();
            }
        }
        if (currentLine) {
            lines.push(currentLine.trim());
        }
        return lines;
    }

    const tooltipTitleCallback = (tooltipItems) => {
        const item = tooltipItems[0];
        let label = item.chart.data.labels[item.dataIndex];
        if (Array.isArray(label)) {
          return label.join(' ');
        }
        return label;
    };
    
    const aiEffectivenessCtx = document.getElementById('aiEffectivenessChart').getContext('2d');
    new Chart(aiEffectivenessCtx, {
        type: 'doughnut',
        data: {
            labels: ['Successful Matches', 'Mismatches'],
            datasets: [{
                label: 'Match Success Rate',
                data: [92, 8],
                backgroundColor: [
                    '#0ea5e9',
                    '#e2e8f0'
                ],
                borderColor: [
                    '#ffffff',
                    '#ffffff'
                ],
                borderWidth: 4,
                hoverOffset: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                       color: '#475569',
                       font: {
                           size: 14
                       }
                    }
                },
                tooltip: {
                    callbacks: {
                        title: tooltipTitleCallback
                    },
                    backgroundColor: '#1e293b',
                    titleFont: { size: 16 },
                    bodyFont: { size: 14 },
                    padding: 12,
                    cornerRadius: 8,
                    displayColors: false
                }
            }
        }
    });
</script>
```

</body>
</html>
