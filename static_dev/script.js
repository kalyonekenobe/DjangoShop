$(document).ready(function(){
    let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    });
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
    $(".add-to-cart").on('click', function(){
        $(this).addClass('disabled');
        let link = $(this);
        let action = $(this).attr('action');
        $.ajax({
            type: 'POST',
            url: action,
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]', this).val(),
            },
            success: function(data){
                if(data == 'True'){
                    if(link.hasClass('btn-success')){
                        link.html("<i class='bi bi-cart-check me-1'></i> Товар у корзині");
                        link.attr('class', 'btn btn-outline-success add-to-cart');
                    }else{
                        link.html("<i class='bi bi-cart-check'></i>");
                        link.attr('class', 'btn btn-success add-to-cart');
                        link.attr('data-bs-toggle', "tooltip");
                        link.attr('data-bs-placement', "top");
                        link.attr('title', "Товар вже додано до корзини");
                    }
                    link.attr('action', '');
                    link.attr('href', '/cart/');
                    tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
                    tooltipTriggerList.map(function (tooltipTriggerEl) {
                      return new bootstrap.Tooltip(tooltipTriggerEl)
                    });
                }
                link.removeClass('disabled');
            }
        });
    });
});