// Handles drag and arrow carousel's scroll
function handle(carouselClass, cardClass, arrowClass) {   
    const carousel = document.querySelector(carouselClass)
    const firstCardWidth = carousel.querySelector(cardClass).offsetWidth;
    const arrowBtns = document.querySelectorAll(arrowClass);
    let isDragging = false, startX, startScrollLeft;

    carousel.classList.add("no-transition");
    carousel.scrollLeft = carousel.firstCardWidth;
    carousel.classList.remove("no-transition");
    // Add event listeners for the arrow buttons to scroll the carousel left and right
    arrowBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            carousel.scrollLeft += btn.id == "left" ? -firstCardWidth : firstCardWidth;
        });
    });
    // Drag events
    const dragStart = (e) => {
        isDragging = true;
        carousel.classList.add("dragging");
        // Records the initial cursor and scroll position of the carousel
        startX = e.pageX;
        startScrollLeft = carousel.scrollLeft;
    }
    const dragging = (e) => {
        if(!isDragging) return; // if isDragging is false return from here
        // Updates the scroll position of the carousel based on the cursor movement
        carousel.scrollLeft = startScrollLeft - (e.pageX - startX);
    }
    const dragStop = () => {
        isDragging = false;
        carousel.classList.remove("dragging");
    }

    carousel.addEventListener("mousedown", dragStart);
    carousel.addEventListener("mousemove", dragging);
    document.addEventListener("mouseup", dragStop);
}

window.onload = () => {
    handle(".trends-carousel", ".trends-card", ".trends-wrapper .arrow")
    handle(".releases-carousel", ".releases-card", ".releases-wrapper .arrow")
    handle(".again-carousel", ".again-card", ".again-wrapper .arrow")
}
