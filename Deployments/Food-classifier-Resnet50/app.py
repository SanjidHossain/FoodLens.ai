import gradio as gr
from fastai.vision.all import load_learner
import pathlib
import platform  # Add this import

plt = platform.system()
if plt == 'Linux':
    pathlib.WindowsPath = pathlib.PosixPath


food_labels = (
'Baden_Brägele_with_Bibliskäs', 'Bibimbap_food',
'Blanquette_de_Veau', 'Boeuf_Bourguignon', 'Bossam_food',
'Bouillabaisse', 'Braised_Beef_Rheinland_style', 'Braunkohl_and_Bregenwurst',
'Budae_Jjigae_food', 'Bulgogi_food', 'Butter_Noodles', 'Cassoulet', 'Chuncheon_Dakgalbi_food',
'Coq_au_Vin', 'Coquilles_Saint_Jacques', 'Crème_brûlée', 'Crêpes', 'Dumplings', 'Döner_with_Curried_Sausage',
'Escargots', 'Fondue_Savoyarde', 'Frankfurter_Green_Sauce', 'German_Bread_Rolls', 'Gimbap_food', 'Gyudon',
'Hamburger_Labskaus', 'Hamburger_Pannfisch', 'Kalguksu_food', 'Kare_raisu', 'Katsudon', 'Kimchi_Jjigae_food',
'Königsberger_Meatballs', 'Manduguk_food', 'Miso_soup', 'Moules_Marinières', 'Ojingeo_Bokkeum_food', 'Okonomiyaki',
'Omurice', 'Onigiri', 'Pajeon_food', 'Pissaladière', 'Pork_Knuckle_with_Sauerkraut',
'Potato_Fritters_or_Potato_Pancakes_Kartoffelpuffer_', 'Potato_Salad', 'Pretzen_from_Bavaria',
'Pumpernickel_from_Lower_Saxony', 'Ramen', 'Salade_niçoise', 'Samgyetang_food', 'Shabu_Shabu', 'Soba',
'Soufflé', 'Soupe_à_L_oignon', 'Steak_Tartare', 'Sundae_food', 'Sushi_Sashimi', 'Tarte_Flambée_with_a_French_Influence',
'Tarte_Tatin', 'Tartiflette', 'Tempura', 'Tteokbokki_food', 'Udon', 'Yakitori', 'Yangnyeom_Tongdak_food', 'adhirasam',
'aloo_gobi', 'aloo_matar', 'aloo_methi', 'aloo_shimla_mirch', 'aloo_tikki', 'anarsa', 'apple_pie', 'ariselu', 'baby_back_ribs',
'baklava', 'bandar_laddu', 'basundi', 'beef_carpaccio', 'beef_tartare', 'beet_salad', 'beignets', 'bhatura', 'bhindi_masala',
'biryani', 'boondi', 'bread_pudding', 'breakfast_burrito', 'bruschetta', 'butter_chicken', 'caesar_salad', 'cannoli', 'caprese_salad',
'carrot_cake', 'ceviche', 'chak_hao_kheer', 'cham_cham', 'chana_masala', 'chapati', 'cheese_plate', 'cheesecake', 'chhena_kheeri',
'chicken_quesadilla', 'chicken_razala', 'chicken_tikka', 'chicken_tikka_masala', 'chicken_wings', 'chikki', 'chocolate_cake',
'chocolate_mousse', 'churros', 'clam_chowder', 'club_sandwich', 'crab_cakes', 'creme_brulee', 'croque_madame', 'cup_cakes',
'daal_baati_churma', 'daal_puri', 'dal_makhani', 'dal_tadka', 'deviled_eggs', 'dharwad_pedha', 'donuts', 'doodhpak', 'double_ka_meetha',
'dum_aloo', 'edamame', 'eggs_benedict', 'falafel', 'filet_mignon', 'fish_and_chips', 'foie_gras', 'french_fries', 'french_onion_soup',
'french_toast', 'fried_calamari', 'fried_rice', 'frozen_yogurt', 'gajar_ka_halwa', 'garlic_bread', 'gavvalu', 'ghevar', 'gnocchi',
'greek_salad', 'grilled_cheese_sandwich', 'grilled_salmon', 'guacamole', 'gulab_jamun', 'gyoza', 'hamburger', 'hot_and_sour_soup',
'hot_dog', 'huevos_rancheros', 'hummus', 'ice_cream', 'imarti', 'jalebi', 'kachori', 'kadai_paneer', 'kadhi_pakoda', 'kajjikaya',
'kakinada_khaja', 'kalakand', 'karela_bharta', 'kofta', 'kuzhi_paniyaram', 'lasagna', 'lassi', 'ledikeni', 'litti_chokha',
'lobster_bisque', 'lobster_roll_sandwich', 'lyangcha', 'maach_jhol', 'macaroni_and_cheese', 'macarons', 'makki_di_roti_sarson_da_saag',
'malapua', 'misi_roti', 'misti_doi', 'modak', 'mussels', 'mysore_pak', 'naan', 'nachos', 'navrattan_korma', 'omelette', 'onion_rings',
'oysters', 'pad_thai', 'paella', 'palak_paneer', 'pancakes', 'paneer_butter_masala', 'panna_cotta', 'peking_duck', 'phirni', 'pho', 'pithe',
'pizza', 'poha', 'poornalu', 'pootharekulu', 'pork_chop', 'poutine', 'prime_rib', 'pulled_pork_sandwich', 'qubani_ka_meetha', 'rabri',
'ras_malai', 'rasgulla', 'ravioli', 'red_velvet_cake', 'risotto', 'samosa', 'sandesh', 'sashimi', 'scallops', 'seaweed_salad',
'shankarpali', 'sheer_korma', 'sheera', 'shrikhand', 'shrimp_and_grits', 'sohan_halwa', 'sohan_papdi', 'spaghetti_bolognese',
'spaghetti_carbonara', 'spring_rolls', 'steak', 'strawberry_shortcake', 'sushi', 'sutar_feni', 'tacos', 'takoyaki', 'tiramisu',
'tuna_tartare', 'unni_appam', 'waffles'
)




model = load_learner('food-recognizer-r50-v0.pkl')

def recognize_image(image):
  pred, idx, probs = model.predict(image)
  print(pred, probs)
  return dict(zip(food_labels, map(float, probs)))

image = gr.inputs.Image(shape=(192,192))
label = gr.outputs.Label(num_top_classes=5)
examples = [
    'test1.jpg',
    'test2.jpg',
    'test3.jpg',
    'test4.jpg',
    'test5.jpg',
    'test6.jpg'
    ]

iface = gr.Interface(fn=recognize_image, inputs=image, outputs=label, examples=examples)
iface.launch(inline=False)
