(function() {
    const startTime = Date.now();
    let clickCount = 0;

    document.addEventListener("click", () => {
        clickCount++;
        localStorage.setItem("clickCount", clickCount);
    });

    window.addEventListener("beforeunload", function() {
        const timeSpent = Date.now() - startTime;
        const userId = localStorage.getItem("userId") || `guest_${Math.random().toString(36).substring(7)}`;

        fetch("http://localhost:8000/track", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                userId: userId,
                clicks: clickCount,
                timeSpent: timeSpent,
                visits: Number(localStorage.getItem("visits") || 0) + 1
            }),
        });

        localStorage.setItem("visits", Number(localStorage.getItem("visits") || 0) + 1);
    });
})();