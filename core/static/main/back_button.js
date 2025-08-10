

function isSafeUrl(url, base) {
  if (!url) return false;
  try {
    const parsed = new URL(url, base);
    return parsed.hostname === window.location.hostname || url.startsWith('/');
  } catch {
    return false;
  }
}

function handleBackButton(event) {
  event.preventDefault();
  const target = event.currentTarget;
  const currentUrl = window.location.href;
  const fallbackUrl = target.getAttribute('href') || target.getAttribute('data-href') || '/';


  if (!isSafeUrl(fallbackUrl, currentUrl)) {
    window.location.href = '/';
    return;
  }


  if (window.history.length > 1) {
    try {
      window.history.back();

      // Fallback на случай, если переход не произошел
      setTimeout(() => {
        if (window.location.href === currentUrl) {
          window.location.href = fallbackUrl;
        }
      }, 500);
    } catch (e) {
      window.location.href = fallbackUrl;
    }
  } else {
    window.location.href = fallbackUrl;
  }
}


let isInitialized = false;
function initBackButtons() {
  if (isInitialized) return;
  isInitialized = true;

  document.querySelectorAll('.back-link').forEach(button => {
    button.removeEventListener('click', handleBackButton);
    button.addEventListener('click', handleBackButton);
  });
}


document.addEventListener('DOMContentLoaded', initBackButtons);


if (typeof MutationObserver !== 'undefined') {
  new MutationObserver(initBackButtons).observe(document.body, {
    childList: true,
    subtree: true
  });
}