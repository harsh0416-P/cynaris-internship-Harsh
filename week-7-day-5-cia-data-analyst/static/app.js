
// ==========================================
// CYNARIS CIA - AI DATA ANALYST
// Complete Frontend Controller
// ==========================================

const API_URL = "";

let sessionId = null;
let salesChart = null;

const $ = (id) => document.getElementById(id);

const fileInput = $("csvFile");
const uploadBtn = $("uploadBtn");
const analyzeBtn = $("analyzeBtn");
const questionInput = $("question");

const answerBox = $("answer");
const uploadStatus = $("uploadStatus");
const answerSource = $("answerSource");

const chartCanvas = $("salesChart");
const chartEmpty = $("chartEmpty");


// ==========================================
// THEME MANAGEMENT
// ==========================================

function applyTheme(theme) {

    document.documentElement.dataset.theme = theme;

    localStorage.setItem("cia-theme", theme);

    $("themeIcon").textContent =
        theme === "dark" ? "☀" : "☾";

    $("themeText").textContent =
        theme === "dark" ? "Light mode" : "Dark mode";

    if (salesChart) {
        updateChartTheme();
    }
}

const savedTheme = localStorage.getItem("cia-theme") || "light";

applyTheme(savedTheme);

$("themeToggle").addEventListener("click", () => {

    const current =
        document.documentElement.dataset.theme;

    applyTheme(current === "dark" ? "light" : "dark");

});


// ==========================================
// FILE SELECTION
// ==========================================

fileInput.addEventListener("change", () => {

    const file = fileInput.files[0];

    $("fileName").textContent =
        file ? `Selected: ${file.name}` : "No file selected";

});


// ==========================================
// CSV UPLOAD
// ==========================================

uploadBtn.addEventListener("click", async () => {

    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a CSV file.");
        return;
    }

    if (!file.name.toLowerCase().endsWith(".csv")) {
        alert("Only CSV files are supported.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    uploadBtn.disabled = true;
    uploadBtn.textContent = "Uploading...";

    uploadStatus.textContent = "Uploading your dataset...";

    try {

        const response = await fetch(
            `${API_URL}/cia/upload-csv`,
            {
                method: "POST",
                body: formData
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail || "Upload failed."
            );
        }

        sessionId = result.session_id;

        $("totalRows").textContent =
            Number(result.dataset_info.rows).toLocaleString();

        $("totalColumns").textContent =
            result.dataset_info.columns_count;

        const missing = Object.values(
            result.dataset_info.missing_values
        ).reduce((sum, value) => sum + value, 0);

        $("missingValues").textContent =
            missing.toLocaleString();

        uploadStatus.textContent =
            `✓ Uploaded successfully: ${result.filename}`;

        answerBox.textContent =
            "Dataset loaded successfully. Ask CIA a question.";

        answerSource.textContent = "READY";

        clearChart("Ask a question to generate a visualization.");

    } catch (error) {

        sessionId = null;

        uploadStatus.textContent =
            `Upload error: ${error.message}`;

        console.error("CSV upload error:", error);

    } finally {

        uploadBtn.disabled = false;
        uploadBtn.textContent = "Upload Dataset";

    }

});


// ==========================================
// SUGGESTED QUESTIONS
// ==========================================

document.querySelectorAll(".suggestion").forEach(button => {

    button.addEventListener("click", () => {

        questionInput.value = button.dataset.question;

        questionInput.focus();

    });

});


// ==========================================
// AI ANALYSIS
// ==========================================

analyzeBtn.addEventListener("click", analyzeDataset);

async function analyzeDataset() {

    if (!sessionId) {
        alert("Upload a CSV dataset first.");
        return;
    }

    const question = questionInput.value.trim();

    if (!question) {
        alert("Enter a question.");
        return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Analyzing...";

    answerBox.textContent =
        "CIA is analyzing your dataset. Please wait...";

    answerSource.textContent = "PROCESSING";

    clearChart("Generating visualization...");

    try {

        const response = await fetch(
            `${API_URL}/cia/analyze`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    session_id: sessionId,
                    question: question
                })
            }
        );

        const result = await response.json();

        console.log("CIA API RESPONSE:", result);

        if (!response.ok) {
            throw new Error(
                result.detail || "Analysis request failed."
            );
        }

        if (!result.success) {
            throw new Error("Analysis was unsuccessful.");
        }

        // Display answer
        answerBox.textContent =
            result.answer || "No answer returned.";

        // Display analysis engine
        answerSource.textContent =
            (result.answer_source || "UNKNOWN").toUpperCase();

        // Validate chart data
        const chartData = result.chart?.chartjs;

        console.log("CHART DATA:", chartData);

        if (
            chartData &&
            Array.isArray(chartData.labels) &&
            chartData.labels.length > 0 &&
            Array.isArray(chartData.datasets) &&
            chartData.datasets.length > 0
        ) {

            renderChart(chartData);

        } else {

            clearChart(
                "No visualization is available for this question."
            );

        }

    } catch (error) {

        console.error("Analysis error:", error);

        answerBox.textContent =
            `Analysis error: ${error.message}`;

        answerSource.textContent = "ERROR";

        clearChart("Unable to generate visualization.");

    } finally {

        analyzeBtn.disabled = false;
        analyzeBtn.textContent = "Analyze Dataset →";

    }

}


// ==========================================
// CLEAR CHART
// ==========================================

function clearChart(message = "No visualization yet.") {

    if (salesChart) {
        salesChart.destroy();
        salesChart = null;
    }

    chartCanvas.style.display = "none";

    chartEmpty.style.display = "block";

    chartEmpty.querySelector("p").textContent = message;

}


// ==========================================
// RENDER CHART
// ==========================================

function renderChart(chartData) {

    // Check Chart.js library
    if (typeof Chart === "undefined") {

        console.error("Chart.js library was not loaded.");

        clearChart(
            "Chart.js failed to load. Check your internet connection."
        );

        return;
    }

    if (!chartCanvas || !chartEmpty) {

        console.error("Chart HTML elements were not found.");

        return;
    }

    // Destroy previous chart
    if (salesChart) {
        salesChart.destroy();
        salesChart = null;
    }

    chartEmpty.style.display = "none";
    chartCanvas.style.display = "block";

    const isPie = chartData.type === "pie";

    const isDark =
        document.documentElement.dataset.theme === "dark";

    const textColor = isDark ? "#edf2ff" : "#667085";
    const gridColor = isDark ? "#354157" : "#e8ebf2";

    const palette = [
        "#5267e8",
        "#9875e8",
        "#38a6cf",
        "#24ad85",
        "#e6a44a",
        "#df7091",
        "#8292b9",
        "#f08b56",
        "#4eafbc",
        "#7892e8"
    ];

    try {

        salesChart = new Chart(
            chartCanvas.getContext("2d"),
            {
                type: chartData.type,

                data: {
                    labels: chartData.labels,

                    datasets: chartData.datasets.map(dataset => ({
                        ...dataset,

                        backgroundColor: isPie
                            ? palette
                            : "#7185ef",

                        borderColor: isPie
                            ? "#ffffff"
                            : "#5267e8",

                        borderWidth: isPie ? 2 : 0,

                        borderRadius: isPie ? 0 : 6
                    }))
                },

                options: {

                    responsive: true,

                    maintainAspectRatio: true,

                    animation: {
                        duration: 700
                    },

                    plugins: {

                        legend: {
                            display: true,
                            position: "top",

                            labels: {
                                color: textColor,
                                usePointStyle: true,
                                padding: 20
                            }
                        },

                        tooltip: {
                            enabled: true
                        }

                    },

                    scales: isPie ? {} : {

                        x: {
                            ticks: {
                                color: textColor
                            },
                            grid: {
                                color: gridColor
                            }
                        },

                        y: {
                            beginAtZero: true,

                            ticks: {
                                color: textColor
                            },

                            grid: {
                                color: gridColor
                            }
                        }

                    }

                }

            }
        );

        console.log("Chart rendered successfully.");

    } catch (error) {

        console.error("Chart rendering failed:", error);

        clearChart(
            `Chart rendering error: ${error.message}`
        );

    }

}


// ==========================================
// UPDATE CHART THEME
// ==========================================

function updateChartTheme() {

    if (!salesChart) return;

    const isDark =
        document.documentElement.dataset.theme === "dark";

    const textColor = isDark ? "#edf2ff" : "#667085";
    const gridColor = isDark ? "#354157" : "#e8ebf2";

    if (salesChart.options.plugins.legend.labels) {
        salesChart.options.plugins.legend.labels.color =
            textColor;
    }

    if (salesChart.options.scales.x) {

        salesChart.options.scales.x.ticks.color =
            textColor;

        salesChart.options.scales.x.grid.color =
            gridColor;

    }

    if (salesChart.options.scales.y) {

        salesChart.options.scales.y.ticks.color =
            textColor;

        salesChart.options.scales.y.grid.color =
            gridColor;

    }

    salesChart.update();

}


// ==========================================
// INITIALIZATION
// ==========================================

clearChart();

console.log("Cynaris CIA Dashboard initialized.");
console.log("Chart.js available:", typeof Chart !== "undefined");
