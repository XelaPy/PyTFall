label mc_setup_merchant:
    "Setting up main Merchant effects here!"
    return
    
label mc_setup_merchant_caravan:
    "Setting up main Merchant-Caravan effects here!"
    return
    
label mc_setup_merchant_mc_defender:
    "MC Caravan Defender Option Reporting!"
    return
    
label mc_setup_merchant_mc_defender_sword:
    "MC Caravan Defender Sword Option Reporting (Finally)!"
    return
    
label mc_setup_warrior_warrior_amazon: 
    $ hero.apply_trait("Amazon Blood")
    return
    
label mc_setup_warrior_warrior_amazon_yuri:
    $ hero.apply_trait("Yuri Expert")
    return
    
label mc_setup_warrior_warrior_amazon_muscle:
    $ hero.apply_trait("Amazon Musculature")
    return
    
label mc_setup_warrior_warrior_amazon_berserk:
    $ hero.apply_trait("Berserk")
    return
    
label mc_setup_warrior_warrior_dragon:
    $ hero.apply_trait("Dragon Blood")
    return
    
label mc_setup_warrior_warrior_dragon_fire:
    $ hero.apply_trait("Fire Dragon Scales")
    return
    
label mc_setup_warrior_warrior_dragon_stone:
    $ hero.apply_trait("Stone Dragon Scales")
    return
    
label mc_setup_warrior_warrior_dragon_sight:
    $ hero.apply_trait("Dragon Eyesight")
    return

label mc_setup_warrior_defender_guard:
label mc_setup_warrior_assassin_princess:
    $ hero.apply_trait("Royal Blood")
    return
    
label mc_setup_warrior_assassin_princess_knight:
    $ hero.apply_trait("Knightly Stance")
    return
    
label mc_setup_warrior_assassin_princess_fencer:
    $ hero.apply_trait("Sword Master")
    return
    
label mc_setup_warrior_assassin_princess_royal:
    $ hero.apply_trait("Royal Assassin")
    return
    
label mc_setup_warrior_assassin_drow:
    $ hero.apply_trait("Drow Blood")
    return
    
label mc_setup_warrior_assassin_drow_poison:
    $ hero.apply_trait("Poison Master")
    return
    
label mc_setup_warrior_assassin_drow_dagger:
    $ hero.apply_trait("Dagger Master")
    return
    
label mc_setup_warrior_assassin_drow_sister:
    $ hero.apply_trait("Sister Lover")
    return
    
label mc_setup_warrior_shooter_forest_elf:
    $ hero.apply_trait("Forest Elf Blood")
    return
    
label mc_setup_warrior_shooter_forest_elf_sniper:
    $ hero.apply_trait("Bow Master")
    return

label mc_setup_warrior_shooter_forest_elf_farsight:
    $ hero.apply_trait("Farsightedness")
    return
    
label mc_setup_warrior_shooter_forest_elf_ranger:
    $ hero.apply_trait("Elven Ranger")
    return
    
label mc_setup_warrior_shooter_summer_fay:
    $ hero.apply_trait("Fae Blood")
    return
    
label mc_setup_warrior_shooter_summer_fay_eternal:
    $ hero.apply_trait("Summer Eternality")
    return
    
label mc_setup_warrior_shooter_summer_fay_affinity:
    $ hero.apply_trait("Summer Affinity")
    return
    
label mc_setup_warrior_shooter_summer_fay_beacon:
    $ hero.apply_trait("Life Beacon")
    return
    
label mc_setup_warrior_defender_guard_armor:
    $ hero.apply_trait("Armor Expert")
    return
    
label mc_setup_warrior_defender_guard_left:
    $ hero.apply_trait("Left-Handed")
    return
    
label mc_setup_warrior_defender_guard_shield:
    $ hero.apply_trait("Shield Master")
    return
    
label mc_setup_warrior_defender_harpy_bones:
    $ hero.apply_trait("Hollow Bones")
    return

label mc_setup_warrior_defender_harpy:
    $ hero.apply_trait("Harpy Priestess Blood")
    return
    
label mc_setup_warrior_defender_harpy_meta:
    $ hero.apply_trait("Effective Metabolism")
    return
    
label mc_setup_warrior_defender_harpy_sky:
    $ hero.baseAP += 1
    $ hero.apply_trait("Sky Ward")
    return
    
label mc_setup_mage_arc_ghost:
    $ hero.apply_trait("Ghostly Structure")
    $ hero.apply_trait("Light")
    return
    
label mc_setup_mage_arc_ghost_intangible:
    $ hero.apply_trait("Incorporeal")
    return
    
label mc_setup_mage_arc_ghost_illusive:
    $ hero.apply_trait("Illusive")
    return
    
label mc_setup_mage_arc_ghost_light:
    $ hero.apply_trait("Master of Light")
    return
    
label mc_setup_mage_arc_vampire:
    $ hero.apply_trait("Vampiric Blood")
    $ hero.apply_trait("Darkness")
    return
    
label mc_setup_mage_arc_vampire_night:
    $ hero.apply_trait("Master of Darkness")
    return
    
label mc_setup_mage_arc_vampire_blood:
    $ hero.apply_trait("Blood Master")
    return
    
label mc_setup_mage_arc_vampire_reflex:
    $ hero.apply_trait("Perfect Reflexes")
    return
    
label mc_setup_mage_sorcerer_kitsune:
    $ hero.apply_trait("Kitsune Blood")
    $ hero.apply_trait("Fire")
    return
    
label mc_setup_mage_sorcerer_kitsune_fire:
    $ hero.apply_trait("Master of Fire")
    return
    
label mc_setup_mage_sorcerer_kitsune_mana:
    $ hero.apply_trait("Mana Source")
    return
    
label mc_setup_mage_sorcerer_kitsune_flow:
    $ hero.apply_trait("Magical Kin")
    return
    
label mc_setup_mage_sorcerer_winter:
    $ hero.apply_trait("Fae Blood")
    $ hero.apply_trait("Ice")
    return
    
label mc_setup_mage_sorcerer_winter_ice:
    $ hero.apply_trait("Master of Ice")
    return
    
label mc_setup_mage_sorcerer_winter_imm:
    $ hero.apply_trait("Winter Eternality")
    return
    
label mc_setup_mage_sorcerer_winter_win:
    $ hero.apply_trait("Winter Magician")
    return
    
label mc_setup_mage_researcher_android:
    $ hero.apply_trait("Artificial Body Structure")
    return
    
label mc_setup_mage_researcher_android_ele:
    $ hero.apply_trait("Master of Electricity")
    return
    
label mc_setup_mage_researcher_android_loop:
    $ hero.apply_trait("Looped Physiology")
    return
    
label mc_setup_mage_researcher_android_recharge:
    $ hero.apply_trait("Recharging")
    return
    
label mc_setup_mage_researcher_slime:
    $ hero.apply_trait("Liquid Body Structure")
    return
    
label mc_setup_mage_researcher_slime_water:
    $ hero.apply_trait("Master of Water")
    return
    
label mc_setup_mage_researcher_slime_aarcher:
    $ hero.apply_trait("Arcane Archer")
    return
    
label mc_setup_mage_researcher_slime_res:
    $ hero.apply_trait("Resilience")
    return