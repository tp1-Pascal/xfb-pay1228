(function() {
    function sendError(errorData) {
        const formData = new FormData();
        Object.keys(errorData).forEach(key => {
            formData.append(key, errorData[key]);
        });

        fetch('/api/log/js-error/', {
            method: 'POST',
            body: formData
        }).catch(console.error);
    }

    // 捕获 JavaScript 运行时错误
    window.onerror = function(message, source, line, column, error) {
        sendError({
            type: 'runtime',
            message: message,
            url: source,
            line: line,
            column: column,
            stack: error && error.stack
        });
        return false;
    };

    // 捕获未处理的 Promise 错误
    window.addEventListener('unhandledrejection', function(event) {
        sendError({
            type: 'promise',
            message: event.reason.message || String(event.reason),
            stack: event.reason.stack,
            url: window.location.href
        });
    });

    // 捕获资源加载错误
    window.addEventListener('error', function(event) {
        if (event.target && (event.target.tagName === 'SCRIPT' || 
            event.target.tagName === 'LINK' || 
            event.target.tagName === 'IMG')) {
            sendError({
                type: 'resource',
                message: `Failed to load ${event.target.tagName}: ${event.target.src || event.target.href}`,
                url: window.location.href
            });
        }
    }, true);
})(); 