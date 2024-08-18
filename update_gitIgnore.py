import os

# This python script will update the .gitignore file in the root directory of the project

# Special folders will get added in a way where we just accept any content instead of going through it
special_resourcepacks = ["Providence_Pack"]
special_configs = ["fancymenu", "ftbquests", "puffish_skills"]

# ================================================================================================== #

def go_through_mods(): 
    """Go through .minecraft/mods and add all jar files like this .minecraft/mods/<modname>.jar"""
    add_to_gitignore("# Mods Folder\n!.minecraft/mods/\n.minecraft/mods/*\n\n# Mods")

    for mod in os.listdir(".minecraft/mods"):
        if mod.endswith(".jar"):
            # If the filename has something written in brackets, rename that file
            if "[" in mod and "]" in mod:
                bracket_content = mod.split("[")[1].split("]")[0]
                mod_name = mod.split("[")[0]
                new_mod_name = f"{mod_name}-{bracket_content}.jar"
                os.rename(f".minecraft/mods/{mod}", f".minecraft/mods/{new_mod_name}")
                print(f"Renamed {mod} to {new_mod_name}")
                add_to_gitignore(f"!.minecraft/mods/{new_mod_name}")
            else:
                add_to_gitignore(f"!.minecraft/mods/{mod}")
    add_to_gitignore("\n")

def go_through_resourcepacks(): 
    """Go through .minecraft/resourcepacks and add all folders like this .minecraft/resourcepacks/<packname>/"""
    add_to_gitignore("# Resourcepacks Folder\n!.minecraft/resourcepacks/\n.minecraft/resourcepacks/*\n\n# Resourcepacks")

    for pack in os.listdir(".minecraft/resourcepacks"):
        if pack in special_resourcepacks and os.path.isdir(f".minecraft/resourcepacks/{pack}"):
            add_to_gitignore(f"!.minecraft/resourcepacks/{pack}/\n!.minecraft/resourcepacks/{pack}/*\n!.minecraft/resourcepacks/{pack}/**")
        else:
            if pack.endswith(".zip") or pack.endswith(".rar"):
                add_to_gitignore(f"!.minecraft/resourcepacks/{pack}")
    add_to_gitignore("\n")

def go_through_configs(): 
    """Go through .minecraft/config and add all folders like this .minecraft/config/<configname>/"""
    add_to_gitignore("# Configs Folder\n!.minecraft/config/\n.minecraft/config/*\n\n# Configs")

    for config in os.listdir(".minecraft/config"):
        if os.path.isdir(f".minecraft/config/{config}"):
            if config in special_configs:
                add_to_gitignore(f"!.minecraft/config/{config}/\n!.minecraft/config/{config}/*\n!.minecraft/config/{config}/**")
            else:
                add_folder(f".minecraft/config/{config}")
        else:
            add_to_gitignore(f"!.minecraft/config/{config}")
    add_to_gitignore("\n")

def go_through_defaultconfigs(): 
    """Go through .minecraft/defaultconfigs and add all folders like this .minecraft/defaultconfigs/<configname>/"""
    add_to_gitignore("# DefaultConfigs Folder\n!.minecraft/defaultconfigs/\n.minecraft/defaultconfigs/*\n\n# DefaultConfigs")

    for config in os.listdir(".minecraft/defaultconfigs"):
        if os.path.isdir(f".minecraft/defaultconfigs/{config}"):
            add_folder(f".minecraft/defaultconfigs/{config}")
        else:
            add_to_gitignore(f"!.minecraft/defaultconfigs/{config}")
    add_to_gitignore("\n")

def go_through_shaderpacks(): 
    """Go through .minecraft/shaderpacks and add all folders like this .minecraft/shaderpacks/<shaderpackname>/"""
    add_to_gitignore("# Shaderpacks Folder\n!.minecraft/shaderpacks/\n.minecraft/shaderpacks/*\n\n# Shaderpacks")

    for shaderpack in os.listdir(".minecraft/shaderpacks"):
        if os.path.isdir(f".minecraft/shaderpacks/{shaderpack}"):
            add_folder(f".minecraft/shaderpacks/{shaderpack}")
        else:
            add_to_gitignore(f"!.minecraft/shaderpacks/{shaderpack}")
    add_to_gitignore("\n")

# ================================================================================================== #

def add_folder(folder_path):
    add_to_gitignore(f"!{folder_path}/\n{folder_path}/*")
    for file in os.listdir(folder_path):
        if os.path.isdir(f"{folder_path}/{file}"):
            add_folder(f"{folder_path}/{file}")
        else:
            add_to_gitignore(f"!{folder_path}/{file}")

def add_to_gitignore(text): 
    """Add string to .gitignore file"""
    with open(".gitignore", "a") as file:
        file.write(text + "\n")

def clear_gitignore(): 
    """Clears the .gitignore file"""
    with open(".gitignore", "w") as file:
        file.write(".minecraft/*\n.minecraft/**\n\n\n")

# ================================================================================================== #

clear_gitignore()
go_through_mods()
go_through_resourcepacks()
go_through_configs()
go_through_defaultconfigs()
go_through_shaderpacks()
