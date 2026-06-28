document.addEventListener("DOMContentLoaded", () => {
    const chatContainer = document.getElementById("chat-container");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-btn");
    const menuButtons = document.querySelectorAll(".menu-btn");
    
    // Global variable to keep track of generated chart instances
    const activeCharts = {};

    // 1. Event listener for clicking menu buttons
    menuButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const query = btn.getAttribute("data-query");
            if (query) {
                sendMessage(query);
            }
        });
    });

    // 2. Event listener for sending message
    sendButton.addEventListener("click", () => {
        handleSend();
    });

    userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            handleSend();
        }
    });

    function handleSend() {
        const text = userInput.value.trim();
        if (text) {
            sendMessage(text);
            userInput.value = "";
        }
    }

    // 3. Main Fetch Function - sends request to backend API
    async function sendMessage(queryText) {
        // Render User Message
        appendMessage("user", queryText);

        // Render loading state indicator
        const loadingId = appendLoadingIndicator();

        try {
            const formData = new FormData();
            formData.append("message", queryText);

            // Fetch backend response
            const response = await fetch("http://localhost:8000/api/chat", {
                method: "POST",
                body: formData
            });

            // Remove loading indicator
            removeLoadingIndicator(loadingId);

            if (response.ok) {
                const data = await response.json();
                
                // Render Assistant Response
                appendMessage("assistant", data.text, data.sql, data.chart, data.tool_used);
            } else {
                appendMessage("assistant", "Error: Backend returned a non-ok status code.");
            }
        } catch (error) {
            console.warn("Backend server offline. Running local fallback parser...");
            removeLoadingIndicator(loadingId);
            
            // Execute Local Fallback if server is offline
            handleLocalFallback(queryText);
        }
    }

    // 4. Local Fallback Mock Handler (for offline demo capability)
    function handleLocalFallback(queryText) {
        const q = queryText.toLowerCase();
        let text = "Processed successfully via local backup parser matrix.";
        let sql = "SELECT * FROM dataset_feed LIMIT 5;";
        let chart = null;
        let tool = "EXPLAIN_DATA";

        if (q.includes("product")) {
            tool = "GENERATE_CHART";
            text = "Calculated top performing inventory items filtered by overall gross sales volumes:";
            sql = "SELECT product_name, SUM(revenue) FROM sales GROUP BY product_name ORDER BY 2 DESC LIMIT 5;";
            chart = {
                type: 'bar',
                labels: ['SaaS Engine', 'Hardware Kits', 'Cloud Services', 'Support Desk', 'Consulting'],
                datasets: [{ 
                    label: 'Revenue ($)', 
                    data: [124000, 98000, 85000, 43000, 29000], 
                    backgroundColor: '#3b82f6' 
                }]
            };
        } 
        else if (q.includes("city") || q.includes("customer")) {
            tool = "GENERATE_CHART";
            text = "Demographic geographic breakdown mapping user retention concentrations across regional centers:";
            sql = "SELECT registration_city, COUNT(id) FROM users GROUP BY registration_city ORDER BY 2 DESC;";
            chart = {
                type: 'pie',
                labels: ['Mumbai', 'Chennai', 'Bangalore'],
                datasets: [{ 
                    data: [580, 410, 230], 
                    backgroundColor: ['#ef4444', '#3b82f6', '#10b981'] 
                }]
            };
        } 
        else if (q.includes("trend") || q.includes("monthly")) {
            tool = "GENERATE_CHART";
            text = "Compiled chronological transaction volumes mapped sequentially across active operational quarters:";
            sql = "SELECT order_month, COUNT(id) FROM orders GROUP BY order_month ORDER BY order_month ASC;";
            chart = {
                type: 'line',
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{ 
                    label: 'Order Velocity', 
                    data: [150, 320, 280, 610, 780, 1100], 
                    borderColor: '#10b981', 
                    backgroundColor: 'rgba(16, 185, 129, 0.1)', 
                    tension: 0.3 
                }]
            };
        } 
        else if (q.includes("revenue") || q.includes("total")) {
            tool = "EXECUTE_QUERY";
            text = "🎯 Core Financial Computation Complete:\n\n• Total Accumulated Gross Revenue: $379,000.00\n• Active Transacting Accounts: 1,220\n• Baseline System Auditing Integrity: 100%";
            sql = "SELECT SUM(payment_amount) AS total_revenue FROM transactions WHERE status = 'SUCCESS';";
        } 
        else if (q.includes("diagram") || q.includes("er")) {
            tool = "GENERATE_FLOWCHART";
            text = "🗺️ Dynamic Entity-Relationship Database Mapping Layout:\n\n[CUSTOMERS] 1 ─── 🔑 places ─── ♾️ [ORDERS]\n[ORDERS]    1 ─── 📦 includes ─── ♾️ [LINE_ITEMS]\n[PRODUCTS]  1 ─── 🏷️ populates ─── ♾️ [LINE_ITEMS]";
            sql = "SELECT table_name, column_name FROM information_schema.columns WHERE table_schema = 'public';";
        }
        
        // --- NEW GENERAL KNOWLEDGE FALLBACKS ---
        else if (q.includes("what is ai") || q.includes("artificial intelligence")) {
            text = "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think, reason, and learn like humans. Examples include speech recognition, decision-making, and visual perception.";
            sql = null;
        }
        else if (q.includes("what is ml") || q.includes("machine learning")) {
            text = "Machine Learning (ML) is a subset of Artificial Intelligence (AI) that enables systems to learn from data, identify complex patterns, and make automated decisions with minimal human intervention.";
            sql = null;
        }
        else if (q.includes("ipl") || q.includes("latest ipl winner")) {
            text = "The latest winner of the Indian Premier League (IPL) is the Kolkata Knight Riders (KKR), who defeated Sunrisers Hyderabad in the 2024 IPL Final.";
            sql = null;
        }
        else if (q.includes("cm of tamilnadu") || q.includes("cm of tamil nadu")) {
            text = "The current Chief Minister of Tamil Nadu is M. K. Stalin.";
            sql = null;
        }
        else if (q.includes("pm of india") || q.includes("prime minister of india") || q.includes("m of india")) {
            text = "The current Prime Minister of India is Narendra Modi.";
            sql = null;
        }
        else if (q.includes("longest road")) {
            text = "The longest road in India is National Highway 44 (NH 44). It spans over 4,112 kilometers, running from Srinagar in the north to Kanyakumari in the south.";
            sql = null;
        }
        else {
            text = `Ollama LLM Agent is currently offline.\n\nTroubleshooting Tip:\nTo query general knowledge dynamically, please run Ollama server on your machine using: \n"ollama run deepseek-r1:7b".`;
            sql = null;
            tool = "EXPLAIN_DATA";
        }

        appendMessage("assistant", text, sql, chart, tool);
    }

    // 5. Append message bubble to UI
    function appendMessage(role, text, sql = null, chart = null, tool = null) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", role);

        const avatar = document.createElement("div");
        avatar.classList.add("avatar");
        avatar.textContent = role === "user" ? "U" : "🤖";

        const contentDiv = document.createElement("div");
        contentDiv.classList.add("message-content");

        // Tool tag
        if (tool) {
            const toolTag = document.createElement("span");
            toolTag.classList.add("tool-tag");
            toolTag.textContent = tool;
            contentDiv.appendChild(toolTag);
        }

        // Message text
        const textElement = document.createElement("p");
        textElement.innerHTML = text.replace(/\n/g, "<br>");
        contentDiv.appendChild(textElement);

        // Render Chart.js Canvas
        if (chart) {
            const chartDiv = document.createElement("div");
            chartDiv.classList.add("chart-container");
            
            const canvas = document.createElement("canvas");
            const canvasId = `chart-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
            canvas.setAttribute("id", canvasId);
            
            chartDiv.appendChild(canvas);
            contentDiv.appendChild(chartDiv);

            // Instantiate Chart.js dynamically
            setTimeout(() => {
                const ctx = document.getElementById(canvasId).getContext("2d");
                
                // Clear any existing instance on this canvas ID
                if (activeCharts[canvasId]) {
                    activeCharts[canvasId].destroy();
                }
                
                activeCharts[canvasId] = new Chart(ctx, {
                    type: chart.type || 'bar',
                    data: {
                        labels: chart.labels,
                        datasets: chart.datasets
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                labels: {
                                    color: '#94a3b8' // text-muted
                                }
                            }
                        },
                        scales: chart.type !== 'pie' ? {
                            x: {
                                ticks: { color: '#94a3b8' },
                                grid: { color: 'rgba(51, 65, 85, 0.2)' }
                            },
                            y: {
                                ticks: { color: '#94a3b8' },
                                grid: { color: 'rgba(51, 65, 85, 0.2)' }
                            }
                        } : {}
                    }
                });
            }, 50);
        }

        // Render SQL Code Block
        if (sql) {
            const sqlDiv = document.createElement("div");
            sqlDiv.classList.add("sql-container");

            const sqlTitle = document.createElement("div");
            sqlTitle.classList.add("sql-title");
            sqlTitle.textContent = "Generated Action SQL Query";

            const pre = document.createElement("pre");
            pre.textContent = sql;

            sqlDiv.appendChild(sqlTitle);
            sqlDiv.appendChild(pre);
            contentDiv.appendChild(sqlDiv);
        }

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(contentDiv);
        chatContainer.appendChild(messageDiv);

        // Scroll to bottom
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Helper functions for loading indicator
    function appendLoadingIndicator() {
        const id = `loading-${Date.now()}`;
        const loadDiv = document.createElement("div");
        loadDiv.setAttribute("id", id);
        loadDiv.classList.add("message", "assistant");
        
        loadDiv.innerHTML = `
            <div class="avatar">🤖</div>
            <div class="message-content" style="font-style: italic; color: #94a3b8;">
                Analyzing data metrics...
            </div>
        `;
        chatContainer.appendChild(loadDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        return id;
    }

    function removeLoadingIndicator(id) {
        const loader = document.getElementById(id);
        if (loader) {
            loader.remove();
        }
    }
});