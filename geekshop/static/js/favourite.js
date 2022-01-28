window.onload = function () {
     $('.description').on('click', 'a[id="favourite_button"]', function() {
        var target = event.target;
        var product_pk = parseInt(target.name.replace('favourite-', ''));
        $.ajax({
            url: '/products/product/ajax/' + product_pk + '/',
            success: function (data) {
                $('#favourite_button').html(data.result);
            },
        })
        console.log(target)
        console.log(product_pk)
     })
}