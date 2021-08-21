$(document).ready(function(){
    let cartTimeout;
    $('.plus').on('click', function(){
        let inputName = $(this).attr('for');
        let inputValue = parseInt($(inputName).val());
        $(inputName).val(Math.min(inputValue + 1, 999));
        clearTimeout(cartTimeout);
        $('.cart-spinner').show();
        $('.cart-buttons a').addClass('disabled');
        cartTimeout = setTimeout(() => {
            $(this).parent().find('form').submit();
        }, 500);
    });
    $('.minus').on('click', function(){
        let inputName = $(this).attr('for');
        let inputValue = parseInt($(inputName).val());
        $(inputName).val(Math.max(inputValue - 1, 1));
        clearTimeout(cartTimeout);
        $('.cart-spinner').show();
        $('.cart-buttons a').addClass('disabled');
        cartTimeout = setTimeout(() => {
            $(this).parent().find('form').submit();
        }, 500);
    });
    $('.cart-form input[name="quantity"]').on('input', function(){
        $(this).val(Math.min(999, Math.max(1, parseInt($(this).val()))));
        let inputValue = parseInt($(this).val());
        if(inputValue){
            clearTimeout(cartTimeout);
            $('.cart-spinner').show();
            $('.cart-buttons a').addClass('disabled');
            cartTimeout = setTimeout(() => {
                $(this).parent().submit();
            }, 500);
        }
    });
    $('.cart-form input[name="quantity"]').on('focusout', function(){
        if(!$(this).val()){
            $(this).val(1);
            clearTimeout(cartTimeout);
            $('.cart-spinner').show();
            $('.cart-buttons a').addClass('disabled');
            cartTimeout = setTimeout(() => {
                $(this).parent().submit();
            }, 500);
        }
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
                $('.cart-spinner').hide();
                $('.cart-buttons a').removeClass('disabled');
            }
        })
    });
});