window.addEventListener('DOMContentLoaded', () => {
    const postsContainer = document.getElementById('posts-container');
    if (postsContainer) {
        const lastNewsId = postsContainer.dataset.lastNewsId;
        if (lastNewsId) {
            const element = document.getElementById(`post-${lastNewsId}`);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    }
});