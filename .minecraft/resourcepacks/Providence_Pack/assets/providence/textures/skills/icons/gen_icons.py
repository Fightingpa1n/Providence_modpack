from PIL import Image, ImageColor, ImageDraw
import random

icons = [
    "health.png",
    "move.png",
    "defence.png",
    "stamina.png",
    "water.png",
    "jump.png",
    "temperature.png",
    "roll.png",
    "sword.png",
    "pickaxe.png",
]

special = [
    "health.png",
    "move.png",
    "defence.png",
    "stamina.png",
    "stats.png",
]

outline_color = "#ff7f00"
darken = 0.4

lava_outline = {
    "main": "#ef5902",
    "shadow": "#d44500",
    "dark": "#a83700",
}

def lava(image):
    outline_rgb = ImageColor.getcolor(outline_color, "RGBA")
    main_rgb = ImageColor.getcolor(lava_outline["main"], "RGBA")
    shadow_rgb = ImageColor.getcolor(lava_outline["shadow"], "RGBA")
    dark_rgb = ImageColor.getcolor(lava_outline["dark"], "RGBA")

    draw = ImageDraw.Draw(image)
    for x in range(image.width):
        for y in range(image.height):
            if image.getpixel((x, y)) == outline_rgb:
                rand = random.random()
                if rand < 0.6:
                    draw.point((x, y), fill=main_rgb)
                elif rand < 0.9:
                    draw.point((x, y), fill=shadow_rgb)
                else:
                    draw.point((x, y), fill=dark_rgb)
    del draw
    return image

def remove_outline(image):
    outline_rgb = ImageColor.getcolor(outline_color, "RGBA")

    draw = ImageDraw.Draw(image)
    for x in range(image.width):
        for y in range(image.height):
            if image.getpixel((x, y)) == outline_rgb:
                draw.point((x, y), fill=(0, 0, 0, 0))
    del draw
    return image

def darken_image(image):
    dark = image.copy()

    for x in range(dark.width):
        for y in range(dark.height):
            if dark.getpixel((x, y))[3] !=255: continue
            r, g, b, a = dark.getpixel((x, y))
            dark.putpixel((x, y), (int(r * darken), int(g * darken), int(b * darken), a))
    return dark

def merge_images(top, bottom):
    #we want to merge the top image onto the bottom image so that the top image is centered on the bottom image since it's smaller
    top_x = (bottom.width // 2) - top.width // 2
    top_y = (bottom.height // 2) - top.height // 2
    bottom.paste(top, (top_x, top_y), top)
    return bottom


def main():
    tile = Image.open("tile.png").copy().convert("RGBA")
    tile_lava = Image.open("tile_lava.png").copy().convert("RGBA")
    lock = Image.open("lock.png").copy().convert("RGBA")
    for icon in icons:
        try:
            ico = Image.open(icon).copy().convert("RGBA")

            ico_lava = lava(ico.copy())
            ico = remove_outline(ico)
            
            available = merge_images(ico, tile.copy())
            available.save(f"available/{icon}")

            unlocked = merge_images(ico_lava, tile_lava.copy())
            unlocked.save(f"unlocked/{icon}")

            locked = available.copy()
            locked = darken_image(locked)
            locked = merge_images(lock, locked)
            locked.save(f"locked/{icon}")


        except Exception as e:
            print(f"Failed to process {icon}: {e}")

    for icon in special:
        try:
            ico = Image.open(icon).copy().convert("RGBA")

            ico_lava = lava(ico.copy())
            ico = remove_outline(ico)

            name = icon.split(".")[0]
            ico.save(f"available/ico_{name}.png")
            ico_lava.save(f"unlocked/ico_{name}.png")

        except Exception as e:
            print(f"Failed to process {icon}: {e}")
    
    print("Done!")


if __name__ == "__main__":
    main()
