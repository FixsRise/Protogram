function getCookie(name) {
    if (!/^[a-zA-Z0-9_-]+$/.test(name)) {
        console.error('Invalid cookie name');
        return null;
    }

    const cookieString = document.cookie;
    if (!cookieString) return null;


    const cookies = Object.fromEntries(
        cookieString.split(';')
            .map(c => c.trim().split('=', 2))
            .filter(([k]) => k)
    );

    return cookies[name] ? decodeURIComponent(cookies[name]) : null;
}

function handleLikeClick(event) {
    const likeBtn = event.target.closest('.like-btn');
    if (!likeBtn || likeBtn.disabled) return;

    const postId = likeBtn.dataset.postId;
    if (!/^\d+$/.test(postId)) {
        console.error('Invalid post ID');
        return;
    }

    const isLiked = likeBtn.classList.contains('liked');
    const likeCountEl = likeBtn.querySelector('.like-count');


    likeBtn.disabled = true;
    likeBtn.style.opacity = '0.7';

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    fetch(`/posts/${postId}/like/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') || '',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            action: isLiked ? 'unlike' : 'like'
        }),
        signal: controller.signal
    })
    .then(response => {
        clearTimeout(timeoutId);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error('Invalid response type');
        }

        return response.json();
    })
    .then(data => {
        if (data && data.status === 'ok') {
            likeBtn.classList.toggle('liked');
            if (likeCountEl && typeof data.likes_count !== 'undefined') {
                likeCountEl.textContent = data.likes_count;
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (error.name !== 'AbortError') {
            showToast('Error during handling likes', 'error');
        }
    })
    .finally(() => {
        likeBtn.disabled = false;
        likeBtn.style.opacity = '1';
    });
}


let likeHandlerInitialized = false;
function initLikeHandler() {
    if (likeHandlerInitialized) return;
    likeHandlerInitialized = true;

    document.addEventListener('click', handleLikeClick);
    console.log('Like handler initialized securely');
}

document.addEventListener('DOMContentLoaded', initLikeHandler);

