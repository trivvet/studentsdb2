var mylink = document.getElementById('add_button');
mylink.addEventListener('click',
    function(event) {
        alert('add_button is clicked')
    }
);
mylink.addEventListener('mouseover',
    function(event) {
        this.style.display = 'none';
    }
).addEventListener('mouseout',
    function(event) {
        this.style.display = '';
    }
);
