let page = 2;
let isLoading = false;

const sentinel = document.getElementById('sentinel');
const observer = new IntersectionObserver((entries) => {
    // Проверяем, что элемент виден и не идет уже загрузка
    if (entries[0].isIntersecting && !isLoading) {
        loadMorePosts();
    }
}, {threshold: 0.1}); // Уменьшим threshold для более раннего срабатывания

observer.observe(sentinel);

function loadMorePosts() {
    isLoading = true;

    fetch(`?page=${page}`)
        .then(response => response.text())
        .then(html => {
            if (html.trim()) {
                document.getElementById('posts-container').insertAdjacentHTML('beforeend', html);
                page++;
                isLoading = false;
            } else {
                // Если больше нет постов, прекращаем наблюдение
                observer.unobserve(sentinel);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            isLoading = false;
        });
}