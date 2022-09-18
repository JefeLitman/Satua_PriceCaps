// Version 1.1
sleep = (ms) => {
    return new Promise(resolve => setTimeout(resolve, ms));
}

fade_in = async (element) => {
    element.classList.add("fade");
    await sleep(300);
    element.classList.remove("d-none");
    element.classList.add("show");
}

fade_out = async (element) => {
    element.classList.add("fade");
    await sleep(300);
    element.classList.add("d-none");
}

fade = async (out_element, in_element) => {    
    out_element.classList.add("fade");
    in_element.classList.add("fade");
    await sleep(300); // Time required for bootstrap to make fade animation is 150 so we use the double
    out_element.classList.add("d-none");
    in_element.classList.remove("d-none");
    await sleep(300);
    in_element.classList.add("show");
}