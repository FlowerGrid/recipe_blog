const calcButton = document.querySelector('#dough-calc-button');
const doughContainer = document.querySelector('.dough-container');
const pieNum = document.querySelector('#pie-num');

calcButton.addEventListener('click', () => {
    console.log('click')
    let pieCount = pieNum.value;
    let weights = doughContainer.querySelectorAll('.dough-weight');
    for (let w of weights) {
        let ratioField = w.previousElementSibling;
        console.log(ratioField)
        let select = ratioField.querySelector('select');
        console.log(select)
        if (select) {
            ratio = select.value;
        } else {
            ratio = parseFloat(ratioField.textContent) / 100;
        }
        w.textContent = (ratio * (+pieCount * 242.5)).toFixed(3);
    }
})