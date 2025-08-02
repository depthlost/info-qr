const toastCategories = {
    success: {
        colorClass: 'text-success',
        iconClass: 'bi-check-circle-fill',
        title: 'Éxito'
    },
    error: {
        colorClass: 'text-danger',
        iconClass: 'bi-x-circle-fill',
        title: 'Error'
    },
    info: {
        colorClass: 'text-info',
        iconClass: 'bi-info-circle-fill',
        title: 'Información'
    },
    warning: {
        colorClass: 'text-warning',
        iconClass: 'bi-exclamation-triangle-fill',
        title: 'Advertencia'
    }
}

function showToast(message, type, delay = 5000) {
    const category = toastCategories[type] || toastCategories.info

    const toastHtml = `
    <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header">
        <i class="${category.iconClass} ${category.colorClass} me-2"></i>
        <strong class="me-auto">${category.title}</strong>
        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Cerrar"></button>
        </div>
        <div class="toast-body"></div>
    </div>`

    const container = document.getElementById('toastContainer')
    container.insertAdjacentHTML('beforeend', toastHtml)

    const toast = container.lastElementChild
    const options = delay > 0 ? { delay, autohide: true } : { autohide: false }
    
    toast.querySelector(".toast-body").textContent = message
    
    const bootstrapToast = new bootstrap.Toast(toast, options);
    bootstrapToast.show();

    toast.addEventListener('hidden.bs.toast', () => { toast.remove() })
}
