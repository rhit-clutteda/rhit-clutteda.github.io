/*
    I was rather unsure of what to do, so I decided to do something a bit odd.  I found that one
    might want to zoom into my larger fractal image, so I added a way to zoom in by reading the value from
    a slider and multiplying the width of the image by that value.

    It's kind of stupid, but oddly fun.
*/

// Set element variables
let zoomSlider = document.querySelector('.zoom-slider');
let input = document.querySelector('#zoom-slider-input');
let image = document.querySelector('.zoom-image')

// listen for inputs and update
input.addEventListener('input', () => {
  zoomSlider.style.setProperty('--slider-value', `${input.value}%`);
  console.log(input.value)
  console.log()
  image.style.width = Math.max(10, input.value * 10)
});

zoomSlider.style.setProperty('--slider-value', `${input.value}%`);