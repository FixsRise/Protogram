document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('deleteModal');
    if (!modal) return;

    const deleteForm = modal.querySelector('form');

    document.body.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-btn')) {
            e.preventDefault();
            const postId = e.target.dataset.postId;
            const deleteUrl = e.target.dataset.postUrl;

            if (deleteForm) {
                deleteForm.action = deleteUrl;
                const input = deleteForm.querySelector('input[name="post_id"]');
                if (input) input.value = postId;
            }

            modal.style.display = 'block';
        }
    });

    const closeModal = () => modal.style.display = 'none';

    if (modal.querySelector('.close')) {
        modal.querySelector('.close').addEventListener('click', closeModal);
    }

    if (modal.querySelector('.cancel-btn')) {
        modal.querySelector('.cancel-btn').addEventListener('click', closeModal);
    }

    window.addEventListener('click', (e) => e.target === modal && closeModal());
});