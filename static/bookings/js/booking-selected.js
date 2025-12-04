function selectBooking(element) {
    // Remove selected class from all cards
    document.querySelectorAll(".booking-card-item").forEach((card) => {
        card.classList.remove("booking-card-selected");
    });
    // Add selected class to clicked card
    element.classList.add("booking-card-selected");

    // Update visuals
    document.getElementById("detail-shop-img").src = element.dataset.shopImg;
    document.getElementById("detail-shop-name").textContent = element.dataset.shopName;
    document.getElementById("detail-shop-address").textContent = element.dataset.shopAddress;
    document.getElementById("detail-shop-description").textContent = element.dataset.shopDescription;
    document.getElementById("detail-shop-phone").textContent = element.dataset.shopPhone;

    document.getElementById("detail-service-name").textContent = element.dataset.serviceName;
    document.getElementById("detail-service-price").textContent = element.dataset.servicePrice;
    document.getElementById("detail-date-day").textContent = element.dataset.dateDay;
    document.getElementById("detail-date-month").textContent = element.dataset.dateMonth;
    document.getElementById("detail-date-time").textContent = element.dataset.dateTime;
    document.getElementById("detail-barbershop-row-name").textContent = element.dataset.shopName;

    // Status Badge
    const statusBadge = document.getElementById("detail-status-badge");
    const status = element.dataset.status;
    statusBadge.textContent = element.dataset.statusDisplay;

    statusBadge.classList.remove("badge-confirmed", "badge-finished");
    if (status === "CONFIRMADO") {
        statusBadge.classList.add("badge-confirmed");
    } else {
        statusBadge.classList.add("badge-finished");
    }

    // Cancel Form
    const cancelForm = document.getElementById("detail-cancel-form");
    if (status === "CONFIRMADO") {
        cancelForm.style.display = "block";
        cancelForm.action = element.dataset.cancelUrl;
    } else {
        cancelForm.style.display = "none";
    }
}

function copyToClipboard(elementId) {
    const text = document.getElementById(elementId).textContent;
    navigator.clipboard.writeText(text).then(() => {
        // Optional: Show a tooltip or simple alert
        // alert('Copiado!');
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const ratingModal = document.getElementById("ratingModal");

    ratingModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;
        const barbershopId = button.getAttribute("data-barbershop-id");
        const barbershopName = button.getAttribute("data-barbershop-name");

        const modalIdInput = ratingModal.querySelector("#modalBarbershopId");
        const modalNameTitle = ratingModal.querySelector("#modalBarbershopName");

        modalIdInput.value = barbershopId;
        modalNameTitle.textContent = barbershopName;

        // Reset stars
        resetStars();
    });

    // Star rating logic
    const stars = document.querySelectorAll(".star-icon");
    const ratingInput = document.getElementById("ratingValue");

    stars.forEach((star) => {
        star.addEventListener("click", function () {
            const value = this.getAttribute("data-value");
            ratingInput.value = value;
            updateStars(value);
        });

        star.addEventListener("mouseover", function () {
            const value = this.getAttribute("data-value");
            highlightStars(value);
        });

        star.addEventListener("mouseout", function () {
            const currentValue = ratingInput.value;
            if (currentValue) {
                updateStars(currentValue);
            } else {
                resetStars();
            }
        });
    });

    function updateStars(value) {
        stars.forEach((s) => {
            if (s.getAttribute("data-value") <= value) {
                s.classList.remove("bi-star");
                s.classList.add("bi-star-fill");
                s.style.color = "#facc15"; // Yellow
            } else {
                s.classList.remove("bi-star-fill");
                s.classList.add("bi-star");
                s.style.color = ""; // Reset
            }
        });
    }

    function highlightStars(value) {
        stars.forEach((s) => {
            if (s.getAttribute("data-value") <= value) {
                s.classList.remove("bi-star");
                s.classList.add("bi-star-fill");
                s.style.color = "#facc15";
            } else {
                s.classList.remove("bi-star-fill");
                s.classList.add("bi-star");
                s.style.color = "";
            }
        });
    }

    function resetStars() {
        stars.forEach((s) => {
            s.classList.remove("bi-star-fill");
            s.classList.add("bi-star");
            s.style.color = "";
        });
    }
});
