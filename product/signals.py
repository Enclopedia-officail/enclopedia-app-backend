from django.db.models.signals import post_save
from django.dispatch import receiver
from product.models import Product, ReviewRating
from django.db.models import Avg, Count
from django.conf import settings

# reviewが作成された時に自動的にreviewの平均値をもとめて平均値を割り出す


@receiver(post_save, sender=ReviewRating)
def rating_average(sender, instance, created, **kwargs):
    if created and instance.id:
        ratings = instance.product.rating_average()
        # productにカウントを混ぜる
        count = instance.product.count_review()
        print(count)
        product = Product.objects.get(id=instance.product_id)
        product.rating = round(ratings, 1)
        print(product.rating)
        product.review_count = count
        product.save()

#自動的にproductが作成された際にpriceも登録されるようにする