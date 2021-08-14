from django import template
from django.utils.safestring import mark_safe
from mainapp.models import Smartphone

register = template.Library()


TABLE_HEAD = """
                <table class="table">
                    <tbody>
             """

TABLE_CONTENT = """
                        <tr>
                            <td class="ps-0">{name}</td>
                            <td>{value}</td>
                        </tr>
                """

TABLE_FOOTER = """
                    </tbody>
                </table>
               """

TRUE_ICON = """
               <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-lg text-success" viewBox="0 0 16 16">
                   <path d="M13.485 1.431a1.473 1.473 0 0 1 2.104 2.062l-7.84 9.801a1.473 1.473 0 0 1-2.12.04L.431 8.138a1.473 1.473 0 0 1 2.084-2.083l4.111 4.112 6.82-8.69a.486.486 0 0 1 .04-.045z"/>
               </svg>
            """

FALSE_ICON = """
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg text-danger" viewBox="0 0 16 16">
                    <path d="M1.293 1.293a1 1 0 0 1 1.414 0L8 6.586l5.293-5.293a1 1 0 1 1 1.414 1.414L9.414 8l5.293 5.293a1 1 0 0 1-1.414 1.414L8 9.414l-5.293 5.293a1 1 0 0 1-1.414-1.414L6.586 8 1.293 2.707a1 1 0 0 1 0-1.414z"/>
                </svg>
             """

PRODUCT_SPECIFICATIONS = {
    'notebook': {
        'Діагональ': 'diagonal',
        'Дисплей': 'display',
        'Частота процесора': 'processor_frequency',
        'Оперативна пам\'ять': 'ram',
        'Відеокарта': 'video_card',
        'Час роботи від батареї': 'accumulator_volume',
    },
    'smartphone': {
        'Діагональ': 'diagonal',
        'Дисплей': 'display',
        'Роздільна здатність': 'resolution',
        'Оперативна пам\'ять': 'ram',
        'Об\'єм акумулятора': 'accumulator_volume',
        'Наявність SD-карти': 'sd_card',
        'Максимальний обсяг SD-карти': 'sd_card_volume',
        'Головна камера': 'main_camera_size',
        'Фронтальна камера': 'frontal_camera_size',
    },
}


def get_product_specification(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPECIFICATIONS[model_name].items():
        field_value = getattr(product, value)
        if value == 'sd_card':
            if field_value:
                field_value = TRUE_ICON
            else:
                field_value = FALSE_ICON
        table_content += TABLE_CONTENT.format(name=name, value=field_value)
    return table_content


@register.filter
def product_specification(product):
    model_name = product.__class__._meta.model_name
    if isinstance(product, Smartphone):
        if not product.sd_card:
            PRODUCT_SPECIFICATIONS['smartphone'].pop('Максимальний обсяг SD-карти')
    return mark_safe(TABLE_HEAD + get_product_specification(product, model_name) + TABLE_FOOTER)