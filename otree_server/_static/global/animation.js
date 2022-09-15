fade = (element, time, direction) => {
    if (direction === "in"){
        element.style.opacity = 0;
        element.classList.remove("d-none");
    }
    else{
        element.style.opacity = 1;
    }

    let last = +Date.now();
    let tick = function() {
        let delta = direction === "in" ? (Date.now() - last) : -(Date.now() - last);
        element.style.opacity = +element.style.opacity + (delta / time);
        last = +Date.now();

        let comparison = direction === "in" ? +element.style.opacity < 1 : +element.style.opacity > 0;
        if (comparison) {
            (window.requestAnimationFrame && requestAnimationFrame(tick)) || setTimeout(tick, 16);
        }
        else{
            if (direction === "out"){
                element.classList.add("d-none");
            }
        }
    };

    tick();
}