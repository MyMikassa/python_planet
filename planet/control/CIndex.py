# -*- coding: utf-8 -*-
from flask import request

from planet.common.success_response import Success
from planet.extensions.register_ext import cache
from planet.extensions.validates.index import IndexListBannerForm
from planet.service.SIndex import SIndex


class CIndex:
    def __init__(self):
        self.sindex = SIndex()

    # @cache.cached(timeout=50, key_prefix='index')
    def list_brand(self):
        """首页的品牌"""
        index_brands = self.sindex.get_index_brand()
        res = []
        for index_brand, brand in index_brands:
            index_brand.fill('brand', brand)
            res.append(index_brand)
        return Success(data=res)

    def list_banner(self):
        form = IndexListBannerForm().valid_data()
        ibshow = dict(form.ibshow.choices).get(form.ibshow.data)
        index_banners = self.sindex.get_index_banner({'IBshow': ibshow})
        return Success(data=index_banners)

    def list_product(self):
        index_products = self.sindex.get_index_product()
        res = []
        for index_product, product in index_products:
            index_product.fill('PRmainpic', product.PRmainpic)
            index_product.fill('PRlinePrice', product.PRlinePrice)
            index_product.fill('PRprice', product.PRprice)
            index_product.fill('PRtitle', product.PRtitle)
            res.append(index_product)
        return Success(data=res)






