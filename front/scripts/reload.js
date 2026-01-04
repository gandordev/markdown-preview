const connectWebSocket = () => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${protocol}//${window.location.host}/ws/reload`);

    ws.onopen = () => { };

    ws.onclose = () => {
        setTimeout(() => location.reload(), 1000);
    };

    ws.onerror = () => {
        setTimeout(() => location.reload(), 1000);
    };
};

// Conectar al abrir la página
connectWebSocket();