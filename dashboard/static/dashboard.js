// Real-Time Dashboard

let netSentHistory = [];
let netRecvHistory = [];
let lastNetSent = null;
let lastNetRecv = null;
let timeHistory = [];
let cpuHistory = [];
let memoryHistory = [];
let diskHistory = [];

const MAX_POINTS = 30;

async function fetchLatest(){
    const response = await fetch("/api/latest");
    return await response.json();
}

function formatUptime(seconds) {
    const days = Math.floor(seconds / 86400);
    seconds %= 86400;
    const hours = Math.floor(seconds / 3600);
    seconds %= 3600;
    const minutes = Math.floor(seconds / 60);
    return `${days}d ${hours}h ${minutes}m`;
}

function updateCharts(data) {
    let sentRate = 0;
    let recvRate = 0;

    if(lastNetSent !== null){
        sentRate = (data.net_sent - lastNetSent) / 1024;
        recvRate = (data.net_recv - lastNetRecv) / 1024;

        if(sentRate < 0) sentRate = 0;
        if(recvRate < 0) recvRate = 0;
    }

    lastNetSent = data.net_sent;
    lastNetRecv = data.net_recv;

    timeHistory = [...timeHistory, new Date().toLocaleTimeString()];
    cpuHistory = [...cpuHistory, data.cpu];
    memoryHistory = [...memoryHistory, data.memory];
    diskHistory = [...diskHistory, data.disk];
    netSentHistory = [...netSentHistory, sentRate];
    netRecvHistory = [...netRecvHistory, recvRate];

    if(timeHistory.length > MAX_POINTS){
        netSentHistory.shift();
        netRecvHistory.shift();
        timeHistory.shift();
        cpuHistory.shift();
        memoryHistory.shift();
        diskHistory.shift();
    }

    Plotly.react("netChart", [
    {
        x: timeHistory,
        y: netSentHistory,
        type: "scatter",
        mode: "lines+markers",
        name: "Sent KB/s",
        line: { color: "#FF5722" }
    },
    {
        x: timeHistory,
        y: netRecvHistory,
        type: "scatter",
        mode: "lines+markers",
        name: "Recv KB/s",
        line: { color: "#03A9F4" }
    }
    ], {
        title: "Network Usage (KB/s)",
        yaxis: {
            rangemode: "tozero",
            autorange: false,
            range: [0, 300]
        }
    });

    Plotly.react("cpuChart", [{
        x: timeHistory,
        y: cpuHistory,
        type: "scatter",
        mode: "lines+markers",
        line: { color: "#4CAF50" }
    }], { title: "CPU Usage (%)"});

    Plotly.react("memoryChart", [{
        x: timeHistory,
        y: memoryHistory,
        type: "scatter",
        mode: "lines+markers",
        line: { color: "#2196F3" }
    }], { title: "Memory Usage (%)" });

    Plotly.react("diskChart", [{
        x: timeHistory,
        y: diskHistory,
        type: "scatter",
        mode: "lines+markers",
        line: { color: "#FFC107" }
    }], { title: "Disk Usage (%)" });
}

async function refresh() {
    const data = await fetchLatest();
    document.getElementById("uptime").textContent =
        "Uptime: " + formatUptime(data.uptime);
    updateCharts(data);
}

setInterval(refresh, 2000);
refresh();