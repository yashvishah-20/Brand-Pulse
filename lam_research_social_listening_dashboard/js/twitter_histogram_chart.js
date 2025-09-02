// Twitter Histogram Chart for Audience Insights
// This script expects a JSON file with keys: views, likes, retweets, replies

async function loadTwitterHistogramChart() {
        // Also update Twitter quick stats if present
        if (document.getElementById('twitterTotalPosts')) {
            document.getElementById('twitterTotalPosts').textContent = data.total_posts?.toLocaleString?.() || 'N/A';
        }
        if (document.getElementById('twitterAvgEngagement')) {
            document.getElementById('twitterAvgEngagement').textContent = data.avg_engagement?.toLocaleString?.() || 'N/A';
        }
        if (document.getElementById('twitterTotalEngagements')) {
            document.getElementById('twitterTotalEngagements').textContent = data.total_engagements?.toLocaleString?.() || 'N/A';
        }
        if (document.getElementById('twitterTopReaction')) {
            document.getElementById('twitterTopReaction').textContent = data.top_reaction || 'N/A';
        }
    try {
        const response = await fetch('../public/twitter_histogram_data.json');
        if (!response.ok) throw new Error('Failed to load twitter_histogram_data.json');
        const data = await response.json();
        const ctx = document.getElementById('twitterHistogramChart');
        if (!ctx) return;
        // Remove previous chart if exists
        if (window.twitterHistogramChartInstance) {
            window.twitterHistogramChartInstance.destroy();
        }
        // Set the counts in the boxes below the chart
        if (document.getElementById('twitterViewsCount')) {
            document.getElementById('twitterViewsCount').textContent = data.views?.toLocaleString() || '-';
        }
        if (document.getElementById('twitterLikesCount')) {
            document.getElementById('twitterLikesCount').textContent = data.likes?.toLocaleString() || '-';
        }
        if (document.getElementById('twitterRetweetsCount')) {
            document.getElementById('twitterRetweetsCount').textContent = data.retweets?.toLocaleString() || '-';
        }
        if (document.getElementById('twitterRepliesCount')) {
            document.getElementById('twitterRepliesCount').textContent = data.replies?.toLocaleString() || '-';
        }
        const labels = ['Views', 'Likes', 'Retweets', 'Replies'];
        const values = [data.views, data.likes, data.retweets, data.replies];
        const colors = ['#3498DB', '#FF6B35', '#27AE60', '#F39C12'];
        window.twitterHistogramChartInstance = new Chart(ctx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Total',
                    data: values,
                    backgroundColor: colors,
                    borderRadius: 8,
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.parsed.y?.toLocaleString?.() || context.parsed.y}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: '#374151', font: { size: 14, weight: 'bold' } }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: '#E5E7EB' },
                        ticks: { color: '#6B7280', font: { size: 12 } }
                    }
                },
                animation: {
                    duration: 1200,
                    easing: 'easeInOutQuart'
                }
            }
        });
    } catch (e) {
        const ctx = document.getElementById('twitterHistogramChart');
        if (ctx) {
            ctx.parentNode.innerHTML = '<div class="text-center text-warning-700">Unable to load Twitter histogram data.</div>';
        }
    }
}

// Call this in initializeCharts('twitter')
