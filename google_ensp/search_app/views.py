from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import QueryForm


def home(request):
    context = {}
    return render(request,'search_app/home.html', context)

def index(request):

    resultats_list = [{'title': 'How To Cook Eggs 101 | Get Cracking - Eggs.ca', 'summary': 'Want to master the art of meringues or learn how to poach an egg like a pro? Read our egg how-to articles and Get Cracking, today.', 'link': 'https://www.eggs.ca/eggs101/'},
    {'title': 'How to Boil Eggs - The Stay at Home Chef', 'summary': 'How many minutes should I cook my egg? Soft Boiled (runny or very soft yolk) – 4 to 6 minutes. Hard Boiled (solid cooked yolk) – 8 to 12 minutes. Hard Boiled', 'link': 'https://thestayathomechef.com/how-to-boil-eggs/'},{'title': 'How to Fry an Egg - Perfect Fried Egg Over Easy, Medium', 'summary': 'In a small nonstick over medium heat, melt butter (or heat oil). Crack egg into pan. Cook 3 minutes, or until white is set. Flip and cook 4 to 5', 'link': 'https://www.delish.com/cooking/recipe-ideas/a23499380/how-to-fry-an-egg/'},
    {'title': 'How to Cook an Egg | goop', 'summary': 'Heat the olive oil in a small, non-stick pan over medium heat. Crack the egg directly into the pan and season generously with salt and pepper. Cook for about two minutes, then use a spatula to flip the egg, being careful not to break the yolk. For a runny yolk, turn off the heat and let the egg sit for one minute.', 'link': 'https://goop.com/food/tutorials/how-to-cook-an-egg/#:~:text=Heat%20the%20olive%20oil%20in,egg%20sit%20for%20one%20minute.'},{'title': 'How to cook eggs safely - Safefood', 'summary': 'Only eat duck eggs that are thoroughly cooked –that means that both the egg white and yolk are solid. · Never eat duck eggs raw or lightly cooked. · Dishes that', 'link': 'https://www.safefood.net/food-safety/cooking-eggs'},
    {'title': 'What Is the Healthiest Way to Cook and Eat Eggs? - Healthline', 'summary': '15 mai 2020 — 5 tips to cook super healthy eggs · 1. Choose a low-calorie cooking method If you are trying to cut back on calories, choose poached or boiled ', 'link': 'https://www.healthline.com/nutrition/eating-healthy-eggs'},{'title': '"How Do You Want Your Eggs?" Eleven Ways To Cook An Egg', 'summary': 'A hard boiled egg is cooked in its shell in boiling water. The “hard” refers to the consistency of the egg white (or albumen) and the yolk. Making', 'link': 'https://www.breakfastwithnick.com/2014/04/08/how-do-you-want-your-eggs-eleven-ways-to-cook-an-egg/'},
    {'title': 'Titre8', 'summary': 'Summary8', 'link': 'link8'},{'title': 'Titre9', 'summary': 'Summary9', 'link': 'link9'},
    {'title': 'Titre10', 'summary': 'Summary10', 'link': 'link10'},{'title': 'Titre11', 'summary': 'Summary11', 'link': 'link11'},
    {'title': 'Titre12', 'summary': 'Summary12', 'link': 'link12'},{'title': 'Titre13', 'summary': 'Summary13', 'link': 'link13'},
    {'title': 'Titre14', 'summary': 'Summary14', 'link': 'link14'},{'title': 'Titre15', 'summary': 'Summary15', 'link': 'link15'},
    {'title': 'Titre16', 'summary': 'Summary16', 'link': 'link16'},{'title': 'Titre17', 'summary': 'Summary17', 'link': 'link17'},
    {'title': 'Titre18', 'summary': 'Summary18', 'link': 'link18'},{'title': 'Titre19', 'summary': 'Summary19', 'link': 'link19'},
    {'title': 'Titre20', 'summary': 'Summary20', 'link': 'link20'},{'title': 'Titre21', 'summary': 'Summary21', 'link': 'link21'},
    {'title': 'Titre22', 'summary': 'Summary22', 'link': 'link22'},{'title': 'Titre23', 'summary': 'Summary23', 'link': 'link23'},
    {'title': 'Titre24', 'summary': 'Summary24', 'link': 'link24'},{'title': 'Titre25', 'summary': 'Summary25', 'link': 'link25'},
    {'title': 'Titre26', 'summary': 'Summary26', 'link': 'link26'},{'title': 'Titre27', 'summary': 'Summary27', 'link': 'link27'},
    {'title': 'Titre28', 'summary': 'Summary28', 'link': 'link28'},
    {'title': 'Titre1', 'summary': 'Summary1', 'link': 'link1'},
    {'title': 'Titre2', 'summary': 'Summary2', 'link': 'link2'},{'title': 'Titre3', 'summary': 'Summary3', 'link': 'link3'},
    {'title': 'Titre4', 'summary': 'Summary4', 'link': 'link4'},{'title': 'Titre5', 'summary': 'Summary5', 'link': 'link5'},
    {'title': 'Titre6', 'summary': 'Summary6', 'link': 'link6'},{'title': 'Titre7', 'summary': 'Summary7', 'link': 'link7'},
    {'title': 'Titre8', 'summary': 'Summary8', 'link': 'link8'},{'title': 'Titre9', 'summary': 'Summary9', 'link': 'link9'},
    {'title': 'Titre10', 'summary': 'Summary10', 'link': 'link10'},{'title': 'Titre11', 'summary': 'Summary11', 'link': 'link11'},
    {'title': 'Titre12', 'summary': 'Summary12', 'link': 'link12'},{'title': 'Titre13', 'summary': 'Summary13', 'link': 'link13'},
    {'title': 'Titre14', 'summary': 'Summary14', 'link': 'link14'},{'title': 'Titre15', 'summary': 'Summary15', 'link': 'link15'},
    {'title': 'Titre16', 'summary': 'Summary16', 'link': 'link16'},{'title': 'Titre17', 'summary': 'Summary17', 'link': 'link17'},
    {'title': 'Titre18', 'summary': 'Summary18', 'link': 'link18'},{'title': 'Titre19', 'summary': 'Summary19', 'link': 'link19'},
    {'title': 'Titre20', 'summary': 'Summary20', 'link': 'link20'},{'title': 'Titre21', 'summary': 'Summary21', 'link': 'link21'},
    {'title': 'Titre22', 'summary': 'Summary22', 'link': 'link22'},{'title': 'Titre23', 'summary': 'Summary23', 'link': 'link23'},
    {'title': 'Titre24', 'summary': 'Summary24', 'link': 'link24'},{'title': 'Titre25', 'summary': 'Summary25', 'link': 'link25'},
    {'title': 'Titre26', 'summary': 'Summary26', 'link': 'link26'},{'title': 'Titre27', 'summary': 'Summary27', 'link': 'link27'},
    {'title': 'Titre28', 'summary': 'Summary28', 'link': 'link28'},
    {'title': 'Titre1', 'summary': 'Summary1', 'link': 'link1'},
    {'title': 'Titre2', 'summary': 'Summary2', 'link': 'link2'},{'title': 'Titre3', 'summary': 'Summary3', 'link': 'link3'},
    {'title': 'Titre4', 'summary': 'Summary4', 'link': 'link4'},{'title': 'Titre5', 'summary': 'Summary5', 'link': 'link5'},
    {'title': 'Titre6', 'summary': 'Summary6', 'link': 'link6'},{'title': 'Titre7', 'summary': 'Summary7', 'link': 'link7'},
    {'title': 'Titre8', 'summary': 'Summary8', 'link': 'link8'},{'title': 'Titre9', 'summary': 'Summary9', 'link': 'link9'},
    {'title': 'Titre10', 'summary': 'Summary10', 'link': 'link10'},{'title': 'Titre11', 'summary': 'Summary11', 'link': 'link11'},
    {'title': 'Titre12', 'summary': 'Summary12', 'link': 'link12'},{'title': 'Titre13', 'summary': 'Summary13', 'link': 'link13'},
    {'title': 'Titre14', 'summary': 'Summary14', 'link': 'link14'},{'title': 'Titre15', 'summary': 'Summary15', 'link': 'link15'},
    {'title': 'Titre16', 'summary': 'Summary16', 'link': 'link16'},{'title': 'Titre17', 'summary': 'Summary17', 'link': 'link17'},
    {'title': 'Titre18', 'summary': 'Summary18', 'link': 'link18'},{'title': 'Titre19', 'summary': 'Summary19', 'link': 'link19'},
    {'title': 'Titre20', 'summary': 'Summary20', 'link': 'link20'},{'title': 'Titre21', 'summary': 'Summary21', 'link': 'link21'},
    {'title': 'Titre22', 'summary': 'Summary22', 'link': 'link22'},{'title': 'Titre23', 'summary': 'Summary23', 'link': 'link23'},
    {'title': 'Titre24', 'summary': 'Summary24', 'link': 'link24'},{'title': 'Titre25', 'summary': 'Summary25', 'link': 'link25'},
    {'title': 'Titre26', 'summary': 'Summary26', 'link': 'link26'},{'title': 'Titre27', 'summary': 'Summary27', 'link': 'link27'},
    {'title': 'Titre28', 'summary': 'Summary28', 'link': 'link28'},]
    paginator = Paginator(resultats_list, 7)
    nombre_page = int(len(resultats_list)/7) if len(resultats_list)%7 == 0  else int(len(resultats_list)/7 + 1)
    x = range(nombre_page)
    page = request.GET.get('page')
    try:
        resultats = paginator.page(page)
    except PageNotAnInteger:
        resultats = paginator.page(1)
    except EmptyPage:
        resultats = paginator.page(paginator.num_pages)
    context = {'resultats': resultats, 
               'x': x,
    }
    return render(request,'search_app/index.html', context)