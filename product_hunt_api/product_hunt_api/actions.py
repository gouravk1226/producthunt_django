import requests
import json
from django.http import HttpResponse
from .constants import PRODUCT_HUNT_ENDPOINT, HEADERS


# this functions make request to product hunt api and fetch the data

def make_request_to_product_hunt():

    json_data = requests.get(PRODUCT_HUNT_ENDPOINT, headers=HEADERS)
    product_hunt_data = json.loads(json_data.text)
    return product_hunt_data


# checks whether link is dead or not

def is_link_dead(link):
    link_response = requests.get(link)
    return True if link_response.status_code != 200 else False


# this function sort the given dictionary

def sort_dictionary(dic):

    sorted_values = sorted(dic.values())  # Sort the values
    sorted_dict = {}

    for value in sorted_values:
        for key in dic.keys():
            if dic[key] == value:
                sorted_dict[key] = dic[key]

    return sorted_dict


# This functions accept the request from the api and return the processed data

def return_deadlinks_ranking(request):

    product_hunt_data = make_request_to_product_hunt()
    votes_dic = {}
    comment_dic = {}
    data_to_be_returned = {}

    for product in product_hunt_data['posts']:
        comments_count = product['comments_count']
        votes_count = product['votes_count']
        product_name = product['name']
        product_link = product['discussion_url']
        votes_dic[product_name] = votes_count
        comment_dic[product_name] = comments_count

        if is_link_dead(product_link):
            sorted_votes = sort_dictionary(votes_dic)
            sorted_comment = sort_dictionary(comment_dic)
            desc_sorted_votes = [key for key in sorted_votes.keys()]
            desc_sorted_comment = [key for key in sorted_comment.keys()]
            data_to_be_returned = {'votes': desc_sorted_votes, 'comments': desc_sorted_comment}

    return HttpResponse(json.dumps(data_to_be_returned), content_type='application/json')
