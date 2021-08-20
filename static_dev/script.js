$(document).ready(function(){
    $('.plus').on('click', function(){
        let inputName = $(this).attr('for');
        let inputValue = parseInt($(inputName).val());
        $(inputName).val(Math.min(inputValue + 1, 999));
        $(this).parent().find('form').submit();
    });
    $('.minus').on('click', function(){
        let inputName = $(this).attr('for');
        let inputValue = parseInt($(inputName).val());
        $(inputName).val(Math.max(inputValue - 1, 0));
        $(this).parent().find('form').submit();
    });
    $('.cart-form').submit(function(e){
        let total_price_field = $(this).attr('total-price-field');
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            cache: false,
            data:
            {
                quantity: $('input[name="quantity"]', this).val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(data){
                data = JSON.parse(data);
                $("#cart-total-price h5").html(data['cart_total_price']);
                $("#cart-message").html(data['cart_message']);
                $(".cart-badge").html(data['cart_products_quantity']);
                $(total_price_field).html(data['product_total_price']);
            }
        })
    });
});