document.addEventListener('DOMContentLoaded', function() {
    const postsContainer = document.getElementById('posts-container');
    const loadingElement = document.getElementById('loading');
    let page = 2;
    let isLoading = false;
    let hasMore = true;

    async function loadPosts() {
        if (isLoading || !hasMore) return;

        isLoading = true;
        loadingElement.style.display = 'block';

        try {
            const response = await fetch(`/api/posts/?page=${page}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                },
                credentials: 'include'  // Для передачи сессий и куки
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Ошибка сервера');
            }

            if (data.posts_html) {
                postsContainer.insertAdjacentHTML('beforeend', data.posts_html);
                hasMore = data.has_next;
                page = data.next_page_number || page + 1;

                if (!hasMore) {
                    loadingElement.textContent = 'Вы достигли конца ленты';
                    window.removeEventListener('scroll', handleScroll);
                }
            }
        } catch (error) {
            console.error('Ошибка загрузки:', error);
            loadingElement.textContent = 'Ошибка загрузки. Попробуйте позже.';
            // Можно добавить кнопку повтора
        } finally {
            isLoading = false;
            setTimeout(() => {
                loadingElement.style.display = 'none';
            }, 500);
        }
    }

    // Оптимизированный обработчик скролла
    const handleScroll = () => {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 800) {
            loadPosts();
        }
    };

    // Дебаунс для оптимизации
    let scrollTimeout;
    window.addEventListener('scroll', () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(handleScroll, 100);
    });

    // Инициализация для первых постов
    loadPosts();
});