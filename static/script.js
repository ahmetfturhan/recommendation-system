let cardContainers = [...document.querySelectorAll('.card_container')];
let preBtns = [...document.querySelectorAll('.pre-btn')];
let nextBtns = [...document.querySelectorAll('.nxt-btn')];

cardContainers.forEach((item, i) => {
    let containerDimensions = item.getBoundingClientRect();
    let containerWidth = containerDimensions.width;

    nextBtns[i].addEventListener('click', () => {
        item.scrollLeft += containerWidth/2;

    })

    preBtns[i].addEventListener('click', () => {
        item.scrollLeft -= containerWidth/2;
    })
})


