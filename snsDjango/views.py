from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView

from .models import Pref, Category
from .forms import SearchForm
import json
import requests
def get_keyid():
    return "この中に取得したkeyidを入れてください"
class IndexView(TemplateView):
    template_name = 'snsDjango/index.html'

    def get_context_data(self, *args, **kwargs):
        searchform = SearchForm()
        category_list = Category.objects.all().order_by('category_l')
        pref_list = Pref.objects.all().order_by('pref')
        params = {
            'searchform': searchform,
            'category_list': category_list,
            'pref_list': pref_list,
            }
        return params
def Search(request):
    if request.method == 'GET':
        searchform = SearchForm(request.POST)

        if searchform.is_valid():
            category_l = request.GET['category_l']
            pref = request.GET['pref']
            freeword = request.GET['freeword']
            query = get_gnavi_data("", category_l, pref, freeword, 10)
            res_list = rest_search(query)
            total_hit_count = len(res_list)
            # 4. 整形した情報をリスト形式で保存し、paramsの一要素として渡す
            restaurants_info = extract_restaurant_info(res_list)

    params = {
        'total_hit_count': total_hit_count,
        'restaurants_info': restaurants_info,
        }

    return render (request, 'snsDjango/search.html', params)


def get_gnavi_data(id, category_l, pref, freeword, hit_per_page):
    keyid = get_keyid()
    # 一度に取得できる最大件数
    hit_per_page = hit_per_page
    # 店舗のid（グルナビ内で一意になっている）
    id = id
    # 大業態カテゴリ
    category_l = category_l
    #pref
    pref = pref
    #Freeword
    freeword = freeword
    #今回は関東地方のみ（コール回数を少なくするため）
    area = "AREA110"
    #パラメータ設定
    query = {"keyid": keyid, "id":id, "area":area, "pref":pref, "category_l":category_l,"hit_per_page":hit_per_page, "freeword":freeword}

    return query


def rest_search(query):
    res_list = []
    res = json.loads(requests.get("https://api.gnavi.co.jp/RestSearchAPI/v3/", params=query).text)
    # レスポンスがerror でない場合に処理を開始する
    if "error" not in res:
        res_list.extend(res["rest"])
    return res_list


def extract_restaurant_info(restaurants: 'restaurant response') -> 'restaurant list':
    restaurant_list = []
    for restaurant in restaurants:
        id = restaurant["id"]
        name = restaurant["name"]
        name_kana = restaurant["name_kana"]
        url = restaurant["url"]
        url_mobile = restaurant["url_mobile"]
        shop_image1 = restaurant["image_url"]["shop_image1"]
        shop_image2 = restaurant["image_url"]["shop_image2"]
        address = restaurant["address"]
        tel = restaurant["tel"]
        station_line = restaurant["access"]["line"]
        station = restaurant["access"]["station"]
        latitude = restaurant["latitude"]
        longitude = restaurant["longitude"]
        pr_long = restaurant["pr"]["pr_long"]

        restaurant_list.append([id, name, name_kana, url, url_mobile, shop_image1, shop_image2, address, tel, station_line, station, latitude, longitude, pr_long])
    return restaurant_list

