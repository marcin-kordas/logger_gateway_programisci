import os
import shutil

# Mapowanie: stara nazwa -> nowa nazwa (na podstawie odczytanych danych z obrazów)
image_mappings = {
    "stworz_wizualizacje_osoby_rekrutowanej_Ala_ready_player_one_ale_w_stylu_grafiki_i_akcesoriach_dopasowanych...danej_osoby_name_Zuzanna_Kot_validation_status_alignment_LOW_justification_First_year_IT_student_with_only_basic_C_image_1.png": "Zuzanna_Kot.png",
    "_Defining_the_Profile_Im_working_on_visualizing_Zuzanna_Kots_profile_Right_now_Im_analyzing_the_data_Shes_...udent_with_a_focus_on_CC_and_Linux_but_the_lack_of_practical_experience_is_a_key_consideration_Constructing_the_Sc_image_1 (2).png": "Artur_Piskorski.png",
    "_Defining_the_Profile_Im_working_on_visualizing_Zuzanna_Kots_profile_Right_now_Im_analyzing_the_data_Shes_...udent_with_a_focus_on_CC_and_Linux_but_the_lack_of_practical_experience_is_a_key_consideration_Constructing_the_Sc_image_1 (3).png": "Jakub_Sobczuk.png",
    "_Defining_the_Profile_Im_working_on_visualizing_Zuzanna_Kots_profile_Right_now_Im_analyzing_the_data_Shes_...udent_with_a_focus_on_CC_and_Linux_but_the_lack_of_practical_experience_is_a_key_consideration_Constructing_the_Sc_image_1 (4).png": "Kamil_Godek.png",
    "_Defining_the_Profile_Im_working_on_visualizing_Zuzanna_Kots_profile_Right_now_Im_analyzing_the_data_Shes_...udent_with_a_focus_on_CC_and_Linux_but_the_lack_of_practical_experience_is_a_key_consideration_Constructing_the_Sc_image_1 (5).png": "Dawid_Łukasik.png",
    "_Defining_the_Profile_Im_working_on_visualizing_Zuzanna_Kots_profile_Right_now_Im_analyzing_the_data_Shes_...udent_with_a_focus_on_CC_and_Linux_but_the_lack_of_practical_experience_is_a_key_consideration_Constructing_the_Sc_image_1 (6).png": "Magdalena_Nowakowska.png",
    "_Defining_the_Profile_Im_working_on_visualizing_Zuzanna_Kots_profile_Right_now_Im_analyzing_the_data_Shes_...udent_with_a_focus_on_CC_and_Linux_but_the_lack_of_practical_experience_is_a_key_consideration_Constructing_the_Sc_image_1.png": "Ihor_Horalevych.png"
}

# Utwórz katalog images jeśli nie istnieje
os.makedirs("images", exist_ok=True)

print("Kopiowanie i przemianowanie plików...\n")

success_count = 0
for old_name, new_name in image_mappings.items():
    if os.path.exists(old_name):
        dst = os.path.join("images", new_name)
        shutil.copy2(old_name, dst)
        print(f"✓ {new_name}")
        success_count += 1
    else:
        print(f"✗ Nie znaleziono: {old_name[:80]}...")

print(f"\n{'='*60}")
print(f"Sukces! Przetworzono {success_count}/{len(image_mappings)} obrazów")
print(f"Katalog: images/")
print(f"{'='*60}\n")

# Wyświetl zawartość katalogu
print("Zawartość katalogu images/:")
for f in sorted(os.listdir("images")):
    if f.endswith(".png"):
        size_mb = os.path.getsize(os.path.join("images", f)) / (1024 * 1024)
        print(f"  • {f:<30} ({size_mb:.2f} MB)")
