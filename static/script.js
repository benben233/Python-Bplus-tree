window.onload = function () {
    let submitForm = false
    let submitButtonList = [].slice.call(document.querySelectorAll('[type="submit"]'))
    submitButtonList.forEach((val, index, arr) => {
        arr[index].onclick = () => {
            submitForm = true
        }
    })

    window.onbeforeunload = () => {
        if (!submitForm) {
            return "Are you sure?";
        }
    }

    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });
};