import django
from django.core.files import File
from django.core.files.images import ImageFile
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()
# import model need to be after django.setup()
from shop.models import Item

def populate():
    # dictionary of products
    T_shirts = [
        {'name': 'tee1',
         'product_season': 'summer',
         'product_type': 'tee',
         'price': 10,
         'description': 'Nice summer tee',
         'image': "C:/Users/daniel/Workspace/ecommerce/media/product_images/black_tshirt.jpg"
         },
        {'name': 'tee2',
         'product_season': 'summer',
         'product_type': 'tee',
         'price': 10,
         'description': 'Nice summer tee',
         'image': "C:/Users/daniel/Workspace/ecommerce/media/product_images/white_tshirt.jpg"
         },
        {'name': 'tee3',
         'product_season': 'winter',
         'product_type': 'tee',
         'price': 10,
         'description': 'Nice summer tee',
         'image': "C:/Users/daniel/Workspace/ecommerce/media/product_images/white_tshirt.jpg"
         },
    ]

    dress = [
        {'name': 'dress1',
         'product_season': 'spring',
         'product_type': 'dress',
         'price': 10,
         'description': 'Nice dress',
         'image': "C:/Users/daniel/Workspace/ecommerce/media/product_images/dress1.jpg"
         },
        {'name': 'dress2',
         'product_season': 'summer',
         'product_type': 'dress',
         'price': 20,
         'description': 'Nice dress',
         'image': "C:/Users/daniel/Workspace/ecommerce/media/product_images/dress1.jpg"
         },
        {'name': 'dress3',
         'product_season': 'autum',
         'product_type': 'dress',
         'price': 30,
         'description': 'Nice dress',
         'image': "C:/Users/daniel/Workspace/ecommerce/media/product_images/dress1.jpg"
         },
    ]
    trousers = [
        {'name': 'trousers1',
         'product_season': 'spring',
         'product_type': 'trousers',
         'price': 10,
         'description': 'Nice trousers',
         'image': "C:/Users/daniel/Workspace/ecommerce/media/product_images/trousers1.jpg"
         },
        {'name': 'trousers2',
         'product_season': 'summer',
         'product_type': 'trousers',
         'price': 20,
         'description': 'Nice trousers',
         'image': "C:/Users/daniel/Workspace/ecommerce/media/product_images/trousers2.jpg"
         },
        {'name': 'trousers3',
         'product_season': 'autum',
         'product_type': 'trousers',
         'price': 30,
         'description': 'Nice trousers',
         'image': "C:/Users/daniel/Workspace/ecommerce/media/product_images/trousers1.jpg"
         },
    ]

    Items = T_shirts+dress+trousers

    for AnItem in Items:
        i = Item.objects.get_or_create(
            name=AnItem['name'], product_season=AnItem['product_season'], price=AnItem['price'])[0]
        i.product_type = AnItem['product_type']
        i.description = AnItem['description']
        #i.image=ImageFile(open("C:\\Users\\daniel\\Desktop\\no license clothing\\cat_tshirt.jpg", 'rb'))
        i.image = AnItem['image']
        #i.image = "C:/Users/daniel/Workspace/ecommerce/media/product_images/cat_tshirt.jpg"
        i.save()


# Start execution here!
if __name__ == '__main__':
    print('Starting shop population script...')
    populate()
