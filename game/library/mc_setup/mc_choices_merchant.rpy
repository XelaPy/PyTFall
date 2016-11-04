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

label mc_setup_warrior:
    $ hero.apply_trait("Tough")
    return
    
label mc_setup_warrior_warrior: # naturally, I dunno how to properly set base classes
    "Warrior class"
    return
    
label mc_setup_warrior_defender:
    "Defender class"
    return
    
label mc_setup_warrior_shooter:
    "Shooter class"
    return
    
label mc_setup_warrior_assassin:
    "Assassin class"
    return
    
label mc_setup_warrior_warrior_amazon: 
    $ hero.apply_trait("Amazon Blood")
    
label mc_setup_warrior_warrior_amazon_axe:
    $ hero.add_item("Great Axe")
    
label mc_setup_warrior_warrior_amazon_armor:
    $ hero.add_item("Mail Armor")
    
label mc_setup_warrior_warrior_amazon_dummy:
    $ hero.add_item("Simple Training Dummy")